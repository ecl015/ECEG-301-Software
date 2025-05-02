def suggest_alternative(distance, orig_mode, priority):
    # Constants
    CO2_PER_GALLON = 20  # lbs of CO2 emitted per gallon of gasoline
    MPG_AVG_CAR = 24.4
    MPG_AVG_BUS = 6.5
    MPG_PP_AVG_TRAIN = 52
    BUS_PASSENGERS = 25
    
    # Cost in dollars (updated with more realistic values)
    COST_DICT = {
        "car": 0.15 * distance,  # $0.15 per mile (gas + maintenance)
        "bus": 1.50 + 0.05 * distance,  # Base fare + distance charge
        "train": 2.00 + 0.10 * distance,
        "walk": 0,
        "bike": 0
    }
    
    # Average speeds in mph (updated for realism)
    SPEED_DICT = {
        "car": 35 if distance > 5 else 25,  # Lower speed for short distances
        "bus": 25 if distance > 3 else 15,
        "train": 40,
        "walk": 3,
        "bike": 10
    }
    
    # Time in hours
    TIME_DICT = {mode: distance / speed for mode, speed in SPEED_DICT.items()}
    
    def get_co2_emissions(mode):
        if mode == "car":
            fuel_used = distance / MPG_AVG_CAR
            return CO2_PER_GALLON * fuel_used
        elif mode == "bus":
            fuel_used = distance / MPG_AVG_BUS
            return (CO2_PER_GALLON * fuel_used) / BUS_PASSENGERS
        elif mode == "train":
            fuel_used = distance / MPG_PP_AVG_TRAIN
            return CO2_PER_GALLON * fuel_used
        elif mode in ["walk", "bike"]:
            return 0
        else:
            return float('inf')
    
    # Calculate emissions for all modes
    emissions = {mode: get_co2_emissions(mode) for mode in COST_DICT.keys()}
    
    # Filter out impractical options
    candidates = []
    for mode in COST_DICT.keys():
        # Skip walking/biking for long distances
        if distance > 5 and mode in ["walk", "bike"]:
            continue
            
        # Skip modes that are significantly worse by priority
        if priority == "cost" and COST_DICT[mode] > 1.5 * COST_DICT[orig_mode]:
            continue
        if priority == "time" and TIME_DICT[mode] > 1.5 * TIME_DICT[orig_mode]:
            continue
        candidates.append(mode)
    
    # Handle case where no candidates remain
    if not candidates:
        return {"error": "No suitable alternatives found"}
    
    # Select best alternative based on priority
    if priority == "emissions":
        best_alt = min(candidates, key=lambda m: emissions[m])
    elif priority == "cost":
        best_alt = min(candidates, key=lambda m: COST_DICT[m])
    elif priority == "time":
        best_alt = min(candidates, key=lambda m: TIME_DICT[m])
    else:
        return {"error": "Invalid priority specified"}
    
    # Prepare results
    if best_alt == orig_mode:
        return {
            "message": "Current mode is already optimal",
            "original_mode": orig_mode,
            "distance": distance,
            "priority": priority
        }
    else:
        return {
            "suggested": best_alt,
            "original_mode": orig_mode,
            "distance": distance,
            "priority": priority,
            "original_emissions": round(emissions[orig_mode], 2),
            "alternative_emissions": round(emissions[best_alt], 2),
            "original_cost": round(COST_DICT[orig_mode], 2),
            "alternative_cost": round(COST_DICT[best_alt], 2),
            "original_time": round(TIME_DICT[orig_mode], 2),
            "alternative_time": round(TIME_DICT[best_alt], 2),
            "cost_savings": round(COST_DICT[orig_mode] - COST_DICT[best_alt], 2),
            "time_savings": round(TIME_DICT[orig_mode] - TIME_DICT[best_alt], 2)
        }