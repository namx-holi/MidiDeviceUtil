

"""
event_grid.py

Description of file

@author: namx-holi
@date:   2018-02-09
"""


import Tkinter as tk
import tkFont
import ttk

import midihandler
import sys

from pygame import midi
midi.init()


# get the ID from the options
device_id = int(sys.argv[1])

# get the name from the options
device_name = sys.argv[2]

WINDOW_TITLE = "Midi Input Grid - {}".format(device_name)
GRID_BACKGROUND_COLOR = "white"
CHANNEL_DIVIDER_COLOR = "grey"


class Application(tk.Frame):

	device = None


	def __init__(self, device_id, master=None):

		tk.Frame.__init__(self, master)

		self.device = midi.Input(device_id)

		self.pack()
		self.create_widgets(master)
		self.poll()


	def create_widgets(self, master):

		box_height = 20
		box_width = 20

		self.grid_array = []
		self.channel_dividers = []

		for channel in range(16):
			self.grid_array.append([])

			self.channel_dividers.append(
				tk.Frame(self,
					width=box_width*64,
					height=box_height//4,
					bg=CHANNEL_DIVIDER_COLOR
				)
			)

			for note in range(128):

				self.grid_array[-1].append(
					tk.Frame(self,
						width=box_width,
						height=box_height,
						bg=GRID_BACKGROUND_COLOR
					)
				)			

		for row_index, row in enumerate(self.grid_array):

			self.channel_dividers[row_index].grid(
					row=row_index*3, columnspan=64
				)

			for col_index, col in enumerate(row):

				# check if col is in the first half
				if col_index < 64:
					col.grid(column=col_index, row=row_index*3+1)
				else:
					col.grid(column=col_index-64, row=row_index*3+2)


	def update_grid(self, line):

		message = line[1]
		channel = line[2]
		note = line[3]
		velocity = line[4]

		if message == "Note On":
			self.grid_array[channel][note].config(
				background=self.get_velocity_colour(velocity)
			)
		elif message == "Note Off":
			self.grid_array[channel][note].config(
				background=GRID_BACKGROUND_COLOR
			)


	def get_velocity_colour(self, velocity):

		r = velocity*2
		g = 0
		b = 0

		colour_code = "#{:02x}{:02x}{:02x}".format(r,g,b)
		return colour_code


	def poll(self):

		while self.device.poll():
			events = self.device.read(1)
			line = midihandler.event_parser(events[0])

			self.update_grid(line)

		self.after(25, self.poll)


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
