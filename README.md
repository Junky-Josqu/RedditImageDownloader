# Reddit Image Downloader -- Module Fork

A python Module for reddit that downloads pictures and gifs from a given subreddit.
For The original script see [georgeglessner](https://github.com/georgeglessner/RedditImageDownloader)
# Setup 
1. Create a [reddit personal use script application](https://www.reddit.com/prefs/apps/).

2. Edit Following Variables in download_images.py and your applications credentials.

		ID='YOUR_ID'  
		SECRET='YOUR_SECRET'  
		PASSWORD='YOUR_PASSWORD'  
		AGENT='Example Bot by /u/example_bot'  
		USERNAME='YOUR_USERNAME'  

3. Run `pip install -r requirements.txt`

# Usage


	Usage: import download_images.py
           download_images.py.download(SUBREDDIT, NUM_PICS, SEARCH_TERM, PAGE, DOWNLOADDIR)


Your images will appear in the DOWNLOADDIR folder created by the application.

__Helpful note:__ To view .gif files on a Mac select the image(s) and press `cmd` + `y` or install a appropriate OS like Arch Linux.


