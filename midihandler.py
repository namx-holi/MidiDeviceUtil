

"""
midihandler.py

Description of file

@author: namx-holi
@date:   2018-02-07
"""


import subprocess

from pygame import midi
midi.init()


def getDeviceList():
	"""
	THIS IS VERY VERY DUMB
	
	This is done because to get the correct count of midi devices,
	the python process needs to be restarted, or started fresh.
	"""

	test = subprocess.check_output(
		["python", "-c", "import midihandler;midihandler._getDeviceList()"]
	)
	exec("devices = {}".format(test))
	
	return devices
	

def _getDeviceList():

	from pygame import midi
	midi.init()

	devices = []

	for device_id in range(midi.get_count()):
		(
			driver, 
			connection, 
			is_input, 
			is_output, 
			x
		) = midi.get_device_info(device_id)

		if (is_input and is_output) or (not is_input and not is_output):
			raise Exception("Not sure what happened here")

		devices.append([
			device_id,
			unicode(driver),
			unicode(connection),
			u"Input" if is_input else u"Output"
		])

	print(devices)


def connect_to_input(id, name):

	subprocess.Popen(["python", "inputwindow.py", str(id), name])


def connect_to_output(id, name):

	subprocess.Popen(["python", "outputwindow.py", str(id), name])
