import os
import json
import requests
import colorama
from colorama import Fore
import ctypes

colorama.init()
os.system('mode con: cols=85 lines=28')
ctypes.windll.kernel32.SetConsoleTitleW('IP Lookup Tool | Created by Ali')

def sanitize_filename(filename):
    """Sanitize filenames by replacing invalid characters with underscores."""
    return ''.join(c if c.isalnum() or c in (' ', '_') else '_' for c in filename)

def save_json_data(filepath, data):
    """Save data to a JSON file."""
    os.makedirs('saved', exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_config(filepath='./data/config.json'):
    """Load configuration from a JSON file."""
    with open(filepath, 'r') as file:
        return json.load(file)

def fetch_ip_info():
    """Fetch and display IP information."""
    config = load_config()

    while True:
        ip_address = input(f"{Fore.LIGHTYELLOW_EX}[{Fore.RESET}+{Fore.LIGHTYELLOW_EX}] Enter the IP address: {Fore.RESET}")
        url = f"https://freeipapi.com/api/json/{ip_address}"
        headers = {
            'accept': 'application/json',
            'accept-language': 'en',
            'user-agent': 'ios:2.65.0:488:14:iPhone13,3',
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            if not data.get('success', True):
                message = data.get('message', '').lower()
                if 'invalid ip address' in message:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"{Fore.LIGHTRED_EX}[{Fore.RESET}-{Fore.LIGHTRED_EX}] Error: Invalid IP address. Please try again.")
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"{Fore.LIGHTRED_EX}[{Fore.RESET}-{Fore.LIGHTRED_EX}] Error: {message.capitalize()}. Please try again.")
                continue

            essential_fields = ["ipVersion", "ipAddress"]
            if any(not data.get(field) for field in essential_fields):
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"{Fore.LIGHTRED_EX}[{Fore.RESET}-{Fore.LIGHTRED_EX}] Error: Incomplete server data. Please try again.")
                continue

            fields = {
                "IP Version": data.get("ipVersion", "Not found"),
                "IP Address": data.get("ipAddress", "Not found"),
                "Latitude": data.get("latitude", "Not found"),
                "Longitude": data.get("longitude", "Not found"),
                "Country": f"{data.get('countryName', 'Not found')} ({data.get('countryCode', 'Not found')})",
                "Time Zone": data.get("timeZone", "Not found"),
                "ZIP Code": data.get("zipCode", "Not found"),
                "City": data.get("cityName", "Not found"),
                "Region": data.get("regionName", "Not found"),
                "Is Proxy": data.get("isProxy", "Not found"),
                "Continent": f"{data.get('continent', 'Not found')} ({data.get('continentCode', 'Not found')})",
                "Currency": f"{data.get('currency', {}).get('name', 'Not found')} ({data.get('currency', {}).get('code', 'Not found')})",
                "Language": data.get("language", "Not found"),
                "Time Zones": ", ".join(data.get("timeZones", [])) or "Not found",
                "TLDs": ", ".join(data.get("tlds", [])) or "Not found",
                "Google Maps Location": f"https://www.google.com/maps/search/?api=1&query={data.get('latitude', '0')},{data.get('longitude', '0')}"
            }

            if config.get("save_ip_json", False):
                filename = f"{sanitize_filename(ip_address)}.json"
                save_json_data(os.path.join('saved', filename), fields)

            os.system('cls' if os.name == 'nt' else 'clear')
            for key, value in fields.items():
                print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] {key}: {Fore.RESET}{value}")

            break

        except requests.RequestException as e:
            print(f"{Fore.LIGHTRED_EX}[{Fore.RESET}-{Fore.LIGHTRED_EX}] Request error: {str(e)}. Please try again.")

    input(f"{Fore.LIGHTYELLOW_EX}Press Enter to exit...")

if __name__ == "__main__":
    fetch_ip_info()