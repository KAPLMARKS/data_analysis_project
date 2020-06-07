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

  ratings = []
  if t:
    ratings.append(rate_text(t))
  ratings.append(rate_feedback(l, r, len(c), v))
  if len(c) != 0:
    ratings.append(rate_comments(c))

  sum = 0
  for rating in ratings:
    sum += rating
  return sum / len(ratings)

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

def rate_feedback(likes, reposts, comments_count, views):
  return min((likes + 100 * reposts + 20 * comments_count) / (views * 0.8), 10)

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
