

"""
helpers.py

Description of file

@author: namx-holi
@date:   2018-02-07
"""


import unicodedata


def sortby(tree, col, descending):
	"""
	Sorts a tree contents when a column header is clicked on
	"""

	# Grab values to sort
	data = [
		(tree.set(child, col), child)
		for child in tree.get_children('')
	]

	# If the data to be sorted is numeric change to float
	if all([is_number(x[0]) for x in data]):
		data = change_data_to_num(data)

	# Now sort the data in place
	data.sort(reverse=descending)
	for ix, item in enumerate(data):
		tree.move(item[1], '', ix)

	# Switch the heading so it will sort in the opposite direction
	tree.heading(
		col,
		command=lambda c=col: sortby(tree, c, int(not descending))
	)


def event_parser(event):

	details = event[0]
	timestamp = event[1]
	channel = details[0]
	note = details[1]
	velocity = details[2]
	var4 = details[3]

	return [timestamp, channel, note, velocity, var4]


def is_number(value):

	try:
		float(value)
		return True
	except ValueError:
		pass

	try:
		unicodedata.numeric(value)
		return True
	except (TypeError, ValueError):
		pass

	return False


def change_data_to_num(data):

	for ix, item in enumerate(data):
		data[ix] = (float(item[0]), item[1])

	return data
