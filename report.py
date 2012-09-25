import sys
import db
import test_fields
from pyjon.reports import ReportFactory


# generates the report of the given file with given data (data is a dictionary)
class Report:

	output = []
	fields_list = []
	# all units are in points
	PAGE_WIDTH = 595
	PAGE_HEIGHT = 842
	LEFT_MARGIN = 36
	RIGHT_MARGIN = 36
	TOP_MARGIN = 36
	BOTTOM_MARGIN = 0
	FRAME_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN # in points (7.5 in inches)
	FRAME_HEIGHT = 0
	CURRENT_Y_AXIS = PAGE_HEIGHT - TOP_MARGIN # this holds the y coordinate for the next frame

	test_field = None

	data = {} # holds the dict with test results

	def generate_report(self):
		temp_from_definition = self.test_field.get_test_name_and_fields() # fields read from the test definition file (no test result values)

		# replace field type with values and prepare fields list
		for t in temp_from_definition[1:]:
			tem = t.split(';')
			tem[1] = str(self.data[db.validate(tem[0])])
			self.fields_list.append(';'.join(tem))

		self.increase_report_height(24 * len(self.fields_list))

		if len(self.fields_list) > 1:
			self.output.append(self.get_title(temp_from_definition[0]))
	
		self.output.append(self.get_fields(self.fields_list))

		self.CURRENT_Y_AXIS = self.CURRENT_Y_AXIS - self.FRAME_HEIGHT
		self.write_xml()
		self.FRAME_HEIGHT = 0

	def increase_report_height(self, height):
		self.FRAME_HEIGHT += height

	# title of the test (for tests with multiple fields)
	def get_title(self, title):
		self.increase_report_height(28) # title in 14p
		return '<para style="report_title">' + title + '</para>\n'

	def get_fields(self, fields):
		temp = """<blockTable style="fields" repeatRows="1" alignment="left" colWidths="234 140.4 46.8 46.8">
	    <tr><td py:for="i in range(4)"></td></tr>
	    <tr py:for="line in data"><td py:for="col in line.split(';')" py:content="col" /></tr>
	  </blockTable>"""

		return temp
	
	# writes the xml output of the report
	def write_xml(self):

		f = open('temp.xml','w')
	
		# header of the xml
		f.write('''<?xml version="1.0" encoding="iso-8859-1" standalone="no" ?>
	<!DOCTYPE document SYSTEM "rml_1_0.dtd">
	<document xmlns:py="http://genshi.edgewall.org/" filename="test.pdf" compression="true">
	<docinit>
		<registerTTFont faceName="Garamond" fileName="font/Garamond.ttf"/>
		<registerTTFont faceName="Garamond-bold" fileName="font/Garamonb.ttf"/>
	</docinit>
	<template pageSize="(''' + str(self.PAGE_WIDTH) + ''',''' + str(self.PAGE_HEIGHT) + ''')" leftMargin="''' + str(self.LEFT_MARGIN)  + '''" rightMargin="''' + str(self.RIGHT_MARGIN)  + '''" showBoundary="0">
	  <pageTemplate id="main">
	    <frame id="first" x1="0.5in" y1="''' + str(self.CURRENT_Y_AXIS)  + '''" width="''' + str(self.FRAME_WIDTH) + '''" height="''' + str(self.FRAME_HEIGHT) + '''" showBoundary="1"/>
	  </pageTemplate>
	</template>
	<stylesheet>
		<paraStyle name="report_title" fontName="Garamond-bold" fontSize="14"/>
		<blockTableStyle id="fields">
			<blockFont name="Garamond" size="12" start="0,0" stop="-1,-1"/>
			<blockFont name="Garamond-bold" size="12" start="1,1" stop="1,-1" />
		</blockTableStyle>
	</stylesheet>
	<story>''')

		# write title and fields
		temp = ''

		for line in self.output:
			temp += line

		f.write(temp)

		# footer of the xml
		f.write("""</story>
	</document>
	""")

		f.close()
	
		self.write_pdf('temp.xml')

	def write_pdf(self, fi):
		factory = ReportFactory()
		factory.render_template(template_file=fi, data=self.fields_list)

		factory.render_document('test.pdf')
		factory.cleanup()
	
	def __init__(self, test_definition_file, data):
		self.test_field = test_fields.TestField(test_definition_file)
		self.data = data

