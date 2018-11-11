#!/usr/bin/env python3

import random
import re
import os
import sys
import time

import rtmidi
from rtmidi.midiconstants import *
import Adafruit_MPR121.MPR121 as MPR121

MIDI_DISCONNECTED_CHECK_INTERVAL = 1
MIDI_CONNECTED_CHECK_INTERVAL = 10

def switchInst(k, inst):
	if hasattr(k, '__call__'):
		return k
	else:
		return (inst, k[1])

def presetDown(d, port):
	global key_map
	if d == 1: return
	curInst = key_map[0][0]
	curInst = (curInst - 1) % 7
	print("Changing current instrument to %d" % curInst)
	key_map = list(map(lambda k: switchInst(k, curInst), key_map))

def presetUp(d, port):
	global key_map
	if d == 1: return
	curInst = key_map[0][0]
	curInst = (curInst + 1) % 7
	print("Changing current instrument to %d" % curInst)
	key_map = list(map(lambda k: switchInst(k, curInst), key_map))

def panic(d, port):
	if port is not None:
		print("Sending all notes off")
		for i in range(0, 16):
			port.send_message([CONTROL_CHANGE + i, ALL_NOTES_OFF, 0])

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
	(0, 24), # 0
	(0, 25), # 1
	(0, 26), # 2
	(0, 27), # 3
	(0, 28), # 4
	(0, 29), # 5
	(0, 30), # 6
	(0, 31), # 7
	(0, 32), # 8
#	(0, 45), # 9
	presetDown, # 9
#	(0, 46), # 10
	presetUp, # 10
	(0, 47), # 11

	(0, 12), # 12
	(0, 22), # 13
	(0, 13), # 14
	(0, 14), # 15
	(0, 15), # 16
	(0, 16), # 17
	(0, 18), # 18
	(0, 19), # 19
	(0, 20), # 20
	(0, 23), # 21
	(0, 17), # 22
	(0, 21), # 23

#	(0, 0), # 24
	panic, # 24
	(0, 1), # 25
	(0, 2), # 26
	(0, 3), # 27
	(0, 4), # 28
	(0, 5), # 29
	(0, 6), # 30
	(0, 7), # 31
	(0, 8), # 32
	(0, 9), # 33
	(0, 10), # 34
	(0, 11), # 35

	(0, 33), # 36
	(0, 34), # 37
	(0, 35), # 38
	(0, 36), # 39
	(0, 37), # 40
	(0, 38), # 41
	(0, 39), # 42
	(0, 40), # 43
	(0, 41), # 44
	(0, 42), # 45
	(0, 43), # 46
	(0, 44), # 47
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
	global key_map
	if len(sys.argv) > 1 and sys.argv[1] == "2":
		init(2)
	else:
		init(1)

	print("Running on addrs %r" % cap_addrs)

	(port, pid) = (None, None)
	midiCheckTime = time.monotonic()

	inst = random.randint(0, 6)
	print("Changing current instrument to %d" % inst)
	key_map = list(map(lambda k: switchInst(k, inst), key_map))

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
			print("Sending all notes off")
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
				m = key_map[key]
				if hasattr(m, '__call__'):
					print("Key %d touched (function)" % key)
					m(0, port)
				else:
					print("Key %d touched (%d on %d)" % (key, m[1], m[0]))
					if port is not None:
						port.send_message([NOTE_ON + m[0], m[1], 127])
			elif not keys[key] and keys_last[key]:
				m = key_map[key]
				if hasattr(m, '__call__'):
					print("Key %d released (function)" % key)
					m(1, port)
				else:
					print("Key %d released (%d on %d)" % (key, m[1], m[0]))
					if port is not None:
						port.send_message([NOTE_OFF + m[0], m[1], 0])

			keys_last[key] = keys[key]

if __name__ == '__main__':
	main()
