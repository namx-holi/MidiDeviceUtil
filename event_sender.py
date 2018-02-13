

"""
outputwindow.py

Description of file

@author: namx-holi
@date:   2018-02-07
"""


import Tkinter as tk
import tkFont
import ttk

import sys

from pygame import midi
midi.init()


# get the ID from the options
device_id = int(sys.argv[1])

# get the name from the options
device_name = sys.argv[2]

WINDOW_TITLE = "Midi Event Sender - {}".format(device_name)


class Application(tk.Frame):

	device = None


	def __init__(self, device_id, master=None):

		tk.Frame.__init__(self, master)

		self.device = midi.Output(device_id)

		self.pack()
		self.create_widgets(master)
		self.poll()


	def create_widgets(self, master):

		# stub widget
		stub = tk.Frame(self,
			width=200,
			height=200,
			bg="white"
		)
		
		stub.pack()


	def poll(self):

		pass

		self.after(250, self.poll)


	def on_closing(self):

		self.device.close()
		root.destroy()


# create root and configure
root = tk.Tk()
root.title(WINDOW_TITLE)
root.resizable(0,0)

# start up the application
app = Application(device_id, master=root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)

app.mainloop()
