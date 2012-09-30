# displays the main window

from gi.repository import Gtk
import sys
import db
import datetime
import re

builder = Gtk.Builder()
patient_id = ''
test_list_data = Gtk.ListStore(str)

gui_name = None
gui_sample_co = None
gui_requested_bd = None
gui_billed_by = None
gui_test_list = None
gui_test_list_selection = None

class Handler:
	global builder
	global test_list_data
	global patient_id

	global gui_name
	global gui_sample_co
	global gui_requested_bd
	global gui_billed_by
	global gui_test_list
	global gui_test_list_selection


	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

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

	def search(self, button):
		tmp = builder.get_object('patient_id').get_text()
		patient_info = db.get_patient(tmp)
		if patient_info != None:
			patient_id = tmp

			# display patient information
			patient = patient_info['patient']
			gui_name.set_text(patient['name'])
			gui_sample_co.set_text(str(patient['sample_co']))
			gui_requested_bd.set_text(patient['requested_bd'])
			gui_billed_by.set_text(patient['billed_by'])

			# display tests
			test_list_data.clear()
			tests = patient_info['tests']
			for test in tests:
				tmp = []
				tmp.append(db.get_test_display_name(test['test_id']))
				test_list_data.append(tmp)

		else: # if the patient (patient_id) is not found
			self.clear_all()
		
	# clears all gui and tests list	
	def clear_all(self):
		patient_id = None
		gui_name.set_text('')
		gui_sample_co.set_text('')
		gui_requested_bd.set_text('')
		gui_billed_by.set_text('')
		test_list_data.clear()

def main():
	global builder
	global test_list_data
	
	global gui_name
	global gui_sample_co
	global gui_requested_bd
	global gui_billed_by
	global gui_test_list
	global gui_test_list_selection

	builder.add_from_file('gui/main.glade')
	builder.connect_signals(Handler())

	window = builder.get_object("main")
	window.show_all()
	
	# assign gui components
	gui_name = builder.get_object('name')
	gui_sample_co = builder.get_object('sample_co')
	gui_requested_bd = builder.get_object('requested_bd')
	gui_billed_by = builder.get_object('billed_by')
	gui_test_list = builder.get_object('test_list')
	gui_test_list_selection = builder.get_object('test_list_selection')

	# prepare list view
	test_renderer = Gtk.CellRendererText()
	test_column = Gtk.TreeViewColumn('Test', test_renderer, text = 0)
	gui_test_list.set_model(test_list_data)
	gui_test_list.append_column(test_column)
	
	Gtk.main()

if __name__ == '__main__':
	main()

