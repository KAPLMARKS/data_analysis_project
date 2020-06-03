from api import Api
from models import Post, Comment

whitelist = open('whitelist.txt').readlines
blacklist = open('blacklist.txt').readlines

def main():
  print('Please, enter your login')
  login = input
  print('Please, enter your password')
  password = input

  api = Api(login, password)

  print("Please, enter analyzing wall owner's id or 'stop' to exit")
  owner_id = input
  while 'stop' != owner_id:
    print('Is it a group?')
    is_group = input
    posts = api.get_posts_with_comments(owner_id, is_group)
    for post in posts:
      print('\n\n\n')
      print('Text: ' + post.text)
      print(post.likes_count + ' likes')
      print(post.reposts_count + ' reposts')
      if post.views_count == 0:
        print('Unable to rate post. Missing views count.')
      else: 
        print('Rating: ' + rate_post(post))

def rate_post(post):
  t = post.text
  l = post.likes_count
  r = post.reposts_count
  v = post.views_count
  c = post.comments

  return ((150 * (l + 10 * r) / v) + rate_text(t) + rate_comments(c)) / 3

def rate_text(text):
  w = 1
  for word in whitelist:
    if word in text:
      w += 1

  b = 0
  for word in blacklist:
    if word in text:
      b += 1

  return 10 - 2 * b / w

def rate_comments(comments):
  s = 0
  for comment in comments:
    s += rate_text(comment.text)
  
  return s / comments.len()
