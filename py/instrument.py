import sys
import time

import Adafruit_MPR121.MPR121 as MPR121
import rtmidi
from rtmidi.midiconstants import *


cap_addrs = [
#	0x5a,
#	0x5b,
#	0x5c,
	0x5d
]

key_map = [
	(0, 60),
	(0, 61),
	(0, 62),
	(0, 63),
	(0, 64),
	(0, 65),
	(0, 66),
	(0, 67),
	(0, 68),
	(0, 69),
	(0, 70),
	(0, 71),
]

caps = []
for addr in cap_addrs:
	cap = MPR121.MPR121()
	cap.begin(addr)
	caps.append(cap)

mo = rtmidi.MidiOut()
mo.open_port(1)

keys = [False] * 48
keys_last = [False] * 48

while True:
	for cap in range(len(caps)):
		touched_data = caps[cap].touched()

		for pin in range(12):
			key = cap*12 + pin
			keys[key] = touched_data & (1 << pin)

			if keys[key] and not keys_last[key]:
				print("Key %d touched" % (key,))
				mo.send_message([NOTE_ON + key_map[key][0], key_map[key][1], 127])
			elif not keys[key] and keys_last[key]:
				print("Key %d released" % (key,))
				mo.send_message([NOTE_OFF + key_map[key][0], key_map[key][1], 0])

			keys_last[key] = keys[key]

	time.sleep(0.01)
