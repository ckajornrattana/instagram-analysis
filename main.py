#! /usr/bin/python

# CS50 Final Project
# Instagram Analysis 
# main.py 
# by Chaowat (Mick) Kajornrattana and Surekha (Catherine) Tuntiserirat 
#
# Please read the documentation. Enjoy! 

import sys
sys.path.append('include/')
from functions import *
from constants import *
import os
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') 
from bs4 import BeautifulSoup
import requests
import re
import urllib
from datetime import datetime


def main():

    # ensure proper usage
    if len(sys.argv) != 2: 
        print 'usage: python main.py instagram_user'
        exit(1)

    # use regex to check for non-alphanumeric character
    if re.search('\[.W]', sys.argv[1]):
        print 'usage: only a-z, A-Z, 0-9 . and _ are accepted'
        exit(1)

    # set the default number of posts to be downloaded (default is 100)
    limit = POSTS_LIMIT

    # interested instagram username
    instagram_user = sys.argv[1]

    # name of folder that all files will be saved  | create folder of this name 
    user_folder_path = OUTPUT_FOLDER + FOLDER_PREFIX + instagram_user + '/'

    # (synchronization) name of a log file
    log_file =  user_folder_path + instagram_user + '.log'

    # (synchronization) read log files. each line represents an element of an array 
    lines = None
    if os.path.exists(log_file):
        with open(log_file, 'r') as log_f:
            lines = log_f.readlines()

    # (synchronization) load lines into an array called prev_posts
    prev_posts = []
    # check if lines is not empty 
    if lines: 
        for line in lines:
            # each line, a field is seprated by a tab
            fields = line.split('\t')
            # ensure that log file is correct
            if len(fields) == 8: 
                # group interested infos of a post as an associative array (aka. dictionary in python)
                prev_post = {'url': fields[0], 'img_url': fields[1], 'like': fields[2], 'comment': fields[3], 
                    'filter': fields[4], 'date': fields[5], 'utime': fields[6], 'img_name': fields[7]}
                prev_posts.append(prev_post)

    # websta.me url
    websta_url = WEBSTA_USER_URL + instagram_user

    # all posts (array)
    posts = []

    # inform user of synchronization
    if prev_posts: 
        print 'Detected a log file'
        print 'Begin synchronizing....'

    counter = 0
    while True: 

        # retrieve source code (string type) from websta_url 
        source_code = requests.get(websta_url)
        # signal error which might be because the user does not exist.
        if source_code.status_code != 200:
            print 'There is an error connecting to server. Please try again :/'
            print 'It is possible that the user might not exist.'
            exit(3)

        # source code (structured by BeautifulSoup class)
        source_code_soup = BeautifulSoup(source_code.content)

        # scrape user profile and handle user error in the first loop 
        if counter == 0: 

            # page_header class contain user profile information
            page_headers = source_code_soup.find_all('div', class_ = CLASS_USER_PROFILE)

            # page_headers not empty 
            if page_headers:

                # check if the user is private 
                if len(page_headers) == 2:
                    if page_headers[1].find('h1'):
                        if page_headers[1].find('h1').string.strip() == PRIVATE:
                            print 'The user page is set to private.'
                            exit(2)


                # if user exists, scrape user profile info 
                # f_ means find | variable with f_ at front is needed to ensure the element is found
                f_posts_count = page_headers[0].find('span', class_ = CLASS_POSTS_COUNT)

                # ensure the interested elements are found and the contents thereof are not empty
                if (f_posts_count and f_posts_count.string):

                    # keep number of posts, followers and following 
                    posts_count = locale.atoi(f_posts_count.string.strip())
                    
                    # converting string (with commas) to integer 
                    if posts_count == 0:
                        print 'The user does not have any post'
                        exit(2)

                    # user does not have enough posts || or when synchronize, try all the posts (limit = number of posts)
                    if limit > posts_count or prev_posts: 
                        limit = posts_count

                    # create folder for a user for all files to be saved
                    create_folder(user_folder_path)

                # upon failure, signal error          
                else:
                    error_scraping()

            # upon failure, signal error 
            else:
                error_scraping()

        # all posts (structured by BeautifulSoup class)
        posts_soup = source_code_soup.find_all('div', class_= CLASS_EACH_POST)

        # iterate over each element in posts_soup to append a tuple that contains post infos to posts
        for post_soup in posts_soup:

            # use BeautifulSoup to search thru DOM by html tag and css class to get post infos
            # f_ means find | variable with f_ at front is needed to ensure the element is found
            f_post_url = post_soup.find('a', class_ = CLASS_POST_URL)
            f_like_count = post_soup.find('span', class_ = re.compile(CLASS_LIKE_COUNT))
            f_comment_count = post_soup.find('span', class_ = re.compile(CLASS_COMMENT_COUNT))
            f_img_filter = post_soup.find('span', class_ = CLASS_FILTER)

            # ensure the interested elements are found and the contents thereof are not empty
            if (f_post_url and f_post_url.get('href') and f_like_count and f_like_count.string and
                f_comment_count and f_comment_count.string and f_img_filter and f_img_filter.string):

                post_url = WEBSTA_URL + f_post_url.get('href')
                like_count = f_like_count.string.strip()
                comment_count = f_comment_count.string.strip()
                img_filter = f_img_filter.string.strip()

            else:
                error_scraping()
            
            # image source and exact date of a post are on another page. retrieve source code from that page
            post_source_code = requests.get(post_url)
            # ensure that the reponse code is 200 OK 
            if post_source_code.status_code != 200:
                print 'There is an error connecting to server. Please try again :/'
                exit(3)

            post_sc_soup = BeautifulSoup(post_source_code.content)
            f_img_url = post_sc_soup.find('a', class_ = CLASS_IMG_URL)
            f_unix_time = post_sc_soup.find('span', class_ = CLASS_TIME)

            # set img_url None if the user posts video
            if img_filter == VIDEO:
                img_url = VIDEO
                img_name = VIDEO
            # for image url, ensure that f_img_url is found and is not empty
            elif f_img_url and f_img_url.get('href'):
                img_url = f_img_url.get('href')
                img_name = get_filename(img_url)
            else: 
                error_scraping()

            # ensure f_unix_time is found and the content thereof is not empty
            if f_unix_time and f_unix_time.get('data-utime'):
                # convert unix time to human readable time
                unix_time = f_unix_time.get('data-utime')
                human_time = datetime.fromtimestamp(int(unix_time)). strftime(TIME_STRING_FORMAT)

            else: 
                error_scraping()

            # the time of this post is before the latest post that was downloaded last time. 
            if prev_posts and unix_time <= prev_posts[0]['utime']:
                # set counter to the maximum int to break out of while loop
                counter = sys.maxint 
                break
            
            # group interested infos of a post as an associative array (aka. dictionary in python)
            post_arr = {'url': post_url, 'img_url': img_url, 'like': like_count, 'comment': comment_count, 
                            'filter': img_filter, 'date': human_time, 'utime': unix_time, 'img_name': img_name}

            # append this tuple to array posts
            posts.append(post_arr)

            # increment and break twice if next post will be more than number specified
            counter += 1

            # Update user with progress for every 10 pages that are opened 
            if counter % 10 == 0:
                print 'Source codes of ' + str(counter) + ' pages have been downloaded.'

            # break out of while loop if the limit has been reached
            if counter >= limit: 
                break

        if counter >= limit: 
            break

        next_page_soup = source_code_soup.find('ul', class_ = CLASS_NEXT_PAGE)
        # check if next page really exists
        if next_page_soup and next_page_soup.find('a') and next_page_soup.find('a').get('href'):
            # go to next page
            websta_url = WEBSTA_URL + next_page_soup.find('a').get('href')
        else: 
            break

    # inform user that your synchronization is up to date. then terminate the program. 
    if len(posts) == 0:
        print 'there is nothing be synchronized. please try again later.'
        exit(0)

    # open analysis html and log file to write. with statement handle error and close file automatically 
    with open(log_file, 'w') as log_f, open(OUTPUT_FOLDER + HTML_PREFIX + instagram_user + '.html', 'w') as html_f:

        # write header in html file 
        html_f.write(HTML_HEADER)

        # write data to log file and html file 
        for post in posts:
            # write a post as a line in a log file
            log_f.write(array_to_line(post))
            # Download image. to the folder 
            img_dest = user_folder_path + post['img_name']
            if post['img_url'] != VIDEO:
                urllib.urlretrieve(post['img_url'], img_dest)
            # write each post as a row in html file
            html_f.write(get_html_row(post, img_dest))

        # append data from previous retrieval to log file and html file, but no need to reload all images again
        for prev_post in prev_posts:
            log_f.write(array_to_line(prev_post))
            img_dest = user_folder_path + prev_post['img_name']
            html_f.write(get_html_row(prev_post, img_dest))
            
        # write footer in html file 
        html_f.write(HTML_FOOTER)

    # update user with the progress
    print 'Done!'
    exit(0)


if __name__ == '__main__':
    main()
    