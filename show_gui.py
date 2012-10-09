# displays the gui of the specified test

from gi.repository import Gtk
import sys
import db
import test_fields
import datetime
import re

builder = Gtk.Builder()

test_field = None
values = {} # to hold the field names and values to be fed into the table
patient_id = None
index = None
data_entered = None # used to store the dictionary of data in case there are previous data

class Handler:
	global builder
	global test_field
	global patient_id
	global index
	global data_entered

	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def done(self, button):
		global values
		global index
		global data_entered

		fields = test_field.get_gui_field_list()
		
		values['`id`'] = '0' # auto increment value
		values['`patient_id`'] = "'" + str(patient_id) + "'"

		for field in fields:
			obj =  builder.get_object(field)

			key = '`' + field + '`'			

			if obj == None:
				# calculation field
				values[key] = "'" + str(get_calculation_result(field)) + "'" # result of the calculation 
				continue

			object_type = obj.get_name()
			
			if object_type == 'GtkEntry':
				values[key] = "'" + get_gtkEntry_value(obj) + "'"
			elif object_type == 'GtkTextView':
				values[key] = "'" + get_gtkTextView_value(obj) + "'"
			elif object_type == 'GtkComboBoxText':
				values[key] = "'" + get_gtkComboBoxText_value(obj) + "'"

		# if there are preiously entered data do an update, else do an insert
		if data_entered is None:
			db.feed_test_data(db.validate(builder.get_object('title').get_text()), values)
		else:
			db.update_test_data(db.validate(builder.get_object('title').get_text()), values, data_entered['id'])

		# update the data entered field of main table
		db.update_data_entered(index)

		# close the window
		self.window.destroy()

def get_calculation_result(field):
	global test_field
	global values

	cal = test_field.get_calculation(field)
	
	# split by '(' and ')' and arthmetic operators, +, -, / and
	pattern = re.compile(r"[+-/*()]")
	temp = pattern.split(cal)
	
	# replace fields in the calculation with values
	for t in temp:
		tem = "`" + db.validate(t.strip()) + "`"
		if tem in values.keys():
			val = float(values[tem].strip().replace("'","")) # convert to float for possible decimal calculations
			cal = cal.replace(t, str(val))

	return eval(cal)

def get_gtkEntry_value(obj):
	return obj.get_text()

def get_gtkTextView_value(obj):
	buf = obj.get_buffer()
	return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)

def get_gtkComboBoxText_value(obj):
	temp = obj.get_active_text()
	if temp == None:
		return ''
	return temp

def set_gtkEntry_value(obj, value):
	obj.set_text(str(value))

def set_gtkTextView_value(obj, value):
	help(obj)
	obj.set_buffer(str(value))

def set_gtkComboBoxText_value(obj, value):
	#help(obj)
	model = obj.get_model()
	print type(model)
	help(model)
	#obj.set_active(str(value))
	model.set_active(str(value))

# displays previous data in the gui
def display_previous_data():
	global test_field
	global data_entered

	fields = test_field.get_gui_field_list()
		
	for field in fields:
		obj =  builder.get_object(field)

		if obj is not None:
			key = "'" + field + "'"			
			object_type = obj.get_name()
			value = data_entered[field]
			if object_type == 'GtkEntry':
				set_gtkEntry_value(obj, value)
			elif object_type == 'GtkTextView':
				set_gtkTextView_value(obj, value)
			elif object_type == 'GtkComboBoxText':
				set_gtkComboBoxText_value(obj, value)


def main(test_gui_file, pat_id, ind, data_enter):
	global builder
	global test_field
	global patient_id
	global index
	global values
	global data_entered
	
	values = {}

	builder.add_from_file(test_gui_file)
	builder.connect_signals(Handler())

	window = builder.get_object("main")
	window.show_all()
	
	test_definition_file = builder.get_object('test_filename').get_text()
	test_field = test_fields.TestField(test_definition_file)
	
	patient_id = pat_id
	index = ind
	data_entered = data_enter
	
	if data_entered is not None:
		display_previous_data()

	Gtk.main()

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2], sys.argv[3]) # test definition file, patient_id, index

