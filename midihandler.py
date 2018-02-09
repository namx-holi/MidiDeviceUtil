

"""
midihandler.py

Description of file

@author: namx-holi
@date:   2018-02-07
"""


import subprocess

from pygame import midi
midi.init()


def get_device_list():
	"""
	THIS IS VERY VERY DUMB
	
	This is done because to get the correct count of midi devices,
	the python process needs to be restarted, or started fresh.
	"""

	test = subprocess.check_output(
		["python", "-c", "import midihandler;midihandler._get_device_list()"]
	)
	exec("devices = {}".format(test))

	return devices
	

def _get_device_list():

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
