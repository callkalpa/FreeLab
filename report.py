import sys
from pyjon.reports import ReportFactory

output = []
fields_list = []

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

	if len(temp) > 2:
		output.append(get_title(temp[0]))
	
	output.append(get_fields(temp[1:]))

	write_xml()

# title of the test (for tests with multiple fields)
def get_title(title):
	return '<h1>' + title + '</h1>\n'

def get_fields(fields):
	temp = """<blockTable repeatRows="1">
    <tr><td py:for="i in range(4)">Kalpa ${i}</td></tr>
    <tr py:for="line in data"><td py:for="col in line.split(';')" py:content="col" /></tr>
  </blockTable>"""

	return temp

# writes the xml output of the report
def write_xml():
	global output

	f = open('temp.xml','w')
	
	# header of the xml
	f.write("""<?xml version="1.0" encoding="iso-8859-1" standalone="no" ?>
<!DOCTYPE document SYSTEM "rml_1_0.dtd">
<document xmlns:py="http://genshi.edgewall.org/">
<template pageSize="(595, 842)" leftMargin="72" showBoundary="0">
  <pageTemplate id="main">
    <frame id="first" x1="1in" y1="1in" width="6.27in" height="9.69in"/>
  </pageTemplate>
</template>
<stylesheet>
</stylesheet>
<story>""")

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
