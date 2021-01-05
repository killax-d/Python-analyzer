#!/usr/bin/python3
# regex import
import re
import sys
import os
import platform

columns = 70;
if (platform.system() != "Windows"):
	columns, rows = os.get_terminal_size(0)

for file in sys.argv[1:]:

	with open(file) as f:

		line = "#DONNE Dylan"
		line_number = 0;
		# Init variable
		previous_depth = 0
		max_loop = 0

		in_function = False
		function_regex = ""
		function = {}

		recursives = {}

		max_trace = []
		trace = []

		in_comment_simple = False
		in_comment_double = False


		while line:
			line = f.readline()
			line_number+=1

			if (line.startswith("    ")):
				print("Trying to fix space instead of tabulation at line : " + str(line_number))
				line = line.replace("    ", '\t')

			clean_line = re.sub("\\s|\n|\r", '', line)

			if (len(clean_line) > 0 and len(clean_line.split('#')[0]) > 0):
				# comment in line fix
				line = line.split('#')[0]

				skip = False

				if (line.count("\'\'\'") == 2):
					skip = True

				elif (line.count("\"\"\"") == 2):
					skip = True

				elif ("\'\'\'" in line):
					in_comment_simple = not in_comment_simple
					skip = True

				elif ("\"\"\"" in line):
					in_comment_double = not in_comment_double
					skip = True


				if (in_comment_simple or in_comment_double):
					skip = True

				if (not skip):
					# reset depth
					current_depth = 0

					# Calculate current depth
					for c in line:
						if (c == '\t'):
							current_depth += 1

					args = line[current_depth:].split(' ')
					word = args[0]

					matching_loop = (word == 'for' or word == 'while')
					matching_func = (word == 'def')

					if (in_function and current_depth <= function['depth']):
						# out of function, close it
						in_function = False

					if (in_function):
						# if actually in function mode
						# search if regex '%function_name%(%args%)' is in line
						# None if not
						self_call = re.search(function_regex, line)
						if (self_call):
							if(function['name'] not in recursives):
								# if is not already called, then add basics attributes
								recursives[function['name']] = {'line': function['line'], 'lines': [line_number], 'args': function['args']}
							else:
								# else just add line number
								recursives[function['name']]['lines'].append(line_number)


					if(len(trace) > 0):
						for i in range(len(trace)):
							# if current depth is inferior to previous detection
							# remove all superior depth trace
							if (trace[i]['depth'] >= current_depth):
								# keep from 0 to 'i' position
								trace = trace[:i]
								break

					if (matching_loop):
						# if actually in loop mode (for|while)

						# then append new detection
						trace.append({'line': line_number, 'depth': current_depth, 'text': line})

						# if current trace is bigger than current max trace
						# make a copy (non mutable)
						if (len(trace) > len(max_trace)):
							max_trace = trace.copy()

					if (matching_func):
						in_function = True
						# split line to get text between '()'
						function_args = line.split('(')[1].split(')')[0]
						# args is already splitted by space ' ', so i=1 -> '%function_name%(...):'
						function_name = args[1].split('(')[0]

						function = {'line': line_number, 'depth': current_depth, 'name': function_name, 'args': function_args}
						if (len(function_args) > 0):
							# if args > 0, add '(.*),' for each args
							# and then, remove last comma ',' with [:-1]
							function_regex = re.compile("[\\s+\\.\\{\\}\\[\\]\\(\\)\\/\\+\\-\\=]" + function['name'] + "\\(" + ('([a-zA-Z0-9_"\'\\.\\{\\}\\[\\]\\(\\)\\/\\+\\-\\=\\s]*),' * (len(function_args.split(','))))[:-1] + "\\)")
						else:
							# without args, just compile '()' 
							function_regex = re.compile("[\\s+\\.\\{\\}\\[\\]\\(\\)\\/\\+\\-\\=]" + function['name'] + "\\(\\)")


	print("_" * columns)
	print("File : " + file)
	if (len(max_trace) > 0):
		print("Max loop : " + str(len(max_trace)) + "\nTrace :")
		print("-> line | text\n-> -----------")
		for l in max_trace:
			print("-> {0:4d} | {1:}".format(l['line'], l['text'][:-1]))
	else:
		print("-> No loop (while|for)")

	print("\n-= Recursives Detection =-")

	if (len(recursives) > 0):
		print("\nRecursives functions : ")
		print("-> line | infos\n-> -----------")
		for f in recursives:
			print("-> {0:4d}".format(recursives[f]['line']) + " | " + f + "(" + recursives[f]['args'] + ") | at lines : " + str(recursives[f]['lines']))
	else:
		print("-> No Recursives functions")

print("\nUsage : ./analyzer.py [file...]")