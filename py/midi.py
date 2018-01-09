#!/usr/bin/env python3

import mpr121

import re
import os
import time

import rtmidi
from rtmidi.midiconstants import *

MIDI_PORT_PID_REGEX = r'^FLUID Synth \((\d+)\).*$'
MIDI_DISCONNECTED_CHECK_INTERVAL = 1
MIDI_CONNECTED_CHECK_INTERVAL = 10

cap_addrs = [
	((1, 0x70, 0x08), 0x5a),
	((1, 0x70, 0x08), 0x5b),
	((1, 0x70, 0x08), 0x5c),
	((1, 0x70, 0x10), 0x5a),
	((1, 0x70, 0x10), 0x5b),
]

key_map = [
	(0, 71), # 0
	(0, 70), # 1
	(0, 68), # 2
	(0, 66), # 3
	(0, 64), # 4
	(0, 65), # 5
	(0, 67), # 6
	(0, 68), # 7
	(0, 71), # 8
	(0, 69), # 9
	(0, 70), # 10
	(0, 71), # 11

	(0, 60), # 12
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

	(0, 104), # 24
	(0, 103), # 25
	(0, 101), # 26
	(0, 100), # 27
	(0, 98), # 28
	(0, 97), # 29
	(0, 95), # 30
	(0, 94), # 31
	(0, 68), # 32
	(0, 69), # 33
	(0, 70), # 34
	(0, 71), # 35

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

	(0, 79), # 48
	(0, 76), # 49
	(0, 75), # 50
	(0, 73), # 51
	(0, 72), # 52
	(0, 59), # 53
	(0, 60), # 54
	(0, 61), # 55
	(0, 67), # 56
	(0, 69), # 57
	(0, 70), # 58
	(0, 72), # 59
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
find_port.port_re = re.compile(MIDI_PORT_PID_REGEX)

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
					cap = mpr121.MPR121(cap_addrs[i][0])
					try:
						cap.begin(cap_addrs[i][1])
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

def key_change(key, touched, cap, pin, midi_port):
	print("Key #%d %s (cap %s, map %d/%d)" % (key, "touch" if touched else "release", cap_addrs[cap], key_map[key][0], key_map[key][1]))

	if midi_port is not None:
		if touched:
			midi_port.send_message([NOTE_ON + key_map[key][0], key_map[key][1], 127])
		else:
			midi_port.send_message([NOTE_OFF + key_map[key][0], key_map[key][1], 0])

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
				key_change(key, True, cap, pin, port)
			elif not keys[key] and keys_last[key]:
				key_change(key, False, cap, pin, port)

			keys_last[key] = keys[key]

if __name__ == '__main__':
	main()
