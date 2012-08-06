FreeLab
=======

FreeLab is a software for printing medical reports in a laboratory

Format of the test definition file
----------------------------------

Test Name
Test Name;Value;Unit;Reference Range
Test Name;Value;Unit;Reference Range

Here Value is whether it is a text, integer, float or a large text (text area).

T-Text
I-Integer
F-Float
A-Large Text

Sample test definition file
---------------------------

Hb
Hb;T;mg/dl;0-12

Structure of a database table of a test
---------------------------------------
id
patient_id
test1
test2
user
status (data entered/printed)
date time (date and time of printing)
