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

class Handler:
	global builder
	global test_field
	global patient_id
	global index

	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def done(self, button):
		global values
		global index

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

		# calls sql insert command with test definition file name, fields and values
		db.feed_test_data(db.validate(builder.get_object('title').get_text()), values)

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


def main(test_gui_file, pat_id, ind):
	global builder
	global test_field
	global patient_id
	global index
	global values

	values = {}

	builder.add_from_file(test_gui_file)
	builder.connect_signals(Handler())

	window = builder.get_object("main")
	window.show_all()
	
	test_definition_file = builder.get_object('test_filename').get_text()
	test_field = test_fields.TestField(test_definition_file)
	
	patient_id = pat_id
	index = ind

	Gtk.main()

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2], sys.argv[3]) # test definition file, patient_id, index

