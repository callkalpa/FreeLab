# displays the main window

from gi.repository import Gtk
import sys
import db
import datetime
import re

builder = Gtk.Builder()
patient_id = ''

class Handler:
	global builder
	global patient_id

	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def search():
		pass

	def add_patient():
		pass

	def add():
		pass

	def print_all():
		pass

	def print_selected():
		pass

	def preview():
		pass

	def done(self, button):
		global values
		fields = test_field.get_gui_field_list()

		values['`id`'] = '0' # auto increment value
		values['`time_stamp`'] = "'" + str(datetime.datetime.now()) + "'"

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

def main():
	global builder
	
	builder.add_from_file('gui/main.glade')
	builder.connect_signals(Handler())

	window = builder.get_object("main")
	window.show_all()
	
	Gtk.main()

if __name__ == '__main__':
	main()

