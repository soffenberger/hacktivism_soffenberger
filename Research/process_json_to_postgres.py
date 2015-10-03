#! /usr/bin/python 
#
# Script to shred the JSON from Tweet Tracker and put onto a local postgres instance
#
#

import psycopg2
import json
import sys
import traceback

def parse_json():
	file_name = sys.argv[1]
	data = []
	b=0
	with open(file_name) as data_file:
		for line in data_file:
			try:
				data.append(json.loads(line))
				if data[b]["cat"] == 2 or data[b]["cat"] == 7:
					data.pop(b)
				else:
					b+=1
			except ValueError:
				print b
	return data
	
def put_in_users (data, a):
	global cur
	cur.execute("""SELECT screen_name FROM users where screen_name = '%s'""" %data[a]["user"]["screen_name"])
	name = cur.fetchone()
	if name:
		print("Skipping user")
	else:
		cur.execute("""Insert Into %s Values (DEFAULT, '%s',%s, '%s', %s);""" %('users', data[a]["user"]["screen_name"], data[a]["user"]["followers_count"], data[a]["user"]["location"].replace("'","''"), data[a]["user"]["verified"]))

def put_in_tweets (data, a):
	key_wd = ''
	hash_tag = ''
	symbols = ''
	trends = ''
	expanded_url = ''
	usr_mentions = ''
	user_id = get_user_id(data[a]["user"]["screen_name"])
	length = len(data[a]["keywords"])		
	for i in range(length):
		key_wd += data[a]["keywords"][i] + ','
	if data[a]["entities"]["hashtags"]:
		length = len(data[a]["entities"]["hashtags"])
		for i in range(length):
			hash_tag += data[a]["entities"]["hashtags"][i]["text"] + ','
	if data[a]["entities"]["symbols"]:
		data[a]["entities"]["symbols"]=''
		#length = len(data[a]["entities"]["symbols"])
		#for i in range(length):
#			symbols += str(data[a]["entities"]["symbols"][i]) + ','
	if data[a]["entities"]["user_mentions"]:
		length = len(data[a]["entities"]["user_mentions"])
		for i in range(length):
			usr_mentions += data[a]["entities"]["user_mentions"][i]["screen_name"] + ','
	if data[a]["entities"]["trends"]:
		length = len(data[a]["entities"]["trends"])
		for i in range(length):
			trends += data[a]["entities"]["trends"][i] + ','
		
	global cur
	try:
		if data[a]["cat"] == 1: 
			cur.execute("""INSERT INTO {0} VALUES (DEFAULT ,'{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7}, '{8}', '{9}', '{10}');""" .format( 'haters1', data[a]["user"]["screen_name"], data[a]["created_at"], data[a]["text"].replace("'","''").encode('utf-8'), hash_tag.encode('utf-8'), symbols.encode('utf-8'), trends.encode('utf-8'), user_id[0], usr_mentions, key_wd.replace("'","''").encode('utf-8'), data[a]["lang"]))
		elif data[a]["cat"] == 2: 
			cur.execute("""INSERT INTO {0} VALUES (DEFAULT ,'{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7}, '{8}', '{9}', '{10}');""" .format( 'anonymous', data[a]["user"]["screen_name"], data[a]["created_at"], data[a]["text"].replace("'","''").encode('utf-8'), hash_tag.encode('utf-8'), symbols.encode('utf-8'), trends.encode('utf-8'), user_id[0], usr_mentions, key_wd.replace("'","''").encode('utf-8'), data[a]["lang"]))
		elif data[a]["cat"] == 3: 
			cur.execute("""INSERT INTO {0} VALUES (DEFAULT ,'{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7}, '{8}', '{9}', '{10}');""" .format( 'nashi', data[a]["user"]["screen_name"], data[a]["created_at"], data[a]["text"].replace("'","''").encode('utf-8'), hash_tag.encode('utf-8'), symbols.encode('utf-8'), trends.encode('utf-8'), user_id[0], usr_mentions, key_wd.replace("'","''").encode('utf-8'), data[a]["lang"]))
		elif data[a]["cat"] == 4: 
			cur.execute("""INSERT INTO {0} VALUES (DEFAULT ,'{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7}, '{8}', '{9}', '{10}');""" .format( 'russia', data[a]["user"]["screen_name"], data[a]["created_at"], data[a]["text"].replace("'","''").encode('utf-8'), hash_tag.encode('utf-8'), symbols.encode('utf-8'), trends.encode('utf-8'), user_id[0], usr_mentions, key_wd.replace("'","''").encode('utf-8'), data[a]["lang"]))
		elif data[a]["cat"] == 5: 
			cur.execute("""INSERT INTO {0} VALUES (DEFAULT ,'{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7}, '{8}', '{9}', '{10}');""" .format( 'lizard_squad', data[a]["user"]["screen_name"], data[a]["created_at"], data[a]["text"].replace("'","''").encode('utf-8'), hash_tag.encode('utf-8'), symbols.encode('utf-8'), trends.encode('utf-8'), user_id[0], usr_mentions, key_wd.replace("'","''").encode('utf-8'), data[a]["lang"]))
		elif data[a]["cat"] == 6: 
			cur.execute("""INSERT INTO {0} VALUES (DEFAULT ,'{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7}, '{8}', '{9}', '{10}');""" .format( 'haters2', data[a]["user"]["screen_name"], data[a]["created_at"], data[a]["text"].replace("'","''").encode('utf-8'), hash_tag.encode('utf-8'), symbols.encode('utf-8'), trends.encode('utf-8'), user_id[0], usr_mentions, key_wd.replace("'","''").encode('utf-8'), data[a]["lang"]))
		elif data[a]["cat"] == 7: 
			cur.execute("""INSERT INTO {0} VALUES (DEFAULT ,'{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7}, '{8}', '{9}', '{10}');""" .format( 'haters3', data[a]["user"]["screen_name"], data[a]["created_at"], data[a]["text"].replace("'","''").encode('utf-8'), hash_tag.encode('utf-8'), symbols.encode('utf-8'), trends.encode('utf-8'), user_id[0], usr_mentions, key_wd.replace("'","''").encode('utf-8'), data[a]["lang"]))
	except:
		pass
		print(traceback.format_exc())
		print("Can't add tweet")

def get_user_id(user_name):
	global cur
	cur.execute("""SELECT user_id FROM %s WHERE screen_name = '%s';""" % ('users', user_name))
	user_id = cur.fetchone()
	return user_id
		

def main():
	data = parse_json()
	conn = psycopg2.connect("dbname =  '%s'" %sys.argv[2])
	global cur 
	cur = conn.cursor()
	for a in range(50000):
		user_id= 0
		try:	
			put_in_users (data, a)	
			put_in_tweets (data, a)
			print("Record Added")
	
		except IndexError:
			print(traceback.format_exc()) 
			print("Done")
			break
	conn.commit()
	cur.close()
	conn.close()




if __name__ == "__main__":
	main()
