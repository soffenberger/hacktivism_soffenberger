#! /usr/bin/python

import csv
import psycopg2
import sys


def parse_csv():
	data = []
	with open(sys.argv[1], 'rb') as csv_file:
		reader = csv.reader(csv_file)
		data= list(reader)
	return data

def main():
	data = parse_csv()
	data.pop(0)
	conn = psycopg2.connect("dbname =  '%s'" %sys.argv[2])
        cur = conn.cursor()
	cur.execute("""set datestyle to DMY;""")
	tags = '' 
	for a in data:
		cur.execute("""INSERT INTO {0} VALUES (DEFAULT ,'{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}');""" .format( sys.argv[3], a[1].replace("'","''"), a[2].replace("'","''"), a[3].replace("'","''"), a[4].replace("'","''"), a[5].replace("'","''"),  a[6].replace("'","''"), a[7].replace("'","''"), a[8].replace("'","''"), a[9].replace("'","''"),a[10].replace("'","''")))	
	conn.commit()
	cur.close()
	conn.close()
	print("done")


if __name__ == "__main__":
	main()
