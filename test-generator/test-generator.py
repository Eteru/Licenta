#!/usr/bin/python

import sys
import random, string
from random import randint
from sets import Set

files_name 		= "test_file"
files_extension = ".c"
files_no 		= 0

int_type 	= "int"
void_type 	= "void"
semi_collon = ";"
parenthesis = "()"

keywords = ["", "const", "static"]
external = "extern"

VARIABLE = 0
FUNCTION = 1

generated_main = False

unique_symbols	 = Set()
external_symbols = []
used_ext_symbols = []

symbols = {}

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def generate_symbols(file_no, is_function = False):
	global generated_main
	file_symbols = []
	symbols_no = randint(0,2) if is_function else randint(5,10)

	if generated_main == False:
		generated_main = True
		file_symbols.append({
			'Name' : "main",
			'Type' : FUNCTION,
			'Keyword' : "",
			'File' : file_no})

	for i in range(symbols_no):
		sym = randomword(randint(2,5))
		while sym in unique_symbols:
			sym = randomword(randint(2,5))

		file_symbols.append({
			'Name' : sym,
			'Type' : -1,
			'Keyword' : "",
			'File' : file_no})
		unique_symbols.add(sym)

	return file_symbols

def generate_functions(file, function):
	syms = generate_symbols(function['File'], True)

	ext_symbols = filter(lambda sym: sym['File'] != function['File'] and \
									sym['Type'] == FUNCTION,
									external_symbols)

	ext_symbols.extend(used_ext_symbols[function['File']])

	# no need to use that many symbols in a single function
	symbols_no 	= randint(0, len(ext_symbols) / 3)
	start_index = randint(0, len(ext_symbols) - symbols_no - 1)

	file.write((int_type if function['Name'] == "main" else void_type) + \
				" " + function['Name'] + parenthesis + \
				"\n" + "{" + "\n")

	for sym in syms:
		file.write("\t" + int_type + " " + sym['Name'] + semi_collon + "\n")

	file.write("\n")

	# write basic instruction to use the symbol
	for i in range (start_index, start_index + symbols_no):
		file.write("\t" + ext_symbols[i]['Name'])

		if ext_symbols[i]['Type'] == VARIABLE:
			file.write("++;\n")
		else:
			file.write(parenthesis + semi_collon + "\n")

	file.write(("\treturn 0;\n" if function['Name'] == "main" else "") + \
				"}" + "\n" + "\n")

def generate_file(file_no):
	filename = files_name + str(file_no + 1) + files_extension

	file = open(filename, "w")

	ext_syms = filter(lambda sym: sym['Keyword'] == external, symbols[file_no])

	for sym in ext_syms:
		file.write(int_type + " " + \
					sym['Name'] + semi_collon + "\n")

	file.write("\n")

	init_syms = filter(lambda sym: sym['File'] != file_no and \
								sym['Keyword'] == external, external_symbols)

	used_ext_symbols.append(init_syms)

	for sym in init_syms:
		file.write(external + " " + int_type + " " + \
					sym['Name'] + semi_collon + "\n")

	file.write("\n")

	other_syms = filter(lambda sym: sym['Keyword'] != external and
									sym['Type'] == VARIABLE, symbols[file_no])

	for sym in other_syms:
		file.write(sym['Keyword'] + " " + int_type + " " + \
					sym['Name'] + semi_collon + "\n")

	file.write("\n")

	funcs = filter(lambda sym: sym['Type'] == FUNCTION, symbols[file_no])

	for f in funcs:
		generate_functions(file, f)

	file.close()

def start():
	files_no = randint(2,4)

	# generate symbols for each file
	for i in range(files_no):
		symbols[i] = generate_symbols(i)

	# parse the generated symbols and assign them a type and a keyword
	for i in range(files_no):
		for sym in symbols[i]:
			# need a lot of external symbols
			if sym['Name'] == "main":
				continue

			if randint(0,1) == 0:
				sym['Type'] = VARIABLE
				sym['Keyword'] = external
				external_symbols.append(sym)
			else:
				sym['Type'] = randint(0,1)
				sym['Keyword'] = keywords[randint(0,2)] if sym['Type'] == 0 else ""

				if sym['Type'] == FUNCTION:
					external_symbols.append(sym)

	for i in range(files_no):
		generate_file(i)

	print "Created", files_no, "files."

start()

