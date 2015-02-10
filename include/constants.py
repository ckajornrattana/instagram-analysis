# CS50 Final Project
# Instagram Analysis 
# constants.py 
# by Chaowat (Mick) Kajornrattana and Surekha (Catherine) Tuntiserirat 
#
# This file contains the constants used by main.py 

# base url of the website that we will be scraping 
WEBSTA_URL = 'http://websta.me'

# for example, http://websta.me/n/catherine is the page of user named 'catherine'
WEBSTA_USER_URL = 'http://websta.me/n/'

# the maximum number of latest posts that the program will download
POSTS_LIMIT = 100

# folder that all data will be saved
OUTPUT_FOLDER = 'output/'

# prefix name for folder that user's data will be saved
FOLDER_PREFIX = 'instagram_'

# prefix name for html file which contains data analysis
HTML_PREFIX = 'analysis_'

# css classes that are used for scraping.
CLASS_USER_PROFILE = 'page_header'
CLASS_POSTS_COUNT = 'counts_media'
CLASS_FOLLOWED_COUNT = 'counts_followed_by'
CLASS_FOLLOWING_COUNT = 'following'
CLASS_EACH_POST = 'photoeach clearfix'
CLASS_POST_URL = 'mainimg'
CLASS_LIKE_COUNT = 'like_count_'
CLASS_COMMENT_COUNT = 'comment_count_'
CLASS_FILTER = 'filter'
CLASS_IMG_URL = 'mainimg'
CLASS_TIME = 'time utime'
CLASS_NEXT_PAGE = 'pager'

# the text that signals that this post contains video
VIDEO = 'Video'

# the text that signals that this user page is private
PRIVATE = 'This user is private.'

# the text that signals that this user does not exist 
NOT_EXISTS = '404 Not Found.'

# the format of human readable time which is used to convert/revert unix time 
TIME_STRING_FORMAT = '%Y-%m-%d %H:%M:%S'

# html header that will be printed to every analysis_username.html 
HTML_HEADER = (
	'<!DOCTYPE html>'
	'<html>'
		'<head>'
			'<script type="text/javascript" src="../js/jquery-2.1.1.min.js"></script>'
			'<script type="text/javascript" src="../js/jquery.tablesorter.js"></script>'
			'<script type="text/javascript" src="../js/script.js"></script>'
			'<link href="../css/blue/style.css" rel="stylesheet"/>'
		'</head>'
		'<body>'
			'<table id="analysis" class="tablesorter table table-striped table-bordered">'
				'<thead>'
					'<tr>'
						'<th>#Likes</th>'
						'<th>#Comments</th>'
						'<th>Pictures</th>'
						'<th>Date</th>'
						'<th>Filter</th>'
				    '</tr>'
			    '</thead>'
			    '<tbody>'
			     
			     
)

# html footer that will be prinited at the end
HTML_FOOTER = '</tbody></table></body></html>'