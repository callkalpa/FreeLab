# This script generates the mysql table, user interface and the report for the specified test definition files

import sys
import db
import gui
import os
import test_fields

GUI_DIR='gui'

test_definition_file = '' # file name of the test definition

def decode_test_definition(fi):
	global data
	global test_definition_file
	test_definition_file = fi
	data = test_fields.get_table_field_list(fi)

# start of report section

def check_for_report():
	return True

def generate_report():
	pass

# end of report section

# start of gui section

def check_for_gui():
	return False

def generate_gui():
	global data
	f = open(os.path.join(GUI_DIR, db.validate(data[0])+ '.glade'), 'w')
	f.write(gui.get_glade(data, test_definition_file))
	f.flush()
	f.close()

# end of gui section

# start of database section

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
		return 'VARCHAR(20)'
	if value is 'I':
		return 'INT'
	if value is 'F':
		return 'FLOAT'
	if value is 'A':
		return 'VARCHAR(50)'	

def generate_table():
	sql = ('CREATE TABLE `' + db.validate(data[0]) + '` (\n' + 
	'`id` INT NOT NULL AUTO_INCREMENT,\n' +
  	'`patient_id` VARCHAR(12) NULL ,\n')

	for test in data[1:]:
		tmp = test.split(';')
		test_name = db.validate(tmp[0])
		value = get_table_field(tmp[1][0])
		sql = sql + '`' + test_name + '` ' + value + ' NULL , \n'


	sql = sql + ('`user` VARCHAR(2) NULL , \n'
	'`time_stamp` TIMESTAMP NULL, \n'
	'PRIMARY KEY (`id`))')


	db.execute_sql(sql)
	print '\'' + data[0] + '\' table created'

# end of database section

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
