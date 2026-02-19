def calculate_bill(total_units):
    # Example tariff (modify based on your country)
    if total_units <= 100:
        rate = 1.5
    elif total_units <= 300:
        rate = 3.0
    else:
        rate = 5.0

    return total_units * rate
