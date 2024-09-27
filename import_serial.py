import json
import serial
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Set up serial communication
ser = serial.Serial('/dev/ttyACM0', 9600) # Change '/dev/ttyACM0' to your serial port

# Set up Google Sheets API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/rami035/Arduino/credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('plant_data_inator').sheet1

def format_sensor_data(input_string):
    # Remove the leading '~' and trailing '|'
    json_string = input_string.strip('~|')

    try:
        # Parse the JSON string into a Python dictionary
        data = json.loads(json_string)

        # Extract the required values from the dictionary
        sensor_name = data['sensorName']
        value = data['value']
        unit = data['unit']

        # Format the output string based on the sensor name
        if sensor_name == 'ambient_temp':
            # Convert temperature from Celsius to Fahrenheit
            value_fahrenheit = (value * 9/5) + 32
            output_string = f"{value_fahrenheit:.2f}°F"
        elif sensor_name == 'Luminosity':
            output_string = f"{value} {unit}"
        else:
            output_string = None

        return sensor_name, output_string
    except json.JSONDecodeError:
        print(f"Invalid JSON data: {json_string}")
        return None, None

# Initialize variables to store the latest temperature and luminosity data
latest_temp = None
latest_lux = None
latest_timestamp = None

# Read from Arduino and Write to Google Sheets
while True:
    if ser.in_waiting:
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        data = ser.readline().decode('utf-8').rstrip()
        sensor_name, formatted_data = format_sensor_data(data)

        if sensor_name == 'ambient_temp':
            latest_temp = formatted_data
        elif sensor_name == 'Luminosity':
            latest_lux = formatted_data

        latest_timestamp = dt_string

        # Check if both temperature and luminosity data are available
        if latest_temp and latest_lux:
            sheet.insert_row([latest_timestamp, latest_temp, latest_lux], 2)
            print(f"Temperature: {latest_temp}, Luminosity: {latest_lux}")
            latest_temp = None
            latest_lux = None

            # Insert the temperature conversion formula at cell D2
            sheet.update_acell('D2', '=VALUE(LEFT(B2, LEN(B2)-2))')
            sheet.update_acell('E2', '=VALUE(LEFT(C2, LEN(C2)-4))')
            break