import string

def get_dynamic_variable_name(text):
	return text.translate(string.maketrans('',''), string.punctuation)
