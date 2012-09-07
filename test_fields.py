# reads the test definition files and return required lists of fields

import db

class TestField():
	output = []

	def __init__(self, test_definition_file):
		#global output

		f = open(test_definition_file,'r')
	
		for line in f.readlines():
			self.output.append(line.replace('\n',''))

	# return the list of fields required for mysql table
	def get_table_field_list(self):
		return self.output

	# return the list of fields required for gui
	def get_gui_field_list(self):
		temp = []
		for field in self.output[1:]:
			temp.append(db.validate(field.split(';')[0]))
		
		print "TEST FIELDS"
		print temp
		return temp

	def get_calculation(self, field):
		for f in output:
			if f.split(';')[0] == field:
				return f.split(';')[1]
