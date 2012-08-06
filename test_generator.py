# This script generates the mysql table, user interface and the report for the specified test definition files

import sys
import MySQLdb
from db import *

def connect_db():
	global cur
	db = MySQLdb.connect(host='localhost',user='freelab',passwd='freelab',db='freelab')
	#db = MySQLdb.connect(get_connection_string())
	cur = db.cursor()

def check_for_report():
	return True

def generate_report():
	pass

def check_for_gui():
	return True

def generate_gui():
	pass

def check_for_table():
	sql = 'SELECT COUNT(*) FROM information_schema.tables WHERE table_schema="[' + get_database() + ']" AND table_name="[' + data[0] + ']";'
	cur.execute(sql)
	
	if cur.fetchone()[0] > 0:
		return True;
	return False

def generate_table():
	pass

def decode_test_definition(fi):
	global data
	f = open(fi,'r')
	data = []

	for line in f.readlines():
		data.append(line.replace('\n',''))
	
	f.close()

	for a in data:
		print a

def main():
	connect_db()

	for fi in sys.argv[1:]:
		decode_test_definition(fi)

		if not check_for_table():
			generate_table()

		if not check_for_gui():
			generate_gui()

		if not check_for_report():
			generate_report()
			
if __name__ == '__main__':
	main()
