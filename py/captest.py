import mpr121

import sys
import time

cap_addrs = [
	(None, 0x5a),
	(None, 0x5a),
	(None, 0x5c),
	(None, 0x5d),
]

caps = []
for addr in cap_addrs:
	cap = mpr121.MPR121(addr[0])
	cap.begin(addr[1])
	caps.append(cap)

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
			elif not keys[key] and keys_last[key]:
				print("Key %d released" % (key,))

			keys_last[key] = keys[key]

	time.sleep(0.01)
