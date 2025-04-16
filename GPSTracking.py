# 301 API project

CO2pergallon = 20 #lbs of CO2 emitted per gallon of gasoline

mpgavgCar = 24.4
mpgavgBus = 6.5 
pmpgavgTrain = 141.4 #passenger mpg of transit train


SupportedFOT = ["Car" , "Bus", "Train", "Walk", "Bike"]

#Get input (will be from google maps)
buspassengers = 25 #avg number of seats per bus
railpassengers = 600 #avg number of seats on transit rail
distance = float(input("Distance (miles): "))
origFOT = input("Form of Transportation (Car, Bus, Train, Walk, Bike): ")

if origFOT in SupportedFOT:
    pass
else:
    print("Form of Transportation not supported")

#Temporary cost values (USD)
CostDict = {
    "Car": 15,
    "Bus": 18,
    "Train": 18,
    "Walk": 0,
    "Bike": 0
}

#Temporary time values (minutes)
TimeDict = {
    "Car": 18,
    "Bus": 25,
    "Train": 30,
    "Walk": 100,
    "Bike": 65,
}

def GetCO2Em(FOT):
    if FOT == "Car":
        fuelUse = mpgavgCar / distance # total fuel use
        CO2Em = fuelUse * CO2pergallon # total CO2 Emissions
        return CO2Em
    elif FOT == "Bus":
        fuelUse = mpgavgCar / distance
        CO2Em = fuelUse * CO2pergallon / buspassengers
        return CO2Em
    elif FOT == "Train":
        fuelUse = pmpgavgTrain / distance
        CO2Em = fuelUse * CO2pergallon / railpassengers
        return CO2Em
    elif FOT == ("Walk" or "Bike"):
        return 0
    else:
        return float('inf')


CO2EmDict = {mode: GetCO2Em(mode) for mode in SupportedFOT}

origCO2Em = CO2EmDict[origFOT]
origCost = CostDict[origFOT]
origTime = TimeDict[origFOT]

candidates = []
for mode in SupportedFOT:
    if mode == origFOT:
        continue
    if distance > 1.5 and mode in ["Walk","Bike"]:
        continue
    if CostDict[mode] > 2 * origCost:
        continue
    if TimeDict[mode] > 2 * origTime:
        continue
    candidates.append(mode)

if candidates:
    best_alt = min(candidates, key=lambda m: CO2EmDict[m])
    print(f"Suggested alternative: {best_alt}")
    print(f"Original CO2 Emissions: {CO2EmDict[origFOT]:.2f} lbs")
    print(f"Alternative CO2 Emissions: {CO2EmDict[best_alt]:.2f} lbs")
    print(f"Cost Difference: ${(CostDict[origFOT] - CostDict[best_alt]):.2f}")
else:
    print("No better alternative available based on your preferences.")