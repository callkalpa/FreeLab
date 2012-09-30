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

class Handler:
	global builder
	global test_list_data
	global selected_tests
	global test_li

	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def remove_selected_tests(self, *args):
		model, rows = builder.get_object('test_list').get_selection().get_selected_rows()
		for row in rows:
			iter = model.get_iter(row)
			# removes the test from test_li
			test_li.remove(model.get_value(iter, 0))
			test_list_data.remove(iter)

	def add_test(self, button):
		test = builder.get_object('tests').get_active_text()
		
		if test is not None and test not in test_li:
			tmp = []
			tmp.append(test)
			test_list_data.append(tmp)
			test_li.append(test)

	def add_patient(self, button):
		# insert in to patient table
		patient = {}
		patient['`id`'] = '0'
		patient['`patient_id`'] = "'" + str(builder.get_object('patient_id').get_text()) + "'"
		patient['`name`'] = "'" + builder.get_object('name').get_text() + "'"
		patient['`requested_bd`'] = "'" + builder.get_object('requested_bd').get_text() + "'"
		patient['`sample_co`'] = "'" + builder.get_object('sample_co').get_text() + "'"
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
	
	builder.add_from_file('gui/add_patient.glade')
	builder.connect_signals(Handler())

	window = builder.get_object("main")
	window.show_all()

	# populate tests combo box
	for test in db.get_tests_list():
		builder.get_object('tests').append_text(test)

	# prepare list view
	renderer = Gtk.CellRendererText()
	column = Gtk.TreeViewColumn('Tests', renderer, text = 0)
	test_list = builder.get_object('test_list')
	test_list.set_model(test_list_data)
	test_list.append_column(column)
	
	Gtk.main()

if __name__ == '__main__':
	main()

