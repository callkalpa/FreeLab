FreeLab
=======

FreeLab is a software for printing medical reports in a laboratory.

Format of the test definition file
----------------------------------
**Test Name**

**Test Name;Value;Unit;Reference Range**

**Test Name;Value;Unit;Reference Range**

Value could be one of the following,

T - Text Field

T[straw, clear] - Combo box with 'straw' and 'clear' items

I - Integer

F - Float

A - Text area


Sample test definition file
---------------------------

Ufr

Appearence;T[starw, clear];;

Pus Cells;T;/h.f.p;;


Structure of a database table of a test
---------------------------------------
id

patient_id

test1

test2

user

date time (date and time of printing)
