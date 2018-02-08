

"""
inputwindow.py

Description of file

@author: namx-holi
@date:   2018-02-07
"""


import Tkinter as tk
import tkFont
import ttk

import helpers
import sys

from pygame import midi
midi.init()


# get the ID from the options
device_id = int(sys.argv[1])

# get the name from the options
device_name = sys.argv[2]

WINDOW_TITLE = "Midi Controller Listener - {} (INPUT)".format(device_name)
EVENT_TREE_COLUMNS = ["Timestamp", "Channel", "Note", "Velocity", "Var4"]


class Application(tk.Frame):

	device = None


	def __init__(self, device_id, master=None):

		tk.Frame.__init__(self, master)

		self.device = midi.Input(device_id)

		self.pack()
		self.create_widgets(master)
		self.build_event_tree()
		self.poll()


	def create_widgets(self, master):

		s = """Events"""
		msg = ttk.Label(self,
			wraplength="4i",
			justify="left",
			anchor="n",
			padding=(10,2,10,6),
			text=s)
		msg.grid(
			row=0, column=0, columnspan=2, sticky="ew"
		)

		# Creating treeview with dual scrollbars
		self.event_tree = ttk.Treeview(self,
			columns=EVENT_TREE_COLUMNS,
			show="headings"
		)
		event_tree_vsb = ttk.Scrollbar(self,
			orient="vertical",
			command=self.event_tree.yview
		)
		event_tree_hsb = ttk.Scrollbar(self,
			orient="horizontal",
			command=self.event_tree.xview
		)
		self.event_tree.configure(
			yscrollcommand=event_tree_vsb.set,
			xscrollcommand=event_tree_hsb.set
		)
		self.event_tree.grid(
			row=1, column=0, sticky="nsew"
		)
		event_tree_vsb.grid(
			row=1, column=1, sticky="ns"
		)
		event_tree_hsb.grid(
			row=2, column=0, sticky="ew"
		)

		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(1, weight=1)


	def build_event_tree(self):

		for col in EVENT_TREE_COLUMNS:
			self.event_tree.heading(
				col,
				text=col.title(),
				command=lambda c=col: helpers.sort_by_col(self.event_tree, c, 0)
			)

			# Adjust the column's width to the header string
			self.event_tree.column(
				col,
				width=tkFont.Font().measure(col.title())+10
			)


	def poll(self):

		while self.device.poll():
			events = self.device.read(1)
			line = helpers.event_parser(events[0])

			self.event_tree.insert("", "end", values=line)
			helpers.sort_by_col(self.event_tree, "Timestamp", 1)

			for ix, val in enumerate(line):
				col_w = max(tkFont.Font().measure(val), tkFont.Font().measure(EVENT_TREE_COLUMNS[ix]))+10

				if self.event_tree.column(EVENT_TREE_COLUMNS[ix], width=None)<col_w:
					self.event_tree.column(EVENT_TREE_COLUMNS[ix], width=col_w)

		self.after(250, self.poll)


# create root and configure
root = tk.Tk()
root.title(WINDOW_TITLE)

# start up the application
app = Application(device_id, master=root)
app.mainloop()
