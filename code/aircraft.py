from FlightRadar24 import FlightRadar24API
from escpos.printer import Usb
import qrcode

fr = FlightRadar24API()
p = Usb(0x04b8, 0x0e20)

center_lat = 39.95240587773885
center_lon = -86.27362980160068
radius = 100000 # in meters

# generate all flights in bounds
bounds = fr.get_bounds_by_point(center_lat, center_lon, radius)
all_flights = fr.get_flights(bounds = bounds)

try:
    # generate details for flight of index 0
    flight = all_flights[0]
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
    p.text('\n')
    if flight.callsign != '':
        p.text(f'Callsign: {flight.callsign}\n')

    if flight.registration != '':
         p.text(f'Registration: {flight.registration}\n')

    if airline != '':
         p.text(f'Airline: {airline}\n')

    if flight.number != '':
        p.text(f'Flight number: {flight.number}\n')

    if flight.origin_airport_iata != '' or flight.destination_airport_iata != '':
        try:
            origin = f'{details["airport"]["origin"]["name"]} ({flight.origin_airport_iata})'
        except (TypeError):
            origin = 'None'
        try:
            destination = f'{details["airport"]["destination"]["name"]} ({flight.destination_airport_iata})'
        except (TypeError):
            destination = 'None'
        p.text(f'{origin} -> {destination}\n')

    if aircraft != '':
         p.text(f'Aircraft: {aircraft}\n')

    if flight.altitude != '':
        p.text(f'Altitude: {flight.altitude}ft\n')
    p.text('\n')

    # generate qr code
    link = f'flightradar24.com/{flight.callsign}'
    p.qr(link, size=8, center=True)
    p.text('\n')

except (IndexError):
    print('No plane found.')

p.cut()
