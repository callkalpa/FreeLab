import sys
from pyjon.reports import ReportFactory

output = []
fields_list = []
REPORT_WIDTH = 7.5 # in inches
REPORT_HEIGHT = 0

# generates the report of the given file with given data (data is a list)
def generate_report(fi, data):
	global output
	global fields_list

	f = open(fi,'r')

	temp = []

	for line in f.readlines():
		temp.append(line.replace('\n',''))
	
	f.close()

	# prepare fields list
	fields_list = temp[1:]
	increase_report_height(0.25 * len(fields_list))

	if len(temp) > 2:
		output.append(get_title(temp[0]))
	
	output.append(get_fields(temp[1:]))

	write_xml()

def increase_report_height(height):
	global REPORT_HEIGHT
	REPORT_HEIGHT += height

# title of the test (for tests with multiple fields)
def get_title(title):
	increase_report_height(0.75)
	return '<h1>' + title + '</h1>\n'

def get_fields(fields):
	temp = """<blockTable repeatRows="1" alignment="left" colWidths="40% 20% 20% 20%">
    <tr><td py:for="i in range(4)"></td></tr>
    <tr py:for="line in data"><td py:for="col in line.split(';')" py:content="col" /></tr>
  </blockTable>"""

	return temp

# writes the xml output of the report
def write_xml():
	global output
	global REPORT_WIDTH
	global REPORT_HEIGHT

	f = open('temp.xml','w')
	
	# header of the xml
	f.write('''<?xml version="1.0" encoding="iso-8859-1" standalone="no" ?>
<!DOCTYPE document SYSTEM "rml_1_0.dtd">
<document xmlns:py="http://genshi.edgewall.org/">
<template leftMargin="0.5in" rightMargin="0.5in" showBoundary="1" pageSize="A3">
  <pageTemplate id="main">
    <frame id="first" x1="0.5in" y1="0.5in" width="''' + str(REPORT_WIDTH) + '''in" height="''' + str(REPORT_HEIGHT) + '''in" showBoundary="1"/>
  </pageTemplate>
</template>
<stylesheet>
</stylesheet>
<story>''')

	# write title and fields
	temp = ''

	for line in output:
		temp += line

	f.write(temp)

	# footer of the xml
	f.write("""</story>
</document>
""")

	f.close()
	
	write_pdf('temp.xml')

def write_pdf(fi):
	factory = ReportFactory()
	factory.render_template(template_file=fi, data=fields_list)

	factory.render_document('test.pdf')
	factory.cleanup()
	
def main():
	generate_report(sys.argv[1], '')

if __name__ == '__main__':
	main()
