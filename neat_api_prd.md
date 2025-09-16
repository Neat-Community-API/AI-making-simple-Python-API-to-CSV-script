# Product Requirements Document: Neat.no Pulse API Data Collection Script

## Overview
Create a Python script that polls the Neat.no Pulse API to collect sensor data from all rooms and export the data to a CSV file.

## Requirements

### Files to Create
1. **`main.py`** - Main Python script
2. **`requirements.txt`** - Python dependencies
3. **`.env`** - Environment variables (template/example)
4. **`README.md`** - Usage instructions and setup guide

### Functional Requirements

#### API Integration
- **Endpoint**: `https://api.pulse.neat.no/v1/orgs/{orgid}/rooms/sensor`
- **Method**: GET request to bulk sensor data endpoint
- **Authentication**: Bearer token (API key from environment variables)
- **URL Parameter**: Organization ID from environment variables (used in URL path)

#### Polling Logic
- Perform exactly **10 API calls** to the bulk sensor data endpoint
- Wait **30 seconds** between each API call
- Continue with remaining polls even if individual API calls fail
- Collect all successful responses before processing

#### Data Processing
- Process raw API response data without modification
- Handle the nested JSON structure:
  ```json
  {
    "data": [
      {
        "id": integer,
        "roomData": {
          "data": [
            {
              "co2": number,
              "humidity": number,
              "illumination": number,
              "people": integer,
              "temp": number,
              "timestamp": string,
              "voc": number,
              "vocIndex": number
            }
          ],
          "shutterClosed": boolean
        }
      }
    ]
  }
  ```

#### CSV Export
- **Structure**: One row per room per poll
- **Columns** (in order):
  - `poll_number` - Which poll iteration (1-10)
  - `room_id` - Room ID from API response
  - `timestamp` - Sensor timestamp
  - `co2` - CO2 reading
  - `humidity` - Humidity reading
  - `illumination` - Illumination reading
  - `people` - People count
  - `temp` - Temperature reading
  - `voc` - VOC reading
  - `vocIndex` - VOC Index reading
  - `shutterClosed` - Shutter status (boolean)
- **Filename**: `sensor_data_export.csv`
- **Format**: Standard CSV with headers

### Technical Requirements

#### Environment Variables (.env file)
```
API_KEY=your_bearer_token_here
ORG_ID=your_organization_id_here
```

#### Dependencies (requirements.txt)
- `requests` - For HTTP API calls
- `python-dotenv` - For loading environment variables
- `pandas` - For CSV creation and data handling

#### Code Structure
- Simple, straightforward implementation
- No logging, testing, or advanced error handling
- Basic error handling: continue on API failures, print simple error messages
- Use standard libraries and the specified dependencies only
- **Important**: Handle cases where `roomData` is `None` - skip rooms with null roomData and continue processing

### Script Behavior
1. Load environment variables from `.env` file
2. Perform 10 API calls with 30-second intervals
3. Collect all successful responses
4. Process nested JSON data into flat rows
5. Export to CSV file
6. Print completion message

### Non-Requirements
- No advanced logging mechanisms
- No unit tests or test files
- No configuration files beyond .env
- No data validation or cleaning
- No retry logic for failed requests
- No progress bars or verbose output

### Documentation Requirements

#### README.md File
Create a comprehensive README file that includes:

**Project Overview**
- Brief description of what the script does
- Purpose: polling Neat.no Pulse API for sensor data

**Prerequisites** 
- Python 3.x requirement
- Neat.no Pulse API access (API key and Organization ID)

**Setup Instructions**
- Step-by-step installation process:
  1. Clone/download the project files
  2. Install dependencies: `pip install -r requirements.txt`
  3. Configure environment variables in `.env` file
- Clear instructions on how to obtain API credentials from Neat.no
- Example `.env` file format with placeholder values

**Usage Instructions**
- How to run the script: `python main.py`
- What the script does (10 polls, 30-second intervals)
- Expected output (CSV file location and name)
- Estimated runtime (approximately 5 minutes)

**Output Description**
- CSV file structure and column descriptions
- Location of output file (`sensor_data_export.csv`)
- Data format explanation (one row per room per poll)

**Troubleshooting**
- Common error scenarios and solutions
- API authentication issues
- Network connectivity problems
- Missing environment variables

**File Structure**
- List of all project files and their purposes

Keep the README concise but comprehensive, suitable for both technical and non-technical users.
- **roomData can be None**: Some API responses may contain rooms where `roomData` is `None`. The script should check for this condition and skip those rooms rather than attempting to call `.get()` on a None object. Use pattern:
  ```python
  room_data = room.get('roomData')
  if room_data is None:
      continue
  ```
- **Base URL**: `https://api.pulse.neat.no`
- **Full Endpoint**: `https://api.pulse.neat.no/v1/orgs/{orgid}/rooms/sensor`
- **Authentication**: Bearer token in Authorization header
- **URL Parameter**: Organization ID (replace {orgid} in URL)
- **Response Format**: JSON with nested structure as shown above

## Success Criteria
- Script successfully makes 10 API calls with 30-second delays
- All sensor data is correctly flattened and exported to CSV
- CSV contains one row per room per successful poll
- Environment variables are properly loaded and used
- Script handles API failures gracefully and continues processing