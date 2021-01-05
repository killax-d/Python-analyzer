#!/usr/bin/python3

# NOT COMMENTED (comment handled)
# Bigger loop: N°3 (Size 5)
# Recursives: [1-2-4-7-11]
# test1() & test2() & test4() & test7() & test11()

# COMMENTED (comment not handled)
# Bigger loop: N°4 (Size 6)
# Recursives: [1-2-4-7-8-9-11]
# test1() & test2() & test4() & test7() & test8() & test9() & test11()

# Types of comments
# 1
''' Commentaire 1 '''
# 2
''' Commentaire 2
'''
# 3
'''
Commentaire 3 '''
# 4
'''
Commentaire 4
'''

# LOOP

#1
# Size 3
for i in range(10):
	for k in range(10):

		while True:
			print("ok")

#2
# Size 2
for i in range(10):
	while True:
		print("ok")

#3
# Bigger loop (comment handled)
# Size 5
while True:
    while True:
		print("ok")
		if (True):
			for i in range(10):
				while True:

					print("ok")
					for j in range(10):
						print("ok")

#4
# Bigger loop (comment not handled)
# Size 6
'''
while True:
	while True:
		while True:
			while True:
				while True:
					while True:
						pass
'''

#5
# Size 4
while True:
	while True:
		print("ok")
		if (True):
			while True:
				while True:
					print("ok")


# /!\ Not recursive
def test(id):
	retest(1)

# recursives
def test1(id):
	return test1(1) # Ignore me

# recursives
def test2(id):
	test2(1)

# /!\ Not recursive
def test3(id):
	test3(1, 2)

# recursives
def test4(id, id2):
	return test4('1', "2")

# /!\ Not recursive
def test5():
	pass

test5()

# /!\ Not recursive
def test6():
	return test6

# recursives
def test7(arg0, arg1):
	return test7((1, 2), {'line': "test", 'arg': "test"})

# /!\ Not recursive
def test8(arg0, arg1):
	return 1 # test8((1, 2), {'line': "test"})

# /!\ Not recursive
'''
def test9(arg0, arg1):
	return test9((1, 2), {'line': "test"})
'''

# /!\ Not recursive
def test10(id):
	return test100(1)


# recursives
def test11(id):
	return 1+test11(1)


