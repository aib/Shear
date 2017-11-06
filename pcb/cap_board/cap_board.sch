EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:switches
LIBS:relays
LIBS:motors
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:adafruit_mpr121
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Adafruit_MPR121 U1
U 1 1 59F97370
P 4450 2900
F 0 "U1" H 4250 3600 60  0000 C CNN
F 1 "Adafruit_MPR121" H 4450 2200 60  0000 C CNN
F 2 "Adafruit_MPR121:Adafruit_MPR121" H 4450 2200 60  0001 C CNN
F 3 "" H 4450 2200 60  0001 C CNN
	1    4450 2900
	1    0    0    -1  
$EndComp
NoConn ~ 4000 2600
$Comp
L GND #PWR01
U 1 1 59F974FF
P 5000 3600
F 0 "#PWR01" H 5000 3350 50  0001 C CNN
F 1 "GND" H 5000 3450 50  0000 C CNN
F 2 "" H 5000 3600 50  0001 C CNN
F 3 "" H 5000 3600 50  0001 C CNN
	1    5000 3600
	1    0    0    -1  
$EndComp
$Comp
L Conn_01x02 J1
U 1 1 59F9757D
P 5300 3400
F 0 "J1" H 5300 3500 50  0000 C CNN
F 1 "Conn_01x02" H 5300 3200 50  0000 C CNN
F 2 "Connectors_Phoenix:PhoenixContact_MSTBVA-G_02x5.08mm_Vertical" H 5300 3400 50  0001 C CNN
F 3 "" H 5300 3400 50  0001 C CNN
	1    5300 3400
	1    0    0    1   
$EndComp
$Comp
L Conn_01x02 J2
U 1 1 59F979A7
P 5800 3200
F 0 "J2" H 5800 3300 50  0000 C CNN
F 1 "Conn_01x02" H 5800 3000 50  0000 C CNN
F 2 "Connectors_Phoenix:PhoenixContact_MSTBVA-G_02x5.08mm_Vertical" H 5800 3200 50  0001 C CNN
F 3 "" H 5800 3200 50  0001 C CNN
	1    5800 3200
	1    0    0    1   
$EndComp
$Comp
L Conn_01x02 J3
U 1 1 59F979F9
P 5300 3000
F 0 "J3" H 5300 3100 50  0000 C CNN
F 1 "Conn_01x02" H 5300 2800 50  0000 C CNN
F 2 "Connectors_Phoenix:PhoenixContact_MSTBVA-G_02x5.08mm_Vertical" H 5300 3000 50  0001 C CNN
F 3 "" H 5300 3000 50  0001 C CNN
	1    5300 3000
	1    0    0    1   
$EndComp
$Comp
L Conn_01x02 J4
U 1 1 59F97A3A
P 5800 2800
F 0 "J4" H 5800 2900 50  0000 C CNN
F 1 "Conn_01x02" H 5800 2600 50  0000 C CNN
F 2 "Connectors_Phoenix:PhoenixContact_MSTBVA-G_02x5.08mm_Vertical" H 5800 2800 50  0001 C CNN
F 3 "" H 5800 2800 50  0001 C CNN
	1    5800 2800
	1    0    0    1   
$EndComp
$Comp
L Conn_01x02 J5
U 1 1 59F97A87
P 5300 2600
F 0 "J5" H 5300 2700 50  0000 C CNN
F 1 "Conn_01x02" H 5300 2400 50  0000 C CNN
F 2 "Connectors_Phoenix:PhoenixContact_MSTBVA-G_02x5.08mm_Vertical" H 5300 2600 50  0001 C CNN
F 3 "" H 5300 2600 50  0001 C CNN
	1    5300 2600
	1    0    0    1   
$EndComp
$Comp
L Conn_01x02 J6
U 1 1 59F97ABE
P 5800 2400
F 0 "J6" H 5800 2500 50  0000 C CNN
F 1 "Conn_01x02" H 5800 2200 50  0000 C CNN
F 2 "Connectors_Phoenix:PhoenixContact_MSTBVA-G_02x5.08mm_Vertical" H 5800 2400 50  0001 C CNN
F 3 "" H 5800 2400 50  0001 C CNN
	1    5800 2400
	1    0    0    1   
$EndComp
$Comp
L RJ45 J7
U 1 1 59F98B56
P 7300 2450
F 0 "J7" H 7500 2950 50  0000 C CNN
F 1 "RJ45" H 7150 2950 50  0000 C CNN
F 2 "Connectors:RJ45_8" H 7300 2450 50  0001 C CNN
F 3 "" H 7300 2450 50  0001 C CNN
	1    7300 2450
	0    1    1    0   
$EndComp
$Comp
L GND #PWR02
U 1 1 59F98B5D
P 6750 2900
F 0 "#PWR02" H 6750 2650 50  0001 C CNN
F 1 "GND" H 6750 2750 50  0000 C CNN
F 2 "" H 6750 2900 50  0001 C CNN
F 3 "" H 6750 2900 50  0001 C CNN
	1    6750 2900
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR03
U 1 1 59F98B65
P 6650 2000
F 0 "#PWR03" H 6650 1850 50  0001 C CNN
F 1 "+5V" H 6650 2140 50  0000 C CNN
F 2 "" H 6650 2000 50  0001 C CNN
F 3 "" H 6650 2000 50  0001 C CNN
	1    6650 2000
	1    0    0    -1  
$EndComp
Text Label 6400 2200 0    60   ~ 0
SCL
Text Label 6400 2600 0    60   ~ 0
SDA
NoConn ~ 6850 2400
NoConn ~ 6850 2500
NoConn ~ 6850 2700
NoConn ~ 6850 2800
NoConn ~ 7650 3000
$Comp
L RJ45 J8
U 1 1 59F98B76
P 7300 3850
F 0 "J8" H 7500 4350 50  0000 C CNN
F 1 "RJ45" H 7150 4350 50  0000 C CNN
F 2 "Connectors:RJ45_8" H 7300 3850 50  0001 C CNN
F 3 "" H 7300 3850 50  0001 C CNN
	1    7300 3850
	0    1    1    0   
$EndComp
$Comp
L GND #PWR04
U 1 1 59F98B7D
P 6750 4300
F 0 "#PWR04" H 6750 4050 50  0001 C CNN
F 1 "GND" H 6750 4150 50  0000 C CNN
F 2 "" H 6750 4300 50  0001 C CNN
F 3 "" H 6750 4300 50  0001 C CNN
	1    6750 4300
	1    0    0    -1  
$EndComp
Text Label 6400 3600 0    60   ~ 0
SCL
Text Label 6400 4000 0    60   ~ 0
SDA
NoConn ~ 6850 3800
NoConn ~ 6850 3900
NoConn ~ 6850 4100
NoConn ~ 6850 4200
NoConn ~ 7650 4400
Text Label 3500 2700 0    60   ~ 0
SCL
Text Label 3500 2800 0    60   ~ 0
SDA
$Comp
L +5V #PWR05
U 1 1 59F99753
P 3800 2050
F 0 "#PWR05" H 3800 1900 50  0001 C CNN
F 1 "+5V" H 3800 2190 50  0000 C CNN
F 2 "" H 3800 2050 50  0001 C CNN
F 3 "" H 3800 2050 50  0001 C CNN
	1    3800 2050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR06
U 1 1 59F99884
P 3900 3300
F 0 "#PWR06" H 3900 3050 50  0001 C CNN
F 1 "GND" H 3900 3150 50  0000 C CNN
F 2 "" H 3900 3300 50  0001 C CNN
F 3 "" H 3900 3300 50  0001 C CNN
	1    3900 3300
	1    0    0    -1  
$EndComp
Wire Wire Line
	4900 3500 5000 3500
Wire Wire Line
	5000 3500 5000 3600
Wire Wire Line
	4900 3400 5100 3400
Wire Wire Line
	4900 3300 5100 3300
Wire Wire Line
	4900 3200 5600 3200
Wire Wire Line
	4900 3100 5600 3100
Wire Wire Line
	4900 3000 5100 3000
Wire Wire Line
	4900 2900 5100 2900
Wire Wire Line
	4900 2800 5600 2800
Wire Wire Line
	4900 2700 5600 2700
Wire Wire Line
	4900 2600 5100 2600
Wire Wire Line
	4900 2500 5100 2500
Wire Wire Line
	4900 2400 5600 2400
Wire Wire Line
	4900 2300 5600 2300
Wire Wire Line
	6850 2100 6750 2100
Wire Wire Line
	6750 2100 6750 2900
Wire Wire Line
	6850 2300 6650 2300
Wire Wire Line
	6650 2300 6650 2000
Wire Wire Line
	6850 2200 6400 2200
Wire Wire Line
	6850 2600 6400 2600
Wire Wire Line
	6850 3500 6750 3500
Wire Wire Line
	6750 3500 6750 4300
Wire Wire Line
	6850 3700 6650 3700
Wire Wire Line
	6650 3700 6650 3400
Wire Wire Line
	6850 3600 6400 3600
Wire Wire Line
	6850 4000 6400 4000
Wire Wire Line
	3800 2050 3800 3200
Wire Wire Line
	3800 3200 4000 3200
Wire Wire Line
	4000 3000 3900 3000
Wire Wire Line
	3900 3000 3900 3300
Wire Wire Line
	2500 2800 4000 2800
$Comp
L Jumper_NO_Small JP3
U 1 1 59F9A351
P 2400 2500
F 0 "JP3" H 2400 2580 50  0000 C CNN
F 1 "Jumper_NO_Small" H 2410 2440 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x01_Pitch2.54mm" H 2400 2500 50  0001 C CNN
F 3 "" H 2400 2500 50  0001 C CNN
	1    2400 2500
	1    0    0    -1  
$EndComp
$Comp
L Jumper_NO_Small JP1
U 1 1 59F9A461
P 2400 3100
F 0 "JP1" H 2400 3180 50  0000 C CNN
F 1 "Jumper_NO_Small" H 2410 3040 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x01_Pitch2.54mm" H 2400 3100 50  0001 C CNN
F 3 "" H 2400 3100 50  0001 C CNN
	1    2400 3100
	1    0    0    -1  
$EndComp
$Comp
L Jumper_NO_Small JP2
U 1 1 59F9A4BE
P 2400 2800
F 0 "JP2" H 2400 2880 50  0000 C CNN
F 1 "Jumper_NO_Small" H 2410 2740 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x01_Pitch2.54mm" H 2400 2800 50  0001 C CNN
F 3 "" H 2400 2800 50  0001 C CNN
	1    2400 2800
	1    0    0    -1  
$EndComp
Wire Wire Line
	2600 2700 4000 2700
Wire Wire Line
	2500 3100 4000 3100
Wire Wire Line
	2200 2800 2300 2800
Wire Wire Line
	2200 3100 2300 3100
Wire Wire Line
	3700 2950 3700 2900
Wire Wire Line
	2200 2500 2200 3100
Connection ~ 2200 2800
Wire Wire Line
	2600 2700 2600 2500
Wire Wire Line
	2600 2500 2500 2500
Wire Wire Line
	2300 2500 2200 2500
Connection ~ 2200 3100
Wire Wire Line
	3700 2900 4000 2900
Wire Wire Line
	3700 2950 2200 2950
Connection ~ 2200 2950
$Comp
L +5V #PWR07
U 1 1 59F9B9D6
P 6650 3400
F 0 "#PWR07" H 6650 3250 50  0001 C CNN
F 1 "+5V" H 6650 3540 50  0000 C CNN
F 2 "" H 6650 3400 50  0001 C CNN
F 3 "" H 6650 3400 50  0001 C CNN
	1    6650 3400
	1    0    0    -1  
$EndComp
$EndSCHEMATC
