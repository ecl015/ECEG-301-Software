import tkinter as tk
from tkinter import scrolledtext
import googlemaps
import re
from emissions_logic import suggest_alternative

# Initialize Google Maps API client
gmaps = googlemaps.Client(key="AIzaSyCE56MaLTB5vYb5q05PESU2a872RUCLslk")  

def get_route_info(start, end, mode='driving'):
    """Get distance and duration for a route"""
    try:
        directions = gmaps.directions(start, end, mode=mode)
        if not directions:
            return None
            
        leg = directions[0]['legs'][0]
        return {
            'distance': leg['distance']['value'] / 1609.34,  # Convert meters to miles
            'duration': leg['duration']['value'] / 3600,     # Convert seconds to hours
            'mode': mode
        }
    except Exception as e:
        print(f"Error getting {mode} directions:", e)
        return None
    
def get_directions():
    start = start_entry.get()
    end = end_entry.get()
    try:
        directions = gmaps.directions(start, end, mode="driving")
        steps = directions[0]['legs'][0]['steps']
        output.delete('1.0', tk.END)
        for step in steps:
            instruction = step['html_instructions']
            clean_instruction = re.sub(r'<.*?>', '', instruction)
            output.insert(tk.END, clean_instruction + '\n')
    except Exception as e:
        output.delete('1.0', tk.END)
        output.insert(tk.END, f"Error getting directions: {e}\n")

def get_suggestion():
    """Get transportation suggestion with proper distance calculation"""
    start = start_entry.get()
    end = end_entry.get()
    transport = transport_entry.get().lower()
    priority = priority_entry.get().lower()
    
    # Validate inputs
    valid_transport = ["car", "bus", "train", "walk", "bike"]
    valid_priorities = ["emissions", "cost", "time"]
    
    if transport not in valid_transport:
        output.delete('1.0', tk.END)
        output.insert(tk.END, f"Invalid transport. Choose from: {', '.join(valid_transport)}\n")
        return
        
    if priority not in valid_priorities:
        output.delete('1.0', tk.END)
        output.insert(tk.END, f"Invalid priority. Choose from: {', '.join(valid_priorities)}\n")
        return

    output.delete('1.0', tk.END)
    output.insert(tk.END, "Calculating route...\n")
    window.update_idletasks()  # Update GUI immediately
    
    try:
        # Get route info for requested transport mode
        route_info = get_route_info(start, end, transport)
        
        # Fallback to driving if needed
        if not route_info and transport != 'driving':
            output.insert(tk.END, f"No {transport} route found, trying driving...\n")
            route_info = get_route_info(start, end, 'driving')
            
        if not route_info:
            output.insert(tk.END, "Error: Could not calculate any route\n")
            return
            
        # Display basic route info
        output.insert(tk.END,
            f"\nROUTE INFO:\n"
            f"Distance: {route_info['distance']:.2f} miles\n"
            f"Duration: {route_info['duration']:.2f} hours\n"
            f"Mode: {route_info['mode']}\n\n")
            
        # Get suggestion from emissions logic
        suggestion = suggest_alternative(route_info['distance'], transport, priority)
        
        # Display suggestion
        if "error" in suggestion:
            output.insert(tk.END, f"Error: {suggestion['error']}\n")
        elif "message" in suggestion:
            output.insert(tk.END, suggestion['message'] + "\n")
        else:
            output.insert(tk.END,
                f"SUGGESTION:\n"
                f"Recommended: {suggestion['suggested'].capitalize()}\n"
                f"CO2 Savings: {suggestion['original_emissions'] - suggestion['alternative_emissions']:.2f} lbs\n"
                f"Cost Savings: ${suggestion['cost_savings']:.2f}\n"
                f"Time Difference: {suggestion['time_savings']:.2f} hours\n")
                
    except Exception as e:
        output.delete('1.0', tk.END)
        output.insert(tk.END, f"Error: {str(e)}\n")

# GUI Setup
window = tk.Tk()
window.title("Transportation Suggestion System")
window.geometry("700x700")

# Input fields
tk.Label(window, text="Start Address:").pack()
start_entry = tk.Entry(window, width=60)
start_entry.pack()

tk.Label(window, text="End Address:").pack()
end_entry = tk.Entry(window, width=60)
end_entry.pack()

tk.Label(window, text="Current Transport Mode (car, bus, train, walk, bike):").pack()
transport_entry = tk.Entry(window, width=30)
transport_entry.insert(0, "car")  # Default value
transport_entry.pack()

tk.Label(window, text="Priority (emissions, cost, or time):").pack()
priority_entry = tk.Entry(window, width=30)
priority_entry.insert(0, "emissions")  # Default value
priority_entry.pack()

# Buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Get Driving Directions", command=get_directions).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Get Transport Suggestions", command=get_suggestion).pack(side=tk.LEFT, padx=5)

# Output area
output = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=25)
output.pack(pady=10)

window.mainloop()