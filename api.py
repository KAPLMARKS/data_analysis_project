import vk_api
from models import Post, Comment

class Api:
    def __init__(self, login, password):
        vk_session = vk_api.VkApi(login, password)
        vk_session.auth()
        self.tools = vk_api.VkTools(vk_session)

    def get_posts(self, owner_id, is_group):
        owner_id = int(owner_id)
        if is_group:
            owner_id = -owner_id
        wall = self.tools.get_all('wall.get', 100, {'owner_id': owner_id})

        posts = []
        for post_data in wall['items']:
            posts.append(Api.parse_post(post_data))

        return posts

    def parse_post(post_data):
        text = post_data['text']
        
        copy_history = []
        if 'copy_history' in post_data:
            copy_history = list(map(Api.parse_post, post_data['copy_history']))
            for post in copy_history:
                text += ' ' + post.text

        likes_count = 0
        if 'likes' in post_data:
            likes_count = post_data['likes']['count']

        reposts_count = 0
        if 'reposts' in post_data:
            reposts_count = post_data['reposts']['count']

        views_count = -1
        if 'views' in post_data:
            views_count = post_data['views']['count']

        return Post(post_data['id'], text, likes_count, reposts_count, views_count)

    def get_comments(self, owner_id, post_id, is_group):
        owner_id = int(owner_id)
        if is_group:
            owner_id = -owner_id
        comments_data = self.tools.get_all('wall.getComments', 100, {
            'owner_id': owner_id,
            'post_id': post_id,
            'need_likes': 1
        })['items']
        comments = []
        for comment_data in comments_data:
            comments.append(Api.parse_comment(comment_data))

        return comments

    def parse_comment(comment_data):
        return Comment(comment_data['text'], comment_data['likes']['count'])

    def get_posts_with_comments(self, owner_id, is_group):
        posts = self.get_posts(owner_id, is_group)
        for post in posts:
            post.comments = self.get_comments(owner_id, post.post_id, is_group)

        return posts
