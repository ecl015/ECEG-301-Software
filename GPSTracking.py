import tkinter as tk
from tkinter import scrolledtext
import googlemaps
import re

# Replace YOUR_API_KEY with your actual Google Maps API key
gmaps = googlemaps.Client(key="AIzaSyBzM03Ll7lH_xDncVgJufhLiKpY9d8PZyc")

def getEmissions():
    #Constants and averages. Can be altered to increase accuracy
    CO2pergallon = 20 #lbs of CO2 emitted per gallon of gasoline
    mpgavgCar = 24.4
    mpgavgBus = 6.5 
    mpgppavgTrain = 52 #passenger mpg per passenger of transit train

    SupportedFOT = ["Car" , "Bus", "Train", "Walk", "Bike"]

    #Get input (temporary)
    buspassengers = 25 #avg number of seats per bus
    distance = float(input("Distance (miles): "))
    origFOT = (input("Form of Transportation (Car, Bus, Train, Walk, Bike): ")).capitalize()
    priority = (input("Priority (Cost, Emissions, Time): ")).capitalize()


    # Should change this when data is retrieved from maps
    if origFOT in SupportedFOT:
        pass
    else:
        print("Form of Transportation not supported")
        exit()


    #Temporary cost values (USD)
    #Should retrieve from API
    CostDict = {
        "Car": 15,
        "Bus": 18,
        "Train": 18,
        "Walk": 0,
        "Bike": 0
    }

    #Temporary time values (minutes) distance / avg speed
    #Should retrieve from API
    TimeDict = {
        "Car": distance / 35, 
        "Bus": distance / 25, 
        "Train": distance / 40, 
        "Walk": distance / 4,
        "Bike": distance / 10,
    }

    def GetCO2Em(FOT):
        if FOT == "Car":
            fuelUse = distance / mpgavgCar # total fuel use
            CO2Em = CO2pergallon * fuelUse # total CO2 Emissions
            return CO2Em
        elif FOT == "Bus":
            fuelUse = distance / mpgavgBus
            CO2Em =  CO2pergallon * fuelUse / buspassengers
            return CO2Em
        elif FOT == "Train":
            fuelUse = distance / mpgppavgTrain
            CO2Em = CO2pergallon * fuelUse
            return CO2Em
        elif FOT == ("Walk" or "Bike"):
            return 0
        else:
            return float('inf') # Should change?


    CO2EmDict = {mode: GetCO2Em(mode) for mode in SupportedFOT}

    origCO2Em = CO2EmDict[origFOT]
    origCost = CostDict[origFOT]
    origTime = TimeDict[origFOT]

    candidates = []
    for mode in SupportedFOT:
        if (distance > 1.5) and (mode in ["Walk","Bike"]):
            continue
        if (priority == "Cost") and (CostDict[mode] > 2 * origCost):
            continue
        if (priority == "Time") and (TimeDict[mode] > 2 * origTime):
            continue
        candidates.append(mode)

    if priority == "Emissions":
        best_alt = min(candidates, key=lambda m: CO2EmDict[m])
    elif priority == "Cost":
        best_alt = min(candidates, key=lambda m: CostDict[m])
    elif priority == "Time":
        best_alt = min(candidates, key=lambda m: TimeDict[m])
    else:
        print("Invalid option")
        exit()
        
    if best_alt == origFOT:
        print("No better alternative available based on your preferences.")
    else:
        print(f"Suggested alternative: {best_alt}")
        print(f"Original CO2 Emissions: {CO2EmDict[origFOT]:.2f} lbs")
        print(f"Alternative CO2 Emissions: {CO2EmDict[best_alt]:.2f} lbs")
        print(f"Cost Save: ${(origCost - CostDict[best_alt]):.2f}")
        print(f'Time Save: {(origTime - TimeDict[best_alt]):.2f} minutes')


# UI setup
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

tk.Label(window, text="Form of Transportation (Car, Bus, Train, Walk, Bike):").pack()
transport = tk.Entry(window, width=50)
transport.pack()

tk.Label(window, text="Priority (Cost, Emissions, Time):").pack()
priority = tk.Entry(window, width=50)
priority.pack()

tk.Button(window, text="Get Directions", command=get_directions).pack(pady=10)

output = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=15)
output.pack()

window.mainloop()
