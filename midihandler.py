"""
Device Handler
"""

from pygame import midi
midi.init()



def getDeviceList():

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

		devices.append({
			"driver": driver,
			"connection": connection,
			"is_input": True if is_input else False
		})

	return devices
	