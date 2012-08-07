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
	cur = db.cursor()
	cur.execute(sql)
	return cur

def main():
	pass

if __name__ == '__main__':
	main()
