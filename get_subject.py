import json
import requests
import sqlite3
import re
import sys
import collections
import pytz
import datetime
from datetime import date

conn = sqlite3.connect('db.sqlite3') # datebase address
cur = conn.cursor()

# get data from API
r = requests.get('http://api.douban.com/v2/movie/in_theaters?start=0&count=100')
json_str = r.text
data = json.loads(json_str)

#get subject_id thus already in datebase
cur.execute("select * from history_subject")
saved_data = []
ids = []
for row in cur:
    ids.append(row[0])

new_subject = []
tz = pytz.timezone('Asia/Shanghai')
today = datetime.datetime.now(tz).date().isoformat()
strip_jpg = re.compile("\.jpg")

# daily rank according to sort of data from douban API
rank = 0
for i in data['subjects']:
	history_rating = dict()
	title = i['title']
	original_title = i['original_title']
	sub_id = i['id']
	rating = i['rating']['average']
	image = i['images']['large']
	image = re.sub(strip_jpg, ".webp", image)
	_id = sub_id

	# update old subject
	if int(i['id']) in ids:
		cur.execute("select update_date, history_rating from history_subject where id=?", [(int(i['id']))])
		check_data = cur.fetchall()
		update_date = check_data[0][0]
		history_rating = check_data[0][1]
		if today != update_date:
			history_rating = json.loads(history_rating)
			history_rating[today] = rating
			print(history_rating)
			temp = sorted(history_rating.items(), key=lambda d:d[0], reverse=False)
			new_rating = collections.OrderedDict()
			for i in temp:
				new_rating[i[0]] = i[1]
			print(new_rating)
			history_rating = json.dumps(new_rating)
			update_subject = (today, history_rating, rank,int(sub_id))
			cur.execute("update history_subject set update_date=?, history_rating=?, daily_rank=?, playing = 1 where id=?", update_subject)
			print('done')
		
	# new subject
	else:
		playing = 1
		pub_date = today
		created_date = today
		update_date = created_date
		history_rating[pub_date] = rating
		history_rating = json.dumps(history_rating)
		subject = (_id, title, original_title, sub_id, rating, history_rating, playing, pub_date, created_date, update_date, image, rank)
		# print(subject)
		new_subject.append(subject)
	rank += 1

# commit new subject
cur.executemany('insert into history_subject values(?,?,?,?,?,?,?,?,?,?,?,?)', new_subject)
conn.commit()

# set stop playing film 
cur.execute("update history_subject set playing = 0, daily_rank = -1 where update_date != ?",(today,))
conn.commit()

# download poster
cur.execute("select id, poster from history_subject")
for row in cur:
	id = row[0]
	try:
		temp = re.sub(strip_webp, ".jpg", row[1])
		pic = requests.get(temp)
	except:
		print('error')
		continue
	path =  '/home/syk/sites/doubanhistory/DoubanHistory/history/static/doubanhis/img/poster/'+str(id)+'.jpg'
	fp = open(path, 'wb')
	fp.write(pic.content)
	fp.close()

conn.close()
