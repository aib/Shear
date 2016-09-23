#!/usr/bin/env python3

import re
import os
import time

import rtmidi
from rtmidi.midiconstants import *
import Adafruit_MPR121.MPR121 as MPR121

MIDI_DISCONNECTED_CHECK_INTERVAL = 1
MIDI_CONNECTED_CHECK_INTERVAL = 10

cap_addrs = [
	0x5a,
	0x5b,
	0x5c,
	0x5d,
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

caps = [None] * len(cap_addrs)
keys = [False] * len(key_map)
keys_last = [False] * len(key_map)

def find_port():
	midiout = rtmidi.MidiOut()

	ports = midiout.get_ports()
	found_pid = None
	found_port = None
	for i in range(len(ports)):
		m = find_port.port_re.fullmatch(ports[i])
		if m is None: continue

		pid = int(m.group(1))
		if not pid_exists(pid): continue

		found_pid = pid
		midiout.open_port(i)
		break

	if found_pid is None:
		return (None, None)
	else:
		return (midiout, found_pid)
find_port.port_re = re.compile(r'^FLUID Synth \((\d+)\) \d+:\d+$')

def replace_port(old_port, old_pid):
	if old_port is None or old_pid is None:
		return find_port()

	if pid_exists(old_pid):
		return (old_port, old_pid)
	else:
		return find_port()

def pid_exists(pid):
	try:
		os.kill(pid, 0)
		return True
	except ProcessLookupError:
		return False
	except PermissionError:
		return True

def main():
	(port, pid) = (None, None)
	midiCheckTime = time.monotonic()

	try:
		while True:
			midi_tasks(port)

			for i in range(len(cap_addrs)):
				if caps[i] is None:
					cap = MPR121.MPR121()
					try:
						cap.begin(cap_addrs[i])
						caps[i] = cap
					except OSError:
						pass

			if port is None:
				checkInterval = MIDI_DISCONNECTED_CHECK_INTERVAL
			else:
				checkInterval = MIDI_CONNECTED_CHECK_INTERVAL

			now = time.monotonic()
			if (now - midiCheckTime >= checkInterval):
				(port, pid) = replace_port(port, pid)
				midiCheckTime = now

			time.sleep(0.001)
	except KeyboardInterrupt:
		if port is not None:
			port.send_message([CONTROL_CHANGE, ALL_NOTES_OFF, 0])
		pass

def midi_tasks(port):
	for cap in range(len(cap_addrs)):
		if caps[cap] is not None:
			try:
				touched_data = caps[cap].touched()
			except OSError:
				touched_data = 0
				caps[cap] = None
		else:
			touched_data = 0

		for pin in range(12):
			key = cap*12 + pin
			keys[key] = touched_data & (1 << pin)

			if keys[key] and not keys_last[key]:
				print("Key %d touched (%d on %d)" % (key, key_map[key][1], key_map[key][0]))
				if port is not None:
					port.send_message([NOTE_ON + key_map[key][0], key_map[key][1], 127])
			elif not keys[key] and keys_last[key]:
				print("Key %d released (%d on %d)" % (key, key_map[key][1], key_map[key][0]))
				if port is not None:
					port.send_message([NOTE_OFF + key_map[key][0], key_map[key][1], 0])

			keys_last[key] = keys[key]

if __name__ == '__main__':
	main()
