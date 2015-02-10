# CS50 Final Project
# Instagram Analysis 
# functions.py 
# by Chaowat (Mick) Kajornrattana and Surekha (Catherine) Tuntiserirat 
#
# This file contains the functions used by main.py 

import os
import commands
import re
from constants import *

# create folder as specified by absolute destination. return true upon success
# exit with code 1 if cannot create folder, return false if folder already exists  
def create_folder(folder_path):

	# check if folder named output already exists 
	if not os.path.exists('output'):
		# mkdir linux command
		cmd = 'mkdir ' + OUTPUT_FOLDER
		# execut mkdir command and print error if any
		(status, output) = commands.getstatusoutput(cmd)
		if status: 
			sys.stderr.write('there was an error:' + output) 
			sys.exit(1)

	# check if the folder already exists
	if not os.path.exists(folder_path):
		# mkdir linux command
		cmd = 'mkdir ' + folder_path
		# execut mkdir command and print error if any
		(status, output) = commands.getstatusoutput(cmd)
		if status: 
			sys.stderr.write('there was an error:' + output) 
			sys.exit(1)
	return

# count the number of files in folder 
def count_files(folder_path):
	counter = 0
	for file in os.listdir(folder_path): 
		counter += 1 
	return counter 

# take a parameter of a url and return the name of file with .jpg filetype 
# if .jpg is not found at the end, return None 
def get_filename(url):
	filename_regex = '\w+\.jpg'
	filename = re.search(filename_regex, url)
	if filename:
		return filename.group(0)
	return None

# take a parameter of an associative array of a post
# return a line of values from an array separated by a tab
def array_to_line(post):
	return post['url'] + '\t' + post['img_url'] + '\t' + post['like'] + '\t' + post['comment'] + '\t' \
		+ post['filter'] + '\t' + post['date'] + '\t' + post['utime'] + '\t' + post['img_name'] + ' \n'

# take a parameter of an associative array of post 
# return an html string that represents the row of a table 
def get_html_row(post, img_dest):
	like_cell = '<td>' + post['like'] + '</td>'
	comment_cell = '<td>' + post['comment'] + '</td>'
	# ensure that an image is a video 
	if post['img_url'] == VIDEO or post['img_name'] == VIDEO:
		picture_cell = '<td> <a href="' + post['url'] + '" target="_blank"> Video </a></td>'
	else:	
		picture_cell = '<td><a href="' + post['url'] + '" target="_blank">' + '<img src="../' \
		+ img_dest + '" width="100"/></a></td>'
	date_cell = '<td>' + post['date'] + '</td>'
	filter_cell = '<td>' + post['filter'] + '</td>'
	return '<tr>' + like_cell + comment_cell + picture_cell + date_cell + filter_cell + '</tr>'

# signal this error for an error that occurs when scraping a website
# the cause of this error is either the web is loaded incorrectly or the strucutre of a page might be changed
def error_scraping():
	print 'There is an error in scraping websta.me. Please try again.'
	exit(4)


