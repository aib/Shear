#!/bin/bash

sysctl net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING --out-interface $2 -j MASQUERADE
iptables -A FORWARD --in-interface $1 -j ACCEPT
