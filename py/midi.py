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

channel_instrument_map = [
	[20],
	[12]
]

def sp_silence(k, t, c, p, m):
	if not t: return
	midi_silence_all(m)

key_map = [
	sp_silence, # 0
	(0, 43), # 1
	(0, 49), # 2
	(0, 51), # 3
	(0, 53), # 4
	(0, 54), # 5
	(0, 58), # 6
	(0, 59), # 7
	(0, 63), # 8
	(0, 65), # 9
	(0, 66), # 10
	(0, 70), # 11

	(1, 49), # 12
	(1, 51), # 13
	(0, 72), # 14
	(1, 52), # 15
	(0, 73), # 16
	(1, 56), # 17
	(0, 77), # 18
	(1, 57), # 19
	(0, 78), # 20
	(1, 61), # 21
	(0, 82), # 22
	(0, 84), # 23

	(1, 63), # 24
	(1, 62), # 25
	(1, 60), # 26
	(2, 0), # 27
	(0, 83), # 28
	(0, 81), # 29
	(0, 77), # 30
	(0, 76), # 31
	(2, 1), # 32
	(2, 2), # 33
	(2, 3), # 34
	(2, 4), # 35

	(0, 76), # 36
	(0, 77), # 37
	(0, 80), # 38
	(0, 81), # 39
	(0, 77), # 40
	(0, 76), # 41
	(0, 74), # 42
	(0, 71), # 43
	(0, 69), # 44
	(0, 68), # 45
	(0, 64), # 46
	(0, 61), # 47

	(0, 58), # 48
	(0, 57), # 49
	(0, 54), # 50
	(0, 52), # 51
	(0, 51), # 52
	(0, 48), # 53
	(0, 47), # 54
	(0, 41), # 55
	(0, 40), # 56
	(0, 39), # 57
	(0, 38), # 58
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
				(old_port, old_pid) = (port, pid)
				(port, pid) = replace_port(port, pid)
				if old_port is None and port is not None:
					print("Connected to PID", pid)
					for chan in range(len(channel_instrument_map)):
						midi_change_instrument(port, chan, channel_instrument_map[chan][0])
				elif old_port is not None and port is None:
					print("Disconnected from PID", old_pid)
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

def midi_change_instrument(midi, channel, instrument):
	midi.send_message([PROGRAM_CHANGE + channel, instrument])
	print("Channel", channel, "changed to", instrument)

def midi_silence_all(midi):
	for channel in range(16):
		midi.send_message([CONTROL_CHANGE + channel, ALL_NOTES_OFF, 0])
	print("Silence!")

if __name__ == '__main__':
	main()
