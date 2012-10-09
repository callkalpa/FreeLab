# displays the main window

from gi.repository import Gtk
import sys
import db
import datetime
import re
import os
import show_gui
import sys
import generate_report
import add_patient
import webbrowser

builder = Gtk.Builder()
patient_id = ''
test_list_data = Gtk.ListStore(str, str, str, str) # test name, data entered data, printed data, index

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
		sys.exit(0)

	def print_all(self, button):
		if len(test_list_data) > 0:
			gui_test_list_selection.select_all()
			self.generate_report()
			# print statement should go here

	def print_selected(self, button):
		self.generate_report()
		# print statement should go here

	def preview(self, button):
		if len(test_list_data) > 0:
			gui_test_list_selection.select_all()
			self.generate_report()
			# views the pdf in system default pdf viewer
			webbrowser.open('test.pdf')

	def enter_data(self, button):
		global patient_id
		model, rows = gui_test_list.get_selection().get_selected_rows()
		for row in rows:
			iter = model.get_iter(row)
			test_name = model.get_value(iter, 0)
			test_gui_file = db.get_test_gui_file(test_name)
			index = model.get_value(iter, 3)
			
			# check whether data is already entered, is so pass the dictionary containing data
			data_entered = None
			if model.get_value(iter, 1) != '':
				data_entered = db.retrive_test_data(db.get_test_table_name(test_name), patient_id) # test_gui_file contains the test table name and .glade
			
			show_gui.main(test_gui_file, patient_id, index, data_entered)
			self.search(button)
		#if row != None:
		#	test_gui_file = db.get_test_gui_file(model[row][0])
		#	index = model[row][3]
		#	show_gui.main(test_gui_file, patient_id, index)
		#	self.search(button)

	def add_patient(self, button):
		add_patient.main()

	def search(self, button):
		global patient_id
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
				# append data entered and printed
				if test['data_entered'] != None:
					tmp.append(str(test['data_entered']))
				else:
					tmp.append('')
				if test['printed'] != None:
					tmp.append(str(test['printed']))
				else:
					tmp.append('')
				
				# append index
				tmp.append(str(test['id']))

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

	def generate_report(self):
		model, rows = gui_test_list.get_selection().get_selected_rows()
		test_definition_files = []
		for row in rows:
			iter = model.get_iter(row)
			if model.get_value(iter, 1) != '':
				test_definition_files.append(db.get_test_definition_file(model.get_value(iter, 0)))
		# generates the report
		generate_report.gen_report(patient_id, test_definition_files)

def main():
	global builder
	global test_list_data
	
	global gui_name
	global gui_sample_co
	global gui_requested_bd
	global gui_billed_by
	global gui_test_list
	global gui_test_list_selection

	builder.add_from_file(os.path.join('gui', 'main.glade'))
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
	# tests
	test_renderer = Gtk.CellRendererText()
	test_column = Gtk.TreeViewColumn('Test', test_renderer, text = 0)
	gui_test_list.append_column(test_column)
	# data entered
	data_renderer = Gtk.CellRendererText()
	data_column = Gtk.TreeViewColumn('Data Entered', data_renderer, text = 1)
	gui_test_list.append_column(data_column)
	# printed
	print_renderer = Gtk.CellRendererText()
	print_column = Gtk.TreeViewColumn('Printed', print_renderer, text = 2)
	gui_test_list.append_column(print_column)
	# index 
	index_renderer = Gtk.CellRendererText()
	index_column = Gtk.TreeViewColumn('Index', index_renderer, text = 3)
	gui_test_list.append_column(index_column)
	
	gui_test_list.set_model(test_list_data)
	
	Gtk.main()

if __name__ == '__main__':
	main()

