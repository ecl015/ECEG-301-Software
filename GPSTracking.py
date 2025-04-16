import tkinter as tk
from tkinter import scrolledtext
import googlemaps
import re

# Replace YOUR_API_KEY with your actual Google Maps API key
gmaps = googlemaps.Client(key="AIzaSyBzM03Ll7lH_xDncVgJufhLiKpY9d8PZyc")

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
        output.insert(tk.END, f"Error: {e}")

# Set up GUI
window = tk.Tk()
window.title("GPS Directions")
window.geometry("600x400")

tk.Label(window, text="Start Address:").pack()
start_entry = tk.Entry(window, width=50)
start_entry.pack()

tk.Label(window, text="End Address:").pack()
end_entry = tk.Entry(window, width=50)
end_entry.pack()

tk.Button(window, text="Get Directions", command=get_directions).pack(pady=10)

output = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=15)
output.pack()

window.mainloop()
