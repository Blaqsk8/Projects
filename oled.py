# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid white
background, a smaller black rectangle, and some white text.
"""

import board
import busio
import displayio
import terminalio
import time
import adafruit_adt7410
from adafruit_display_text import label
from digitalio import DigitalInOut, Direction, Pull
import adafruit_displayio_ssd1306
import adafruit_displayio_sh1107
import adafruit_gps
import adafruit_adxl34x

# If using I2C, we'll create an I2C interface to talk to using default pins
i2c = board.I2C()

# Create accelerometer object
accelerometer = adafruit_adxl34x.ADXL343(i2c)

# Create button objects
button_a = DigitalInOut(board.D9)
button_b = DigitalInOut(board.D6)
button_c = DigitalInOut(board.D5)

# Set direction of circuit
button_a.direction = Direction.INPUT
button_b.direction = Direction.INPUT
button_c.direction = Direction.INPUT

# Set Pullup
button_a.pull = Pull.UP
button_b.pull = Pull.UP
button_c.pull = Pull.UP

# Create a serial connection for the GPS connection using default speed and
# a slightly higher timeout (GPS modules typically update once a second).
# These are the defaults you should use for the GPS FeatherWing.
# For other boards set RX = GPS module TX, and TX = GPS module RX pins.
uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)

# for a computer, use the pyserial library for uart access
# import serial
# uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=10)

# Create a GPS module instance.
gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial
# gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface

# Create a GPS module instance.
gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial
# gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface

# Initialize the GPS module by changing what data it sends and at what rate.
# These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
# PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
# the GPS module behavior:
#   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
# Turn on just minimum info (RMC only, location):
# gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn off everything:
# gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn on everything (not all of it is parsed!)
# gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b"PMTK220,1000")
# Or decrease to once every two seconds by doubling the millisecond value.
# Be sure to also increase your UART timeout above!
# gps.send_command(b'PMTK220,2000')
# You can also speed up the rate, but don't go too fast or else you can lose
# data during parsing.  This would be twice a second (2hz, 500ms delay):
# gps.send_command(b'PMTK220,500')

displayio.release_displays()

adt = adafruit_adt7410.ADT7410(i2c, address=0x48)
adt.high_resolution = True

display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_sh1107.SH1107(display_bus, width=128, height=64)

#Create Lines of text
splash = displayio.Group()
line1 = label.Label(terminalio.FONT, text="                ",
    color=0xFFFF00, x=2, y=3)
line2 = label.Label(terminalio.FONT, text="                ",
    color=0xFFFF00, x=2, y=13)
line3 = label.Label(terminalio.FONT, text="                ",
    color=0xFFFF00, x=2, y=23)

splash.append(line1)
splash.append(line2)
splash.append(line3)

display.show(splash)




def display_loc():
    while True:
        lat = round(gps.latitude, 6)
        long = round(gps.longitude, 5)
        alt = round(gps.altitude_m, 5)
        line1.text = "Lat: " + str(lat)
        line2.text = "Long: " + str(long)
        line3.text = "Alt: " + str(alt)
        if not button_b.value:
            display_temp()
        if not button_c.value:
            display_orientation()
        time.sleep(0.2)

def display_temp():
    last_print_1 = time.monotonic()
    while True:
        gps.update()
        current = time.monotonic()
        if current - last_print_1 >= 1.0:
            last_print = current
            temp_f = round(adt.temperature*1.8 + 32, 2)
            temp_c = round(adt.temperature, 2)
            print(gps.timestamp_utc.tm_hour)
            if gps.timestamp_utc.tm_hour >= 0 and gps.timestamp_utc.tm_hour <= 3:
                time_hf = gps.timestamp_utc.tm_hour + 8
            if gps.timestamp_utc.tm_hour = 4:
                time_hf = 12
            if gps.timestamp_utc.tm_hour >= 4 and gps.timestamp_utc.tm_hour <= 23:
                time_hf = gps.timestamp_utc.tm_hour - 4
            time_f = "{:02}:{:02}:{:02}".format(time_hf,
                    gps.timestamp_utc.tm_min,
                    gps.timestamp_utc.tm_sec)
            line1.text = "Time: " + time_f
            line2.text = "Temp F: " + str(temp_f)
            line3.text = "Temp C: " + str(temp_c)
            if not button_a.value:
                display_loc()
            if not button_c.value:
                display_orientation()
            time.sleep(0.1)

def display_orientation():
    while True:
        acceleration = accelerometer.acceleration
        x_accel = round(acceleration[0], 2)
        y_accel = round(acceleration[1], 2)
        z_accel = round(acceleration[2], 2)
        line1.text = "X: " + str(x_accel)
        line2.text = "Y: " + str(y_accel)
        line3.text = "Z: " + str(z_accel)
        if not button_a.value:
            display_loc()
        if not button_b.value:
            display_temp()
        time.sleep(0.2)

# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()

while True:
    gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print("Waiting for fix...")
            continue
        # We have a fix! (gps.has_fix is true)
        # Print out details about the fix like location, date, etc.
        print("=" * 40)  # Print a separator line.
        print(
            "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                gps.timestamp_utc.tm_mday,  # struct_time object that holds
                gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                gps.timestamp_utc.tm_min,  # month!
                gps.timestamp_utc.tm_sec,
            )
        )
        print("Latitude: {0:.6f} degrees".format(gps.latitude))
        print("Longitude: {0:.6f} degrees".format(gps.longitude))
        print("Fix quality: {}".format(gps.fix_quality))
        # Some attributes beyond latitude, longitude and timestamp are optional
        # and might not be present.  Check if they're None before trying to use!
        if gps.satellites is not None:
            print("# satellites: {}".format(gps.satellites))
        if gps.altitude_m is not None:
            print("Altitude: {} meters".format(gps.altitude_m))
        if gps.speed_knots is not None:
            print("Speed: {} knots".format(gps.speed_knots))
        if gps.track_angle_deg is not None:
            print("Track angle: {} degrees".format(gps.track_angle_deg))
        if gps.horizontal_dilution is not None:
            print("Horizontal dilution: {}".format(gps.horizontal_dilution))
        if gps.height_geoid is not None:
            print("Height geo ID: {} meters".format(gps.height_geoid))
        temp_f = round(adt.temperature*1.8 + 32, 1)

        if not button_a.value:
            display_loc()

        if not button_b.value:
            display_temp()

        if not button_c.value:
            display_orientation()
