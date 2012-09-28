import db
import sys
import report
import os
import test_fields
import string
import common

# quries the database and generates the report
def gen_report(patient_id, test_definition_files):

	rep = report.Report()

	for test_definition_file in test_definition_files:
		temp = test_fields.TestField(test_definition_file)
		test_name = db.validate(temp.get_test_name())

		cur = db.retrive_test_data(test_name, patient_id)

		data = cur.fetchone()
		rep.set_test_info(test_definition_file, data)
		rep.generate_report()

	rep.write_xml()

if __name__ == '__main__':
	gen_report(sys.argv[1], sys.argv[2:])
