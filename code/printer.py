from FlightRadar24 import FlightRadar24API
import qrcode

fr = FlightRadar24API()

center_lat = 39.95240587773885
center_lon = -86.27362980160068
radius = 4000 # in meters

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

    # print all details to terminal
    print()
    if flight.callsign != '':
        print(f'Callsign: {flight.callsign}')
    if flight.registration != '':
         print(f'Registration: {flight.registration}')
    if airline != '':
         print(f'Airline: {airline}')
    if flight.number != '':
        print(f'Flight number: {flight.number}')
    if flight.origin_airport_iata != '' or flight.destination_airport_iata != '':
        try:
            origin = f'{details["airport"]["origin"]["name"]} ({flight.origin_airport_iata})'
        except (TypeError):
            origin = 'None'
        try:
            destination = f'{details["airport"]["destination"]["name"]} ({flight.destination_airport_iata})'
        except (TypeError):
            destination = 'None'
        print(f'{origin} → {destination}')
    if aircraft != '':
         print(f'Aircraft: {aircraft}')
    if flight.altitude != '':
        print(f'Altitude: {flight.altitude}ft')
    print()

    # generate qr code
    link = f'flightradar24.com/{flight.callsign}'
    img = qrcode.make(link)
    img.save("fr24_qrcode.png")

except (IndexError):
    print('No plane found.')
