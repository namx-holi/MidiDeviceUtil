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