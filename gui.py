import db

xml_output=''
random_id = 1 # used to generate id's for labels, buttons etc
XPAD = 10

def get_xml_header(id):
	temp = """<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <!-- interface-requires gtk+ 3.0 -->
  <object class="GtkWindow" id=\"""" + id + """\">
    <property name="can_focus">False</property>
    <child>
      <object class="GtkGrid" id="grid1">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="row_spacing">10</property>
        <property name="column_spacing">5</property>
        <property name="row_homogeneous">True</property>"""

	return temp

def get_xml_footer():
	temp = """
      </object>
    </child>
  </object>
</interface>"""
		

	return temp
# returns the xml corresponding to a row of a test
def get_row_xml(fields):
	global random_id

	temp = ''
	i = 0

	for row in fields:
		t = row.split(';')
		id = db.validate(t[0])
		name = t[0]
		test_type = t[1]
		unit = t[2]
		reference_range = t[3]
	

		# input field
		items = ''
		if test_type == 'A': # text area
			object_class = 'GtkTextView'
		elif test_type[0] == 'T' and len(test_type)>1 and test_type[1] == '[': # combo box
			object_class = 'GtkComboBoxText'
			items = """
            <property name="entry_text_column">0</property>
            <property name="id_column">1</property>
            <items>"""
			its = test_type[2:-1].split(',') # get items to be inserted to the combo box
			for item in its:
				items = items + """
              <item translatable="yes">""" + item.strip() + """</item>"""

			items = items + """
            </items>"""
		elif len(test_type)>1 and test_type[1] == '(': # calculation field, just ignore it
			continue
		else: # text field
			object_class = 'GtkEntry'


		temp = temp + """
	<child>
	  <object class=\"""" + object_class + """\" id=\"""" + id + """\">
	    <property name="visible">True</property>
            <property name="can_focus">True</property>
		""" + items + """
          </object>
          <packing>
            <property name="left_attach">1</property>
            <property name="top_attach">""" + str(i) + """</property>
            <property name="width">1</property>
            <property name="height">1</property>
          </packing>
        </child>"""
		
		# test name
		# label was moved here so that calculation field labels are not added
		temp = temp + get_label(name, i, 0)		
		
		# unit
		if unit != '':
			temp = temp + get_label(unit, i, 2)

		# reference range
		if reference_range != '':
			temp = temp + get_label(reference_range, i, 3)

		i = i + 1

	# done button
	temp = temp + """
	<child>
          <object class="GtkButton" id="button""" + str(random_id) + """\">
            <property name="label" translatable="yes">Done</property>
            <property name="use_action_appearance">False</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
            <property name="use_action_appearance">False</property>
          </object>
          <packing>
            <property name="left_attach">3</property>
            <property name="top_attach">""" + str(i) + """</property>
            <property name="width">1</property>
            <property name="height">1</property>
          </packing>
        </child>"""

	random_id = random_id + 1


	return str(temp)

def get_label(value, row, column):

	global random_id

	temp = """
	<child>
          <object class="GtkLabel" id="label""" + str(random_id) + """\">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="xalign">0</property>
            <property name="xpad">""" + str(XPAD) + """</property>
            <property name="label" translatable="yes">""" + value + """</property>
          </object>
          <packing>
            <property name="left_attach">""" + str(column) + """</property>
            <property name="top_attach">""" + str(row) + """</property>
            <property name="width">1</property>
            <property name="height">1</property>
          </packing>
        </child>"""
	random_id = random_id + 1

	return temp		

# returns the xml of glade, when the list of fields is passed
def get_glade(data):

	xml_output = get_xml_header(db.validate(data[0]))
	
	xml_output = xml_output + get_row_xml(data[1:])

	xml_output = xml_output + get_xml_footer()

	return xml_output
	

def main():
	pass

if __name__ == '__main__':
	main()
