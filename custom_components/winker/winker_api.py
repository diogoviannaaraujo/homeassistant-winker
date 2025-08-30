import aiohttp

class WinkerAPI:
    """Class to interact with the door control API."""

    def __init__(self, token=None):
        """Initialize the API client."""
        self.base_url = "https://api.winker.com.br/v1"
        self.token = token

    async def authenticate(self, email, password):
        """Authenticate with email and password to get a token."""
        # Device info that matches the working request
        device_info = {
            "model": "iPad8,6",
            "platform": "iOS",
            "uuid": "B3090523-D7E6-5903-8D0F-3D3B6E1535E7",
            "version": "18.6",
            "manufacturer": "Apple",
            "isVirtual": False,
            "serial": "unknown",
        }
        
        auth_data = {
            "username": email,
            "password": password,
            "key": "95948139456726945478756737323318116352",
            "version": "2.2.33",
            "device": device_info,
        }

        # Headers that match the working request from Proxyman
        headers = {
            "Accept": "application/json",
            "app-version": "2.2.33",
            "has-category": "",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Origin": "ionic://localhost",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "Connection": "keep-alive",
            "device": f'{{"model":"{device_info["model"]}","platform":"{device_info["platform"]}","uuid":"{device_info["uuid"]}","version":"{device_info["version"]}","manufacturer":"{device_info["manufacturer"]}","isVirtual":{str(device_info["isVirtual"]).lower()},"serial":"{device_info["serial"]}"}}',
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/auth/login", 
                json=auth_data,
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    # Assuming the API returns a token in the response
                    self.token = data.get("token")
                    return self.token
                else:
                     # Print the error response body for debugging
                     try:
                         error_data = await response.json()
                         print(f"Error response (JSON): {error_data}")
                     except:
                         error_text = await response.text()
                         print(f"Error response (Text): {error_text}")
                     print(f"Response status: {response.status}")
                     return None

    async def fetch_doors(self):
        """Fetch the list of doors from the API."""
        headers = {
            "Authorization": self.token
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/access-control/user/devices?id_portal=291",
                headers=headers,
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data  # Assuming the API returns a list of door details
                else:
                    return []

    async def open_door(self, door):
        """Send a request to open the door with the given ID."""
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }
        body = {
            "device": door,  # Pass the door ID in the JSON body
            "id_portal": 291,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/access-control/user/device/open",
                headers=headers,
                json=body,
            ) as response:
                if response.status == 200:
                    return True
                else:
                    return False

    async def fetch_cameras(self):
        headers = {
            "Authorization": self.token,
            "Accept": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/camera?id_portal=291&active=1", headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data  # Assuming the API returns a list of camera details
                else:
                    print(response.status)
                    return []

    async def fetch_camera(self, camera_id):
        headers = {
            "Authorization": self.token,
            "Accept": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/camera/{camera_id}", headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    print(response.status)
                    return None

    async def start_camera(self, camera_id):
        headers = {
            "Authorization": self.token,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/camera/{camera_id}/start", headers=headers
            ) as response:
                if response.status == 204:
                    return True
                else:
                    return False
