# generates the main, patient sql tables and main gui

import db

def main():
	create_tables()
	create_gui()

def create_gui():
	pass

def create_tables():
	# create patient table if it does not exist
	patient_sql = '''CREATE TABLE IF NOT EXISTS `patient`(
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
`patient_id` VARCHAR(10) NULL,
`name` VARCHAR(20) NULL,
`user` VARCHAR(10) NULL
)'''
	db.execute_sql(patient_sql)

	# create main table if it does not exist
	main_sql = '''CREATE TABLE IF NOT EXISTS `main`(
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
`patient_id` VARCHAR(10) NULL,
`requested_bd` VARCHAR(30) NULL,
`sample_co` DATE NULL,
`test_id` INT NULL,
`data_entered` TIMESTAMP NULL,
`printed` TIMESTAMP NULL
)'''
	db.execute_sql(main_sql)

if __name__ == '__main__':
	main()
