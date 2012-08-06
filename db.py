
DBFILE='db.config'
settings = {}

def read_config_file():
	f = open(DBFILE,'r')
	

	for line in f.readlines():
		temp = line.replace('\n','').split(':')
		settings[temp[0]] = temp[1]

	f.close()

def get_connection_string():
	read_config_file()
	# return with the single quotes trimmed
	return (','.join(["%s=%s" %(k,v) for k,v in settings.items()]))[1:-1]

def get_database():
	read_config_file()
	return settings['db']
	
def get_connection_string2():
	f = open(DBFILE,'r')
	
	temp = []
	
	for line in f.readlines():
		temp.append(line.replace('\n',''))

	f.close()
	return ','.join(temp)

def main():
	read_config_file()
	get_database()

if __name__ == '__main__':
	main()
