#!

"""
Description of file

@author: namx-holi
@date:   2018-02-07
"""

import Tkinter as tk
import tkFont
import ttk
import midihandler
import helpers

WINDOW_TITLE = "Midi Controller Listener"
DEVICE_TREE_COLUMNS = ["Id", "Driver", "Controller", "I/O"]


class Application(tk.Frame):

	selected_device = None

	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		self.create_widgets(master)
		self.build_device_tree()
		self.poll()


	def create_widgets(self, master):

		s = """Device List"""
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
		self.device_tree = ttk.Treeview(self,
			columns=DEVICE_TREE_COLUMNS,
			show="headings"
		)
		device_tree_vsb = ttk.Scrollbar(self,
			orient="vertical",
			command=self.device_tree.yview
		)
		device_tree_hsb = ttk.Scrollbar(self,
			orient="horizontal",
			command=self.device_tree.xview
		)
		self.device_tree.configure(
			yscrollcommand=device_tree_vsb.set,
			xscrollcommand=device_tree_hsb.set
		)
		self.device_tree.grid(
			row=1, column=0, columnspan=2, sticky="nsew"
		)
		device_tree_vsb.grid(
			row=1, column=2, sticky="nse"
		)
		device_tree_hsb.grid(
			row=2, column=0, columnspan=2, sticky="ew"
		)
		# self.device_tree.bind('<ButtonRelease-1>', self.selected_item)


		# Configure all rows and columns so they expand to fill cell
		self.grid_columnconfigure(0, weight=3)
		self.grid_columnconfigure(1, weight=4)
		self.grid_rowconfigure(1, weight=1)


		# Button to refresh list of devices
		self.refresh_button = tk.Button(self,
			text="Refresh",
			command=self.update_device_tree
		)
		self.refresh_button.grid(
			row=3, column=0, sticky="nsew"
		)


		# Button to connect to device
		self.connect_button = tk.Button(self,
			text="Connect to Device",
			command=self.connect_to_selected_device
		)
		self.connect_button.grid(
			row=3, column=1, columnspan=2, sticky="nsew"
		)


	def build_device_tree(self):
		for col in DEVICE_TREE_COLUMNS:
			self.device_tree.heading(
				col,
				text=col.title(),
				command=lambda c=col: helpers.sortby(self.device_tree, c, 0)
			)

			# Adjust the column's width to the header string
			self.device_tree.column(
				col,
				width=tkFont.Font().measure(col.title())
			)

		self.update_device_tree()


	def update_device_tree(self):

		# Clear tree
		self.device_tree.delete(*self.device_tree.get_children())

		self.devices = midihandler.getDeviceList()


		for device in self.devices:
			self.device_tree.insert("", "end", values=device)

			# Adjust column's width if necessary to fit each value
			for ix, val in enumerate(device):
				col_w = max(tkFont.Font().measure(val), tkFont.Font().measure(DEVICE_TREE_COLUMNS[ix]))+10

				if self.device_tree.column(DEVICE_TREE_COLUMNS[ix], width=None)<col_w:
					self.device_tree.column(DEVICE_TREE_COLUMNS[ix], width=col_w)


	def poll(self):
		# Item was selected!
		curItem = self.device_tree.focus()
		now = self.device_tree.item(curItem)["values"]

		if now != self.selected_device:
			self.selection_changed(now)
			self.selected_device = now
		self.after(250, self.poll)


	def selection_changed(self, selection):
		if selection is None or selection is "":
			print("No selected item.")
		else:
			print("Selection is now {}.".format(selection))


	def connect_to_selected_device(self):
		if self.selected_device == "":
			print("No selected device to connect to.")
		else:
			print("THIS WOULD CONNECT TO SELECTED DEVICE <{}>".format(self.selected_device[2]))


# create root and configure
root = tk.Tk()
root.title(WINDOW_TITLE)
root.resizable(0,0)

# start up the application
app = Application(master=root)
app.mainloop()
