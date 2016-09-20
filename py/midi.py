#!/usr/bin/env python3

import re
import os
import time

import rtmidi
from rtmidi.midiconstants import *

MIDI_DISCONNECTED_CHECK_INTERVAL = 1
MIDI_CONNECTED_CHECK_INTERVAL = 10

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

	while True:
		midi_tasks(port)

		if port is None:
			checkInterval = MIDI_DISCONNECTED_CHECK_INTERVAL
		else:
			checkInterval = MIDI_CONNECTED_CHECK_INTERVAL

		now = time.monotonic()
		if (now - midiCheckTime >= checkInterval):
			print("Checking MIDI connection " + str((port, pid)) + "")
			(port, pid) = replace_port(port, pid)
			midiCheckTime = now

		time.sleep(1)

import random
def midi_tasks(port):
	if port is not None:
		note = random.randint(60, 72)
		port.send_message([NOTE_ON, note, 127])
		time.sleep(0.1)
		port.send_message([NOTE_OFF, note, 0])

if __name__ == '__main__':
	main()
