#!/usr/bin/env python3

import re
import os
import sys
import time

import rtmidi
from rtmidi.midiconstants import *
import Adafruit_MPR121.MPR121 as MPR121

MIDI_DISCONNECTED_CHECK_INTERVAL = 1
MIDI_CONNECTED_CHECK_INTERVAL = 10

cap_addrs1 = [
	0x5a,
	0x5b,
	0x5c,
	0x5d,
]

cap_addrs2 = [
	0x5a,
	0x5b,
]

key_map1 = [
	(0, 71), # 0
	(0, 70), # 1
	(0, 68), # 2
	(0, 66), # 3
	(0, 64), # 4
	(0, 65), # 5
	(0, 67), # 6
	(0, 68), # 7
	(0, 71), # 8
	(0, 87), # 9
	(0, 86), # 10
	(0, 84), # 11

	(0, 94), # 12
	(0, 74), # 13
	(0, 89), # 14
	(0, 88), # 15
	(0, 87), # 16
	(0, 86), # 17
	(0, 80), # 18
	(0, 79), # 19
	(0, 78), # 20
	(0, 73), # 21
	(0, 84), # 22
	(0, 76), # 23

	(0, 108), # 24
	(0, 107), # 25
	(0, 104), # 26
	(0, 106), # 27
	(0, 103), # 28
	(0, 107), # 29
	(0, 105), # 30
	(0, 102), # 31
	(0, 101), # 32
	(0, 100), # 33
	(0, 99), # 34
	(0, 97), # 35

	(0, 79), # 36
	(0, 76), # 37
	(0, 75), # 38
	(0, 73), # 39
	(0, 72), # 40
	(0, 59), # 41
	(0, 60), # 42
	(0, 61), # 43
	(0, 67), # 44
	(0, 69), # 45
	(0, 70), # 46
	(0, 72), # 47
]

key_map2 = [
	(0, 99), # 0
	(0, 101), # 1
	(0, 103), # 2
	(0, 104), # 3
	(0, 100), # 4
	(0, 101), # 5
	(0, 105), # 6
	(0, 106), # 7
	(0, 102), # 8
	(0, 103), # 9
	(0, 107), # 10
	(0, 108), # 11

	(1, 80), # 12
	(1, 79), # 13
	(1, 77), # 14
	(1, 79), # 15
	(1, 80), # 16
	(1, 84), # 17
	(1, 86), # 18
	(1, 87), # 19
	(1, 91), # 20
	(1, 92), # 21
	(1, 96), # 22
	(1, 98), # 23
]

cap_addrs = None
key_map = None
caps = None
keys = None
keys_last = None

def init(i):
	global cap_addrs, key_map, caps, keys, keys_last
	if i == 2:
		cap_addrs = cap_addrs2
		key_map = key_map2
	else:
		cap_addrs = cap_addrs1
		key_map = key_map1

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
	if len(sys.argv) > 1 and sys.argv[1] == "2":
		init(2)
	else:
		init(1)

	print("Running on addrs %r" % cap_addrs)

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
