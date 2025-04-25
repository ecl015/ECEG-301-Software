# 301 API project


#Constants and averages. Can be altered to increase accuracy
CO2pergallon = 20 #lbs of CO2 emitted per gallon of gasoline
mpgavgCar = 24.4
mpgavgBus = 6.5 
mpgppavgTrain = 52 #passenger mpg per passenger of transit train


SupportedFOT = ["car" , "bus", "train", "walk", "bike"]

#Get input (temporary)
buspassengers = 25 #avg number of seats per bus
distance = float(input("Distance (miles): "))
origFOT = (input("Form of Transportation (Car, Bus, Train, Walk, Bike): ")).lower()
priority = (input("Priority (Cost, Emissions, Time): ")).lower()


# Should change this when data is retrieved from maps
if origFOT in SupportedFOT:
    pass
else:
    print("Form of Transportation not supported")


#Temporary cost values (USD)
#Should retrieve from API
CostDict = {
    "car": 15,
    "bus": 18,
    "train": 18,
    "walk": 0,
    "bike": 0
}

#Temporary time values (minutes) distance / avg speed
#Should retrieve from API
TimeDict = {
    "car": distance / 35, 
    "bus": distance / 25, 
    "train": distance / 40, 
    "walk": distance / 4,
    "bike": distance / 10,
}

def GetCO2Em(FOT):
    if FOT.lower() == "car":
        fuelUse = distance / mpgavgCar # total fuel use
        CO2Em = CO2pergallon * fuelUse # total CO2 Emissions
        return CO2Em
    elif FOT.lower() == "bus":
        fuelUse = distance / mpgavgBus
        CO2Em =  CO2pergallon * fuelUse / buspassengers
        return CO2Em
    elif FOT.lower() == "train":
        fuelUse = distance / mpgppavgTrain
        CO2Em = CO2pergallon * fuelUse
        return CO2Em
    elif FOT.lower() == ("walk" or "bike"):
        return 0
    else:
        return float('inf') # Should change?


CO2EmDict = {mode: GetCO2Em(mode) for mode in SupportedFOT}

origCO2Em = CO2EmDict[origFOT]
origCost = CostDict[origFOT]
origTime = TimeDict[origFOT]

candidates = []
for mode in SupportedFOT:
    if (distance > 1.5) and (mode in ["walk","bike"]):
        continue
    if (priority.lower() == "cost") and (CostDict[mode] > 2 * origCost):
        continue
    if (priority.lower() == "time") and (TimeDict[mode] > 2 * origTime):
        continue
    candidates.append(mode)

if priority.lower() == "emissions":
    best_alt = min(candidates, key=lambda m: CO2EmDict[m])
elif priority.lower() == "cost":
    best_alt = min(candidates, key=lambda m: CostDict[m])
elif priority.lower() == "time":
    best_alt = min(candidates, key=lambda m: TimeDict[m])
else:
    print("Invalid option")

if best_alt == origFOT:
    print("No better alternative available based on your preferences.")
else:
    print(f"Suggested alternative: {best_alt.capitalize()}")
    print(f"Original CO2 Emissions: {CO2EmDict[origFOT]:.2f} lbs")
    print(f"Alternative CO2 Emissions: {CO2EmDict[best_alt]:.2f} lbs")
    print(f"Cost Save: ${(origCost - CostDict[best_alt]):.2f}")
    print(f'Time Save: {(origTime - TimeDict[best_alt]):.2f} minutes')
