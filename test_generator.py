# This script generates the mysql table, user interface and the report for the specified test definition files

import sys
import db

def check_for_report():
	return True

def generate_report():
	pass

def check_for_gui():
	return True

def generate_gui():
	pass

def check_for_table():
	sql = 'SELECT COUNT(*) FROM information_schema.tables WHERE table_schema="' + db.get_database() + '" AND table_name="' + db.validate(data[0]) + '";'
	cur = db.execute_sql(sql)
	tmp = cur.fetchone()[0]
	if tmp > 0:
		print 'table \'' + data[0] + '\' already exists'
		return True;
	return False

# returns the appropriate sql table field type
def get_table_field(value):
	if value is 'T':
		return 'VARCHAR(12)'
	if value is 'I':
		return 'INT'
	if value is 'F':
		return 'FLOAT'
	if value is 'A':
		return 'VARCHAR(50)'	

def generate_table():
	sql = ('CREATE TABLE `' + db.validate(data[0]) + '` (\n' + 
	'`id` INT NOT NULL ,\n' +
  	'`patient_id` VARCHAR(12) NULL ,\n')

	for test in data[1:]:
		tmp = test.split(';')
		test_name = db.validate(tmp[0])
		value = get_table_field(tmp[1])
		sql = sql + '`' + test_name + '` ' + value + ' NULL , \n'


	sql = sql + ('`user` VARCHAR(2) NULL , \n'
	'`status` VARCHAR(10) NULL , \n'
	'`time_stamp` DATE NULL)')


	db.execute_sql(sql)
	print '\'' + data[0] + '\' table created'

def decode_test_definition(fi):
	global data
	f = open(fi,'r')
	data = []

	for line in f.readlines():
		data.append(line.replace('\n',''))
	
	f.close()

def main():
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
