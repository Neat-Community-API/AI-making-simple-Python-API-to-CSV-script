import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

def load_environment():
    load_dotenv()
    api_key = os.getenv('API_KEY')
    org_id = os.getenv('ORG_ID')

    if not api_key or not org_id:
        print("Error: API_KEY and ORG_ID must be set in .env file")
        exit(1)

    return api_key, org_id

def make_api_call(api_key, org_id):
    url = f"https://api.pulse.neat.no/v1/orgs/{org_id}/rooms/sensor"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        return None

def process_data(all_responses):
    rows = []

    for poll_number, response in enumerate(all_responses, 1):
        if response is None:
            continue

        data = response.get('data', [])

        for room in data:
            room_id = room.get('id')
            room_data = room.get('roomData')

            if room_data is None:
                continue

            shutter_closed = room_data.get('shutterClosed')
            sensor_data_list = room_data.get('data', [])

            for sensor_data in sensor_data_list:
                row = {
                    'poll_number': poll_number,
                    'room_id': room_id,
                    'timestamp': sensor_data.get('timestamp'),
                    'co2': sensor_data.get('co2'),
                    'humidity': sensor_data.get('humidity'),
                    'illumination': sensor_data.get('illumination'),
                    'people': sensor_data.get('people'),
                    'temp': sensor_data.get('temp'),
                    'voc': sensor_data.get('voc'),
                    'vocIndex': sensor_data.get('vocIndex'),
                    'shutterClosed': shutter_closed
                }
                rows.append(row)

    return rows

def export_to_csv(data, filename='sensor_data_export.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data exported to {filename}")

def main():
    api_key, org_id = load_environment()

    print("Starting data collection...")
    all_responses = []

    for poll in range(1, 11):
        print(f"Making API call {poll}/10...")
        response = make_api_call(api_key, org_id)
        all_responses.append(response)

        if poll < 10:
            time.sleep(30)

    print("Processing data...")
    processed_data = process_data(all_responses)

    if processed_data:
        export_to_csv(processed_data)
        print(f"Collection complete. Processed {len(processed_data)} data points.")
    else:
        print("No data to export.")

if __name__ == "__main__":
    main()