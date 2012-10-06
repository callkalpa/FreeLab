import MySQLdb
import os
import datetime

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

# generates list to be used in preparing main report (patient information)
def get_main_report_list(patient_id):
	sql = "SELECT * FROM `patient` WHERE `patient_id`='" + patient_id + "'"
	tmp = execute_sql(sql).fetchone()
	t = str(datetime.datetime.now())
	date = t.split(' ')[0]
	time = t.split(' ')[1].split('.')[0]
	list_temp = 'Serial No:;' + str(tmp['patient_id']) + ';;#Name:;' + tmp['name'] + ';Date:;' + date + '#Sample Collected On:;' + str(tmp['sample_co']) + ';Time:;' + time + '#Requested By Doctor:;' + tmp['requested_bd'] + ';;'
	return list_temp

# retrives test data based on patient_id
def retrive_test_data(test_name, patient_id):
	sql = "SELECT * FROM `" + test_name + "` WHERE `patient_id`='" + patient_id + "'"
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

# returns the test display name of the desired test id
def get_test_display_name(test_id):
	sql = "SELECT `display_name` FROM test_info WHERE `test_id`='" + str(test_id) + "'"
	temp = execute_sql(sql).fetchone()['display_name']
	return temp

# returns the definition file of the desired test
def get_test_definition_file(test):
	sql ="SELECT `definition_file` FROM test_info WHERE `display_name`='" + test + "'"
	temp = execute_sql(sql).fetchone()['definition_file']
	return os.path.join('definition', temp) # definition is the directory of test definition files

# returns the gui file of the desired test
def get_test_gui_file(test):
	sql ="SELECT `gui_file` FROM test_info WHERE `display_name`='" + test + "'"
	temp = execute_sql(sql).fetchone()['gui_file']
	return os.path.join('gui', temp) # gui is the directory of the test gui files

def get_patient(patient_id):
	return_dic = {}
	sql_patient = "SELECT * FROM `patient` WHERE `patient_id`='" + str(patient_id) + "'"
	temp_patient = execute_sql(sql_patient).fetchone()
	if temp_patient != None:
		return_dic['patient'] = temp_patient
		sql_tests = "SELECT * FROM `main` WHERE `patient_id`='" + patient_id + "'"
		temp_tests = execute_sql(sql_tests).fetchall()

		return_dic['tests'] = temp_tests
		return return_dic

def update_data_entered(index):
	sql = "UPDATE main SET data_entered = '" + str(datetime.datetime.now()) + "' WHERE id=" + index
	execute_sql(sql)

# modifies text so that so that it is valid as a table/field name
def validate(text):
	return text.lower().replace(' ','_')

def main():
	pass

if __name__ == '__main__':
	main()
