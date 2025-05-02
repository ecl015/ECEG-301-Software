from emissions_logic import suggest_alternative

# Test cases
test_cases = [
    (1, "car", "emissions"),  # Short distance
    (10, "car", "cost"),      # Medium distance
    (50, "bus", "time"),      # Long distance
    (100, "car", "time")      # Edge case
]

for distance, mode, priority in test_cases:
    print(f"\nTesting: {distance} miles, mode={mode}, priority={priority}")
    result = suggest_alternative(distance, mode, priority)
    print(result)