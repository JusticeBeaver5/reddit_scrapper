

test_subreddit = 'funny' # subreddit name
test_filter = 'hot' #['hot', 'top', 'controvercial', 'new', rising]
test_timeframe = 'day'  #['hour', 'day', 'week', 'month', 'year, 'all']



class RedditPost:
    import json
    import requests

    def __init__(self, subreddit, filter, posts_limit=1, timeframe=None, max_comments=20, best_comments=None):
        self.subreddit = subreddit
        self.filter = filter
        self.posts_limit = posts_limit
        self.timeframe = timeframe
        self.max_comments = max_comments
        self.best_comments = 5


    # get reddit post
    def request_subreddit_posts(self):
        '''Get list of posts in provided subreddit'''

        if self.subreddit == 'hot' or 'new':
            url = f'https://www.reddit.com/r/{self.subreddit}/{self.filter}.json?limit={self.posts_limit}'
        url = f'https://www.reddit.com/r/{self.subreddit}/{self.filter}.json?limit={self.posts_limit}&t={self.timeframe}'
        request = self.requests.get(url,
                            headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36)'})
        return request.json()


    # get posts and sort them by date, return the latest one.
    def get_post_id(self):
        '''Get post id'''

        if self.subreddit != 'hot':
            self.post_id = self.request_subreddit_posts()['data']['children'][0]['data']['id']
        self.post_id = self.request_subreddit_posts()['data']['children'][2]['data']['id']
        return self.post_id


    # get titles comments, images and video urls
    def get_post_data(self):

        '''this method makes request to get post title, any images video or gif files and top comments in the post'''

        url = f'https://www.reddit.com/r/{self.subreddit}/comments/{self.get_post_id()}.json?limit={self.max_comments}'
        request = self.requests.get(url, headers={
            'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36)'})

        age_restricted = request.json()[0]['data']['children'][0]['data']['over_18']
        title, img_url, vid_url, audio_url, post_id, subreddit = [],[],[],[],[],[]
        title.append(request.json()[0]['data']['children'][0]['data']['title'])
        post_id.append(request.json()[0]['data']['children'][0]['data']['id'])
        subreddit.append(request.json()[0]['data']['children'][0]['data']['subreddit_name_prefixed'])
        try:
            vid_url.append(request.json()[0]['data']['children'][0]['data']['media']['reddit_video']['fallback_url'])
            audio_url.append('https://v.redd.it/' + vid_url[0].split('/')[3] + '/DASH_audio.mp4')
            img_url.append(None)
        except TypeError as e:
            print(e, 'no video found')
        try:
            x = request.json()[0]['data']['children'][0]['data']['gallery_data']['items']
            y = request.json()[0]['data']['children'][0]['data']['media_metadata']
            for i in range(len(x)):
                med_id  = x[i]['media_id']
                temp_link = y[med_id]['s']['u']
                temp_link = temp_link.replace("amp;", '')
                img_url.append(temp_link)
        except KeyError as error:
            print(error, 'no galery found')
            pass
        if not img_url:
            img_url.append(request.json()[0]['data']['children'][0]['data']['url'])

        comment_list = []
        if request.json()[1]['data']['children']:
            stickied = request.json()[1]['data']['children'][0]['data']['stickied']
            if len(request.json()[1]['data']['children']) > self.best_comments:
                for i in range(0 + int(stickied), self.best_comments + int(stickied)):
                    author = request.json()[1]['data']['children'][i]['data']['author']
                    ups = request.json()[1]['data']['children'][i]['data']['ups']
                    if author != '[deleted]':
                        comment = request.json()[1]['data']['children'][i]['data']['body']
                        comment_list.append(f'"{comment}" -by {author}\n--------------')
                        # comment_list.append(f'"{comment}" -by {author}, {ups} upvotes\n--------------') # comments with upvotes 

        return [title, post_id, img_url, vid_url, audio_url, [age_restricted], subreddit, comment_list] #post_type






a = RedditPost('funny', 'hot')
# a.request_subreddit_posts()
# print(a.get_post_id())
print(a.get_post_data())