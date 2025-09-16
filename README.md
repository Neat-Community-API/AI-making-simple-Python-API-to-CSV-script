# Neat.no Pulse API Data Collection Script

## Overview
This Python script polls the Neat.no Pulse API to collect sensor data from all rooms and exports the data to a CSV file. The script performs 10 API calls with 30-second intervals between calls to gather comprehensive sensor data.

## Prerequisites
- Python 3.x
- Neat.no Pulse API access (API key and Organization ID)

## Setup Instructions

### 1. Create Virtual Environment
It's recommended to use a virtual environment to isolate project dependencies:

**Using python3:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Using python:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
1. Open the `env_example` file in your preferred text editor
2. Replace the placeholder values with your actual credentials:
   ```
   API_KEY=your_actual_bearer_token
   ORG_ID=your_actual_organization_id
   ```
3. Rename the `env_example` file to `.env`

### 4. Obtaining API Credentials
To obtain your API credentials from Neat.no:
- Contact Neat.no support or your system administrator
- You will need both an API key (bearer token) and your Organization ID
- The API key should be provided as a bearer token for authentication
- The Organization ID is used in the API endpoint URL

## Usage Instructions

### Running the Script
```bash
python main.py
```

### What the Script Does
- Makes 10 API calls to the Neat.no Pulse sensor endpoint
- Waits 30 seconds between each API call
- Continues processing even if individual API calls fail
- Processes all collected sensor data into a flat CSV format
- Exports results to `sensor_data_export.csv`

### Expected Runtime
Approximately 5 minutes (due to 30-second intervals between API calls)

## Output Description

### CSV File Structure
The script creates a file named `sensor_data_export.csv` with the following columns:

| Column | Description |
|--------|-------------|
| poll_number | Which poll iteration (1-10) |
| room_id | Room ID from API response |
| timestamp | Sensor timestamp |
| co2 | CO2 reading |
| humidity | Humidity reading |
| illumination | Illumination reading |
| people | People count |
| temp | Temperature reading |
| voc | VOC reading |
| vocIndex | VOC Index reading |
| shutterClosed | Shutter status (true/false) |

### Data Format
- One row per room per poll
- Data from successful API calls only
- Rooms with null roomData are skipped

## Troubleshooting

### Common Issues

**Missing environment variables:**
```
Error: API_KEY and ORG_ID must be set in .env file
```
- Solution: Ensure your `.env` file contains valid API_KEY and ORG_ID values

**API authentication issues:**
```
API call failed: 401 Unauthorized
```
- Solution: Verify your API_KEY is correct and has proper permissions

**Network connectivity problems:**
```
API call failed: Connection timeout
```
- Solution: Check your internet connection and try again

**No data exported:**
```
No data to export.
```
- Solution: This indicates all API calls failed. Check your credentials and network connection

## File Structure
```
.
├── main.py              # Main Python script
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (credentials)
├── README.md           # This file
└── sensor_data_export.csv  # Output file (created after running script)
```
