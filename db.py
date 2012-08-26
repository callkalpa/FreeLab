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
	cur = db.cursor()
	cur.execute(sql)
	return cur

# insert command to table to insert test data
def feed_test_data(test_name, values):
	sql = 'INSERT INTO `' + test_name + '` (' + (','.join(values.keys())) + ') VALUES (' + (','.join(values.values())) + ')'
	print sql
	execute_sql(sql)

# modifies text so that so that it is valid as a table/field name
def validate(text):
	return text.lower().replace(' ','_')

def main():
	pass

if __name__ == '__main__':
	main()
