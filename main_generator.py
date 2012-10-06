# generates the patient, main, test_info sql tables

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
`name` VARCHAR(30) NULL,
`requested_bd` VARCHAR(30) NULL,
`sample_co` DATE NULL,
`billed_by` VARCHAR(10) NULL
)'''
	db.execute_sql(patient_sql)

	# create main table if it does not exist
	main_sql = '''CREATE TABLE IF NOT EXISTS `main`(
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
`patient_id` VARCHAR(10) NULL,
`test_id` INT NULL,
`data_entered` TIMESTAMP NULL,
`printed` TIMESTAMP NULL
)'''
	db.execute_sql(main_sql)

	# create test_info table
	test_info = ''' CREATE TABLE IF NOT EXISTS `test_info`(
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
`test_id` INT,
`display_name` VARCHAR(50) NULL,
`definition_file` VARCHAR(30) NULL,
`gui_file` VARCHAR(40) NULL
)'''	
	db.execute_sql(test_info)

if __name__ == '__main__':
	main()
