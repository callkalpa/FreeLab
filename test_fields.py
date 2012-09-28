# reads the test definition files and return required lists of fields

import db

class TestField():
	output = []

	def __init__(self, test_definition_file):
		self.output = []
		f = open(test_definition_file,'r')
		
		for line in f.readlines():
			self.output.append(line.replace('\n',''))

	# return the list of fields including the test name
	def get_test_name_and_fields(self):
		return self.output
#		l = len(self.output)
#		return self.output[:l/2]

	# return test name
	def get_test_name(self):
		return self.output[0]

	# return the list of fields required for gui
	def get_gui_field_list(self):
		temp = []
		for field in self.output[1:]:
			temp.append(db.validate(field.split(';')[0]))
		
		return temp

	def get_calculation(self, field):
		for f in self.output:
			if db.validate(f.split(';')[0]) == field:
				return f.split(';')[1][2:-1] # return without the paranthesis and field type
