import googlemaps

# Initialize client with your API key
gmaps = googlemaps.Client(key="AIzaSyCE56MaLTB5vYb5q05PESU2a872RUCLslk")  

def test_route_distance(start, end, mode):
    try:
        directions = gmaps.directions(start, end, mode=mode)
        
        if not directions:
            print(f"❌ No {mode} route found between {start} and {end}")
            return None
            
        distance_m = directions[0]['legs'][0]['distance']['value']
        distance_km = distance_m / 1000
        distance_miles = distance_m / 1609.34
        
        print(f"✅ {mode.upper()} route found:")
        print(f"From: {directions[0]['legs'][0]['start_address']}")
        print(f"To: {directions[0]['legs'][0]['end_address']}")
        print(f"Distance: {distance_m:,} m | {distance_km:.2f} km | {distance_miles:.2f} miles")
        print(f"Duration: {directions[0]['legs'][0]['duration']['text']}\n")
        
        return distance_miles
        
    except Exception as e:
        print(f"❌ Error getting {mode} directions: {str(e)}")
        return None

# Test cases
test_routes = [
    ("Statue of Liberty", "Times Square", "walking"),
    ("Disneyland", "Universal Studios Hollywood", "driving"),
    ("London Eye", "Buckingham Palace", "bicycling"),
    ("Eiffel Tower", "Louvre Museum", "transit")
]

for start, end, mode in test_routes:
    test_route_distance(start, end, mode)