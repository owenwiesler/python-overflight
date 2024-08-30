# python-overflight

## Description

Python Overflight is a script that utilizes a [Flight Radar API](https://github.com/JeanExtreme002/FlightRadarAPI) to gather information of an aircraft flying overhead of a specified region, and then print the data onto receipt paper utilizing an [ESC/POS Python library](https://github.com/python-escpos/python-escpos).

The region boundary can be manually set via latitude and longitude coordinates, with the radius being adjustable as well.

Vendor and serial number of printer must be set manually, and if applicable, a profile for a specific printer can be set. See the [ESC/POS Documentation](https://python-escpos.readthedocs.io/en/latest/) to learn more.

## Dependencies

This script makes use of:

- [FlightRadarAPI](https://github.com/JeanExtreme002/FlightRadarAPI)
- [python-escpos](https://github.com/python-escpos/python-escpos)

## Usage

#### Raspberry Pi / Linux

In my case, this script is running off of a Raspberry Pi Zero W. The script runs on boot up, initially importing the required modules. The script then looks for a file to be written to a path that, once seen, runs the rest of the code. This was done to eliminate the time taken to import the modules that takes a surprisngly long time.

At the moment, I have a shortcut on my iPhone that is able to SSH into the Pi and using the *touch* command, writes a file to the path that the Pi looks for. On execution, the script deletes the created file and goes into the pause phase, waiting again for a file to be created. This works with Siri and runs fast enough for my uses. 

For the entire setup, please see [rpi-setup](https://github.com/owenwiesler/python-overflight/blob/main/rpi-setup.md).

#### Macintosh

Unavailable. 

Aircraft data gathering works well (and quickly), but unable to print using the thermal receipt printer I have available, and Epson TM-M30. 

#### Windows

Unavailable. 

## Documentation

*To come...*
