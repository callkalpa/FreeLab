# This script generates the mysql table, user interface and the report for the specified test definition files

import sys
import MySQLdb
from db import *

def connect_db():
	global cur
	db = MySQLdb.connect(host='localhost',user='freelab',passwd='freelab',db='freelab')
	cur = db.cursor()

def check_for_report(fi):
	return True

def generate_report(fi):
	pass

def check_for_gui(fi):
	return True

def generate_gui(fi):
	pass

def check_for_table(fi):
	return False

def generate_table(fi):
	pass

def main():
	connect_db()

	for fi in sys.argv[1:]:
		if not check_for_table(fi):
			generate_table(fi)

		if not check_for_gui(fi):
			generate_gui(fi)

		if not check_for_report(fi):
			generate_report(fi)
			
if __name__ == '__main__':
	main()
