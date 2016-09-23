#!/bin/bash

dnsmasq -d -p 0 -F 10.0.42.2,10.0.42.2,4h -O 3,10.0.42.1 -O 6,4.2.2.1,8.8.8.8,8.8.4.4 --dhcp-leasefile=/dev/null
