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
	((1, 0x70, 0x01), 0x5a),
	((1, 0x70, 0x01), 0x5b),
	((1, 0x70, 0x01), 0x5c),
	((1, 0x70, 0x02), 0x5a),
	((1, 0x70, 0x02), 0x5b),
]

insts = [
	0,
	10,
	20,
	30
]
def sp_change_01(n):
	base = 10 * n
	def _change_01(k, t, c, p, m):
		if not t: return
		if (insts[n] - base) % 2 == 0: insts[n] += 1
		else: insts[n] -= 1
		m.send_message([PROGRAM_CHANGE + n, insts[n]])
		print("Channel", n, "changed to", insts[n])
	return _change_01

def sp_change_2(n):
	base = 10 * n
	def _change_2(k, t, c, p, m):
		if not t: return
		if insts[n] < base+2: insts[n] += 2
		else: insts[n] -= 2
		m.send_message([PROGRAM_CHANGE + n, insts[n]])
		print("Channel", n, "changed to", insts[n])
	return _change_2

def sp_silence(k, t, c, p, m):
	for chan in range(16):
		m.send_message([CONTROL_CHANGE + chan, ALL_NOTES_OFF, 0])
	print("Silence!")

key_map = [
	sp_silence, # 0
	(0, 45), # 1
	(0, 47), # 2
	(0, 48), # 3
	(0, 50), # 4
	(0, 52), # 5
	(0, 53), # 6
	(0, 55), # 7
	(0, 57), # 8
	(0, 59), # 9
	(0, 60), # 10
	sp_change_01(0), # 11

	sp_change_01(1), # 12
	(1, 48), # 13
	(0, 60), # 14
	(1, 49), # 15
	(0, 61), # 16
	(1, 50), # 17
	(0, 62), # 18
	(1, 51), # 19
	(0, 64), # 20
	(1, 52), # 21
	(0, 65), # 22
	(0, 67), # 23

	(1, 53), # 24
	(1, 55), # 25
	(1, 57), # 26
	sp_change_2(1), # 27
	(0, 69), # 28
	(0, 71), # 29
	sp_change_2(0), # 30
	(3, 60), # 31
	(3, 59), # 32
	(3, 57), # 33
	(4, 64), # 34
	sp_silence, # 35

	sp_change_01(2), # 36
	(2, 62), # 37
	(2, 60), # 38
	(2, 59), # 39
	(2, 58), # 40
	(2, 57), # 41
	(2, 56), # 42
	(2, 55), # 43
	(2, 54), # 44
	(2, 53), # 45
	(2, 52), # 46
	(2, 51), # 47

	(2, 50), # 48
	(2, 49), # 49
	(2, 48), # 50
	sp_change_2(3), # 51
	(3, 65), # 52
	(3, 64), # 53
	(3, 62), # 54
	(3, 60), # 55
	(3, 59), # 56
	(3, 58), # 57
	(3, 57), # 58
	sp_silence, # 59
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
			for chan in range(16):
				port.send_message([CONTROL_CHANGE + chan, ALL_NOTES_OFF, 0])

def key_change(key, touched, cap, pin, midi_port):
	print("Key #%d %s (cap %s, map %s)" % (key, "touch" if touched else "release", cap_addrs[cap], key_map[key]))

	if midi_port is not None:
		if callable(key_map[key]):
			key_map[key](key, touched, cap, pin, midi_port)
		else:
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
