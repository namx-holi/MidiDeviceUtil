#!

"""
Description of file

@author: namx-holi
@date:   2018-02-07
"""

import Tkinter as tk
import midihandler

WINDOW_TITLE = "Midi Controller Listener"




class Application(tk.Frame):

	selected_device = None
	devices = []

	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		self.create_widgets(master)
		self.poll()


	def create_widgets(self, master):
		# List of devices that can be connected to
		self.device_list_scrollbar = tk.Scrollbar(self,
			orient=tk.VERTICAL
		)
		self.device_list = tk.Listbox(self,
			exportselection=0,
			yscrollcommand=self.device_list_scrollbar.set
		)
		self.device_list_scrollbar.config(
			command=self.device_list.yview
		)

		# Button to refresh list of devices
		self.refresh_button = tk.Button(self,
			text="Refresh",
			command=self.update_device_list
		)

		# Packing items into the frame.
		# TODO: Get scrollbar working
		#self.device_list_scrollbar.grid()
		self.device_list.grid(
			row=0, rowspan=1, column=0, columnspan=1
		)
		self.device_list_scrollbar.grid(
			row=0, rowspan=1, column=1, columnspan=1,
			sticky=tk.N+tk.S
		)
		self.refresh_button.grid(
			row=1, rowspan=1, column=0, columnspan=2,
			sticky=tk.W+tk.E
		)


	def poll(self):
		now = self.device_list.curselection()
		if now != self.selected_device:
			self.selection_changed(now)
			self.selected_device = now
		self.after(250, self.poll)


	def selection_changed(self, selection):
		if selection is None or selection is ():
			print("No selected item.")
		else:
			print("Selection is now {}.".format(
				self.devices[selection[0]]))


	def update_device_list(self):
		self.devices = midihandler.getDeviceList()

		self.device_list.delete(0, tk.END)
		
		for device in self.devices:
			self.device_list.insert(
				tk.END,
				"{}|{}|{}".format(
					device["driver"],
					device["connection"],
					device["is_input"]
				)
			)

	def connect_to_selected_device(self):
		pass


# create root and configure
root = tk.Tk()
root.title(WINDOW_TITLE)

# start up the application
app = Application(master=root)
app.mainloop()
