from FlightRadar24 import FlightRadar24API
from escpos.printer import Usb

fr = FlightRadar24API()
p = Usb(0x04b8, 0x0e20)
p.profile.profile_data["media"]["width"]["pixels"] = 560  # Number based on trial and error 

center_lat = # Latitude Coordinate
center_lon = # Longitude Coordinate
radius = # Boundary Radius

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

    # generate qr code
    link = f'flightradar24.com/{flight.callsign}'
    p.qr(link, size=8, center=True)

except (IndexError):
    p.set(align='center')
    p.text('No plane found.')

p.cut()
