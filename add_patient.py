# displays the gui to add patient

from gi.repository import Gtk
import sys
import db
import datetime
import re

builder = Gtk.Builder()
test_list_data = Gtk.ListStore(str)
selected_tests = [] # holds selected test to remove when requested
test_li = [] # used to avoid adding the same test twice

gui_patient_id = None
gui_name = None
gui_sample_co = None
gui_requested_bd = None
gui_tests = None
gui_test_list = None
gui_test_list_selection = None

class Handler:
	global builder
	global test_list_data
	global selected_tests
	global test_li

	global gui_patient_id
	global gui_name
	global gui_sample_co
	global gui_requested_bd
	global gui_tests
	global gui_test_list
	global gui_test_list_selection

	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def remove_selected_tests(self, *args):
		model, rows = gui_test_list.get_selection().get_selected_rows()
		for row in rows:
			iter = model.get_iter(row)
			# removes the test from test_li
			test_li.remove(model.get_value(iter, 0))
			test_list_data.remove(iter)

	def add_test(self, button):
		test = gui_tests.get_active_text()
		
		if test is not None and test not in test_li:
			tmp = []
			tmp.append(test)
			test_list_data.append(tmp)
			test_li.append(test)

	def add_patient(self, button):
		# insert in to patient table
		patient = {}
		patient['`id`'] = '0'
		patient['`patient_id`'] = "'" + str(gui_patient_id.get_text()) + "'"
		patient['`name`'] = "'" + gui_name.get_text() + "'"
		patient['`requested_bd`'] = "'" + gui_requested_bd.get_text() + "'"
		patient['`sample_co`'] = "'" + gui_sample_co.get_text() + "'"
		patient['`billed_by`'] = "'MANUAL'"

		# feed data to patient table
		db.feed_test_data('patient', patient)

		# insert tests into main table
		for test in test_list_data:
			main = {}
			main['`id`'] = '0'
			main['`patient_id`'] = patient['`patient_id`']
			main['`test_id`'] = "'" + str(db.get_test_id(test[0])) + "'"

			# feed data to main table
			db.feed_test_data('main', main)

def main():
	global builder
	global test_list_data
	
	global gui_patient_id
	global gui_name
	global gui_sample_co
	global gui_requested_bd
	global gui_tests
	global gui_test_list
	global gui_test_list_selection
	
	builder.add_from_file('gui/add_patient.glade')
	builder.connect_signals(Handler())

	window = builder.get_object("main")
	window.show_all()

	# assign gui components
	gui_patient_id = builder.get_object('patient_id')
	gui_name = builder.get_object('name')
	gui_sample_co = builder.get_object('sample_co')
	gui_requested_bd = builder.get_object('requested_bd')
	gui_tests = builder.get_object('tests')
	gui_test_list = builder.get_object('test_list')
	gui_test_list_selection = builder.get_object('test_list_selection')

	# populate tests combo box
	for test in db.get_tests_list():
		gui_tests.append_text(test)

	# prepare list view
	renderer = Gtk.CellRendererText()
	column = Gtk.TreeViewColumn('Tests', renderer, text = 0)
	gui_test_list.set_model(test_list_data)
	gui_test_list.append_column(column)
	
	Gtk.main()

if __name__ == '__main__':
	main()

