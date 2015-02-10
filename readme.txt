The codes were written for fun to submit as a CS50 final project.

Overview 

Instagram Analysis is a command line Python program that scrapes websta.me website (an Instagram Web Viewer). The program can download all the Instagram pictures of a specified user as well as other information e.g. the number of likes, comments, picture filtersand dates posted. It then generates an HTML file that has a table consisting of these information. The table can be sorted, so that a user can use it to analyze what makes their photos popular or appealing to their followers. 

------------------------------------------------------------------------------------------

Requirements

In Mac OS X, make sure that you have Python 2.7.x installed. You also need to install other modules used in this project. First, make sure that pip (Python Package Index) is installed in your computer. If not, please head to https://pip.pypa.io/en/latest/installing.html#install-or-upgrade-pip and install it accordingly. After pip is installed, open terminal again. Type the following to install modules:
	sudo pip install BeautifulSoup4
	sudo pip install requests
However, if python signifies that you are missing any module upon running, please type pip install name_of_modue to install it. 

------------------------------------------------------------------------------------------

How to run the program 

1. Open the terminal.
2. Use cd command to navigate yourself to the folder of the program, which is the folder that contains main.py 
3. Type "python main.py instagram_username "For example, if your username is mirandakerr, you should type "python main.py mirandakerr" 

------------------------------------------------------------------------------------------
|_ main.py
|_ include
|_ output
  |_ instagram_username1
  |_ analysis_username1.html
  |_ instagram_username2
  |_ analysis_username2.html
|_ js 
|_ css

What does this program do? 

1. By typing python main.py instagram_username, you are downlaoding, by default, latest 100 posts of an instagram user. After typing the command, you should see a folder output created. Inside output folder, you should see a folder called "instagram_username" depending on the username that you types. This folder contains all the pictures that have been downloaded. In output folder, you should see another file analysis_username.html. This file contains a table with 5 columns: #likes, #comments, pictures, date, filter. You can click at the head of each column to sort a column. This should give you an insight as to which pictures are most popular among your followers and perhaps why as well.

2. You can synchronize this folder by typing the same command line of the same user again. Both pictures and the analysis html file will be updated accordingly. 

3. If the user does not exist, does not have any post or set to private, the program will display the warning accordingly.

4. If the post is a video, the program does not download a video. But rather just print in html file thatthis post is a video with numbers of likes and comments with a link for a user to navigate to.