import MySQLdb

DBFILE='db.config'
settings = {}

def read_config_file():
	f = open(DBFILE,'r')
	
	for line in f.readlines():
		temp = line.replace('\n','').split(':')
		settings[temp[0]] = temp[1]

	f.close()

def get_database():
	read_config_file()
	return settings['db']
	
def execute_sql(sql):
	read_config_file()
	db = MySQLdb.connect(**settings)
	db.autocommit(True)
	cur = db.cursor(MySQLdb.cursors.DictCursor)
	cur.execute(sql)
	return cur

# insert command to table to insert test data, patient info
def feed_test_data(test_name, values):
	sql = 'INSERT INTO `' + test_name + '` (' + (','.join(values.keys())) + ') VALUES (' + (','.join(values.values())) + ')'
	execute_sql(sql)

# retrives test data based on patient_id
def retrive_test_data(test_name, patient_id):
	sql = 'SELECT * FROM `' + test_name + '` WHERE `patient_id`=' + patient_id
	return execute_sql(sql)

# returns a list of tests available (Display names)
def get_tests_list():
	sql = 'SELECT `display_name` FROM test_info ORDER BY `display_name`'
	temp = execute_sql(sql)
	test_list = []
	for test in temp.fetchall():
		test_list.append(test['display_name'])
	return test_list

# returns the test id of the desired test
def get_test_id(test):
	sql ="SELECT `test_id` FROM test_info WHERE `display_name`='" + test + "'"
	temp = execute_sql(sql).fetchone()['test_id']
	return temp

# modifies text so that so that it is valid as a table/field name
def validate(text):
	return text.lower().replace(' ','_')

def main():
	pass

if __name__ == '__main__':
	main()
