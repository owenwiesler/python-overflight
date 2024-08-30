# Raspberry Pi Setup

## Hardware

- Raspberry Pi

## Dependency Installation

Firstly, pip must be installed onto the Pi. This can be done via the terminal using the command:
```
sudo apt install python3-pip
```
Next, to add the required modules for this project:
```
sudo pip install FlightRadarAPI
```
and
```
sudo pip install python-escpos
```
It is possible that an error will occur at this stage: "This environment is externally managed...". Adding *--break-system-packages* as an argument should resolve this issue. 

## Setup

1. SCP aircraft.py to the Pi. This can be done in a secondary computer's terminal using the command:
    ```
    scp aircraft.py pi@XX.X.XX.XXX:~/
    ```
    - This must be executed from the same directory that the script is present in. 
    - If using a Pi OS that includes desktop, the script can be downloaded straight from the Pi iteslf into the desired directory.

2. Edit the *center_lon*, *center_lat*, and *radius* variables to the match the region that the script will look for aircraft in.
    - To edit the script from the Pi, run the following command from within the terminal:
    ```
    sudo nano aircraft.py
    ```

3. Edit the *path_start* and *path_stop* variables. These are the paths that the script will look for to either execute itself, or stop entirely.

4. To have the program run continuously from boot up, the *cron* scheduling utility will be used. To use cron, enter this command in the terminal:
    ```
    crontab -e
    ```
    Next, add a new line to the bottom of the file and write:
    ```
    @reboot sleep30; python3 /home/pi/aircraft.py &
    ```
    - The *sleep30* adds a 30 second delay from when the Pi boots up to when the program is started. This can be changed, or removed, but to assure that all the required packages for the program are loaded before running, it is left in.

5. Reboot the Pi:
    ```
    sudo reboot
    ```

6. Check to see if the program is running:
    ```
    ps -aef | grep python
    ```

7. Write the necessary file to the start path to run the program:
    ```
    touch XXXXX
    ```

8. [Optional] Create a shortcut to run the program from an iPhone using "Run script over SSH". Input all required information. 
