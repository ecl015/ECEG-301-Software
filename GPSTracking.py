# 301 API project


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
    if FOT.lower() == "Car":
        fuelUse = distance / mpgavgCar # total fuel use
        CO2Em = CO2pergallon * fuelUse # total CO2 Emissions
        return CO2Em
    elif FOT.lower() == "Bus":
        fuelUse = distance / mpgavgBus
        CO2Em =  CO2pergallon * fuelUse / buspassengers
        return CO2Em
    elif FOT.lower() == "Train":
        fuelUse = distance / mpgppavgTrain
        CO2Em = CO2pergallon * fuelUse
        return CO2Em
    elif FOT.lower() == ("Walk" or "Bike"):
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

if best_alt == origFOT:
    print("No better alternative available based on your preferences.")
else:
    print(f"Suggested alternative: {best_alt.capitalize()}")
    print(f"Original CO2 Emissions: {CO2EmDict[origFOT]:.2f} lbs")
    print(f"Alternative CO2 Emissions: {CO2EmDict[best_alt]:.2f} lbs")
    print(f"Cost Save: ${(origCost - CostDict[best_alt]):.2f}")
    print(f'Time Save: {(origTime - TimeDict[best_alt]):.2f} minutes')

