import os
import sys
import time
from FlightRadar24 import FlightRadar24API
from escpos.printer import Usb

fr = FlightRadar24API()
p = Usb(0x04b8, 0x0e20)
p.profile.profile_data["media"]["width"]["pixels"] = 560  # specific to TM-M30 Epson printer

# paths to start or stop file
path_start = "###"
path_stop = "###"

# generate boundary
center_lat = 0  # ENTER LATITUDE
center_lon = 0  # ENTER LONGITUDE
radius = 0  # ENTER RADIUS (meters)
bounds = fr.get_bounds_by_point(center_lat, center_lon, radius)

while True:
    time.sleep(0.5)

    if os.path.exists(path_start):  
        os.remove(path_start)
        
        # generate all flights in boundary
        all_flights = fr.get_flights(bounds = bounds)

        try:
            # find closest flight to center within bounds
            flight_dis = []
            for flight in all_flights:
                distance = ((flight.latitude - center_lat) ** 2) + ((flight.longitude - center_lon) ** 2)
                flight_dis.append({"distance": distance, "flight": flight})
            
            flight_dis = sorted(flight_dis, key=lambda d: d['distance'])
            flight = flight_dis[0]['flight']

            # gather extra details for flight
            details = fr.get_flight_details(flight)

            # create variable for plane 
            try:
                aircraft = details['aircraft']['model']['text']
            except (KeyError, TypeError):
                aircraft = ''
            
            # create variable for airline
            try:
                airline = details['airline']['name']
            except (KeyError, TypeError):
                airline = ''

            # print all details
            if flight.callsign != '':
                p.set(bold=True, align='center', double_height=True, double_width=True)
                p.text(f'{flight.callsign}\n')
                p.set(bold=False, double_height=False, double_width=False)  
            
            if airline != '':
                if flight.number != '':
                    p.set(align='center')
                    p.text(f'{airline} {flight.number}\n') 
                else:
                    p.set(align='center')
                    p.text(f'{airline}\n')
        
            if flight.origin_airport_iata != '' or flight.destination_airport_iata != '':
                try:
                    origin = f'{flight.origin_airport_iata}'  # {details["airport"]["origin"]["name"]}
                except (TypeError):
                    origin = 'None'
                try:
                    destination = f'{flight.destination_airport_iata}'  # {details["airport"]["destination"]["name"]}
                except (TypeError):
                    destination = 'None'
                p.set(align='center')
                p.text(f'{origin} -> {destination}\n')

            if aircraft != '':
                p.ln(1)
                p.set(align='center')
                p.text(f'{aircraft}\n')

            if flight.registration != '':
                p.set(align='center') 
                p.text(f'{flight.registration}\n')

            # create qr code
            link = f'flightradar24.com/{flight.callsign}'
            p.qr(link, size=8, center=True)

        except (IndexError):
            p.set(align='center')
            p.text('No plane found.')

        p.cut()

    elif os.path.exists(path_stop):
        os.remove(path_stop)
        sys.exit()
        
