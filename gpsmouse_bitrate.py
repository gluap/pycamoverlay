#!/usr/bin/env python3
import serial
import codecs

set_baud = bytes.fromhex("b5 62 06 00 14 00 01 00 00 00 d0 08 00 00 00 c2 01 00 07"
                         " 00 07 00 00 00 00 00 c4 96 b5 62 06 00 01 00 01 08 22")

with serial.Serial('/dev/ttyAMA0', 9600, timeout=1) as ser:
    ser.write(set_baud)
set_speed = bytes.fromhex("B5 62 06 08 06 00 64 00 01 00 01 00 7A 12 B5 62 06 08 00 00 0E 30".replace(" ", ''))
write_settings = bytes.fromhex("B5 62 06 09 0D 00 00 00 00 00 FF FF 00 00 00 00 00 00 17 31 BF".replace(" ", ''))
with serial.Serial('/dev/ttyAMA0', 115200, timeout=1) as ser:
    ser.write(set_speed)
    ser.write(write_settings)
    while True:
        print(ser.readline())