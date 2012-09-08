import db
import sys
import report
import os
import test_fields

# quries the database and generates the report
def gen_report(test_definition_file, patient_id):
	temp = test_fields.TestField(test_definition_file)
	test_name = db.validate(temp.get_test_name())

	cur = db.retrive_test_data(test_name, patient_id)
	data = cur.fetchone()
	rep = report.Report(test_definition_file, data)
	rep.generate_report()

if __name__ == '__main__':
	gen_report(sys.argv[1], sys.argv[2])
