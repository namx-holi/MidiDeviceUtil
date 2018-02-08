

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

WINDOW_TITLE = "Midi Controller Listener - {} (OUTPUT)".format(device_name)


class Application(tk.Frame):

	device = None


	def __init__(self, device_id, master=None):

		tk.Frame.__init__(self, master)

		self.device = midi.Output(device_id)

		self.pack()
		self.create_widgets(master)
		self.poll()


	def create_widgets(self, master):

		pass


	def poll(self):

		pass

		self.after(250, self.poll)


# create root and configure
root = tk.Tk()
root.title(WINDOW_TITLE)

# start up the application
app = Application(device_id, master=root)
app.mainloop()
