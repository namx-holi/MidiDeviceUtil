

"""
helpers.py

Description of file

@author: namx-holi
@date:   2018-02-07
"""


import unicodedata


def sort_by_col(tree, col, descending):
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
		command=lambda c=col: sort_by_col(tree, c, int(not descending))
	)


def event_parser(event):

	details = event[0]
	timestamp = event[1]

	byte0 = details[0]
	byte1 = details[1]
	byte2 = details[2]

	message_code = (byte0 & 0xf0) >> 4
	message = lookup_message(message_code)

	channel = (byte0 & 0x0f) + 1

	note = byte1
	velocity = byte2

	return [timestamp, message, channel, note, velocity]


def lookup_message(message_code):

	if message_code == 0x8:
		return "Note Off"
	elif message_code == 0x9:
		return "Note On"
	elif message_code == 0xa:
		return "Poly Key Pressure"
	elif message_code == 0xb:
		return "Controller Change"
	elif message_code == 0xc:
		return "Program Change"
	elif message_code == 0xd:
		return "Channel Pressure"
	elif message_code == 0xe:
		return "Pitch Bend"
	else:
		return "???"


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
