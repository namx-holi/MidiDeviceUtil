"""
Helpers!
"""


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
	#data = change_numeric(data)

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
	var1 = details[0]
	var2 = details[1]
	var3 = details[2]
	var4 = details[3]

	return [timestamp, var1, var2, var3, var4]


