import json

def format_price(value, decimals):
    try:
        number = int(value) / (10 ** int(decimals))
        return f"{number:,.{int(decimals)}f}"
    except:
        return "NaN"
        

def extract_required_data(data):
    rates = []
    for room in data.get('recommendedEntries'):
        for inventory in room.get('hotelRoomInventoryList'):
            inv_data = {}
            inv_data['room_name'] = room.get('name')
            inv_data['rate_name'] = 'Price/room/night'
            inv_data['shown_currency'] = inventory.get('rateDisplay').get('roomFareDisplays').get('currency')
            inv_data['cancellation_policy'] = inventory.get('roomCancellationPolicy').get('cancellationPolicyLabel')
            inv_data['breakfast'] = inventory.get('roomInventoryGroupOption')
            inv_data['number_of_guests'] = inventory.get('maxOccupancy')

            inv_data['shown_price'] = {'rate_name': 'Exclude taxes & fees'}

            decimals = inventory.get('rateDisplay').get('numOfDecimalPoint')

            total_price_per_stay = inventory.get('rateDisplay').get('totalFare').get('amount')
            shown_price_per_stay = inventory.get('rateDisplay').get('baseFare').get('amount')
            taxes_amount = inventory.get('rateDisplay').get('taxes').get('amount')

            original_total_price_per_stay = inventory.get('originalRateDisplay').get('totalFare').get('amount')
            original_shown_price_per_stay = inventory.get('originalRateDisplay').get('baseFare').get('amount')
            original_taxes_amount = inventory.get('originalRateDisplay').get('taxes').get('amount')

            inv_data['total_price_per_stay'] = format_price(total_price_per_stay, decimals)
            inv_data['shown_price_per_stay'] = format_price(shown_price_per_stay, decimals)
            inv_data['taxes_amount'] = format_price(taxes_amount, decimals)
            inv_data['original_total_price_per_stay'] = format_price(original_total_price_per_stay, decimals)
            inv_data['original_shown_price_per_stay'] = format_price(original_shown_price_per_stay, decimals)
            inv_data['original_taxes_amount'] = format_price(original_taxes_amount, decimals)

            rates.append(inv_data)

    return rates

def get_rates_file():
    try:
        with open("results/api_response.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            data = data.get('data')
            rates = extract_required_data(data)
            with open('results/rates.json', "w", encoding="utf-8") as w:
                json.dump(rates, w, indent=2)
    except FileNotFoundError:
        print("File 'api_response.json' is not found.")