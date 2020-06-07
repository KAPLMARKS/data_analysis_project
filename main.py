from api import Api
from models import Post, Comment

whitelist = []
with open('whitelist.txt','r') as file: 
  for line in file: 
    whitelist.append(line)  
blacklist = []
with open('blacklist.txt','r') as file: 
  for line in file: 
    blacklist.append(line)

def rate_post(post):
  t = post.text
  l = post.likes_count
  r = post.reposts_count
  v = post.views_count
  c = post.comments

  rating = 0
  text_rating = rate_text(t)
  feedback_rating = rate_feedback(l, r, v)
  if len(c) != 0:
    comments_rating = rate_comments(c)
    rating = (text_rating + feedback_rating + comments_rating) / 3
  else: 
    rating = (text_rating + feedback_rating) / 2

  return rating

def rate_text(text):
  w = 1
  for word in whitelist:
    if word in text:
      w += 1

  b = 0
  for word in blacklist:
    if word in text:
      b += 1

  rating = 10 - 2 * b / w
  if rating < 0:
    rating = 0

  return rating

def rate_feedback(likes, reposts, views):
  return min((likes + 10 * reposts) / (views * 0.5), 10)

def rate_comments(comments):
  s = 0
  for comment in comments:
    s += rate_text(comment.text)
  
  return s / len(comments)

print('Please, enter your login')
login = input()
print('Please, enter your password')
password = input()

api = Api(login, password)

print("Please, enter analyzing wall owner's id or 'stop' to exit")
owner_id = input()
while 'stop' != owner_id:
  print('Is it a group?')
  is_group = input()
  posts = api.get_posts_with_comments(owner_id, is_group)
  ratings = []
  for post in posts:
    print('\n\n\n')
    print('Text: ' + str(post.text))
    print('Likes: ' + str(post.likes_count))
    print('Reposts:' + str(post.reposts_count))
    print('Views: ' + str(post.views_count))
    if post.views_count < 1:
     print('Unable to rate post. Missing views count.')
    else: 
      rating = rate_post(post)
      ratings.append(rating)
      print('Rating: ' + str(rating))
  overallRating = 0
  for rating in ratings:
    overallRating += rating
  overallRating = overallRating / len(ratings)
  print('Overall rating: ' + str(overallRating))
  
  print('\n\n\n')
  print("Please, enter analyzing wall owner's id or 'stop' to exit")
  owner_id = input()
