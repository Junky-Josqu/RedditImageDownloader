#!/usr/bin/env python
'''

MIT License

Copyright (c) 2018 George

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Edided Last time by JohnaOne on 2 April 2019 making it to a python Module
Editd by JohnaOne on 3 April 2019 converting code into python 3 and also bugfixing and as well replacing image folder with variable DOWNLOADDIR
Edited by Johnaone on 4 April 2019 Bugfix
Edited by JohnaOne on 12 April 2019 stopping it from downloading gifs
REQUIRES:
praw
prawcore
docopt

Reddit Image Downloader
'''

import praw
import urllib.request, urllib.parse, urllib.error
import sys
import os
import signal
from prawcore import NotFound
from prawcore import PrawcoreException

#SUBREDDIT = 'funny'
#NUM_PICS = 3
#SEARCH_TERM = None
#PAGE = 'hot'
#DOWNLOADDIR = 'memes'
def download(SUBREDDIT, NUM_PICS, SEARCH_TERM, PAGE, DOWNLOADDIR, ID, SECRET, PASSWORD, AGENT, USERNAME):
    # initialize variables
    #subreddit = ''
    #num_pics = 0

    # handle 'ctrl + c' if downloads takes too long
    def sigint_handler(signum, frame):
        print('\nQuitting...')
        sys.exit(1)

    signal.signal(signal.SIGINT, sigint_handler)

    # connect to reddit
    reddit = praw.Reddit(
        client_id=ID,
        client_secret=SECRET,
        password=PASSWORD,
        user_agent=AGENT,
        username=USERNAME)

    # get values of arguments
    #subreddit = arguments.get('--subreddit')
    #num_pics = int(arguments.get('--number'))
    #search_term = arguments.get('--query')
    #page = arguments.get('--page')
    subreddit = SUBREDDIT
    num_pics = int(NUM_PICS)
    search_term = SEARCH_TERM
    page = PAGE

    # prompt for a subreddit if none given
    if subreddit == None:
        while True:
            # obtain subreddit to download %s from, and number of %s to download
            subreddit = input('Please enter subreddit: ')

            # check that subreddit exists
            try:
                reddit.subreddits.search_by_name(subreddit, exact=True)
                break
            except NotFound:
                print('Subreddit %s does not exist.' % subreddit)

    # determine what to search
    if search_term == None:
        if page == 'hot':
            results = reddit.subreddit(subreddit).hot()
        elif page == 'controversial':
            results = reddit.subreddit(subreddit).controversial()
        elif page == 'top':
            results = reddit.subreddit(subreddit).top()
        elif page == 'rising':
            results = reddit.subreddit(subreddit).rising()
        elif page == 'new':
            results = reddit.subreddit(subreddit).new()
    else:
        results = reddit.subreddit(subreddit).search(
            search_term, params={'nsfw': 'yes'})

    # create %s folder if one does not exits
    if not os.path.exists(DOWNLOADDIR):
        os.mkdir(DOWNLOADDIR)

    # find %s/gifs in subreddit
    try:
        count = 1
        for submission in results:
            if count <= num_pics:
                if 'https://i.imgur.com/' in submission.url or 'https://i.redd.it' in submission.url:
                    img_url = submission.url
                    _, extension = os.path.splitext(img_url)
#                   if extension in ['.gif', '.gifv']: # check if file is gif and breaks
#                       print('cant handle gif gonna break')
#                       count += 1
#                       break
                    if extension in ['.jpg', '.gif', '.jpeg', '.png']:
                        print('\nDownloading', subreddit + str(
                            count) + extension)
                        print('Source:', img_url)
                        print('Comments: https://www.reddit.com/r/' + subreddit + '/comments/' + str(
                            submission))
                        urllib.request.urlretrieve(img_url, '%s/%s%i%s' %
                                           (DOWNLOADDIR, subreddit, count, extension))
                        count += 1
                    # .gifv file extensions do not play, convert to .gif
                    elif extension == '.gifv':
                        print('\nDownloading', subreddit + str(count) + '.gif')
                        print('Source:', img_url)
                        print('Comments: https://www.reddit.com/r/' + subreddit + '/comments/' + str(
                            submission))
                        root, _ = os.path.splitext(img_url)
                        img_url = root + '.gif'
                        urllib.request.urlretrieve(img_url, '%s/%s%i%s' %
                                           (DOWNLOADDIR, subreddit, count, '.gif'))
                        count += 1
                if 'https://thumbs.gfycat.com/' in submission.url:
                    img_url = submission.url
                    print('\nDownloading', subreddit + str(count) + '.gif')
                    print('Source:', img_url)
                    print('Comments: https://www.reddit.com/r/' + subreddit + '/comments/' + str(
                        submission))
                    urllib.request.urlretrieve(img_url, '%s/%s%i%s' %
                                       (DOWNLOADDIR, subreddit, count, '.gif'))
                    count += 1
                # some gfycat conversions will not work due to capitalizations of link
                if 'https://gfycat.com/' in submission.url:
                    img_url = submission.url
                    img_url = img_url.split('https://', 1)
                    img_url = 'https://thumbs.' + img_url[1]
                    if 'gifs/detail/' in img_url:
                        img_url = img_url.split('gifs/detail/', 1)
                        img_url = img_url[0] + img_url[1]
                    root, _ = os.path.splitext(img_url)
                    img_url = root + '-size_restricted.gif'
                    print('\nDownloading', subreddit + str(count) + '.gif')
                    print('Source:', img_url)
                    print('Comments: https://www.reddit.com/r/' + subreddit + '/comments/' + str(
                        submission))
                    urllib.request.urlretrieve(img_url, '%s/%s%i%s' %
                                       (DOWNLOADDIR, subreddit, count, '.gif'))
                    count += 1
            else:
                print('\nCompleted!\n')
                break

    except PrawcoreException:
        print('\nError accessing subreddit!\n')


#if __name__ == '__main__':
#    arguments = docopt(__doc__)
#    main()
