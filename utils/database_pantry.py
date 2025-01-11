import os
import requests
from dotenv import load_dotenv

load_dotenv()

PANTRY_ID = os.environ.get("PANTRY_ID")
BASE_URL = f"https://getpantry.cloud/apiv1/pantry/{PANTRY_ID}"
headers = {"Content-Type": "application/json"}


def store_data(basket_name: str, data: dict):
    """Store data in Pantry under the given basket name."""
    response = requests.put(url=f"{BASE_URL}/basket/{basket_name}", headers=headers, json=data, timeout=10)
    if response.status_code == 200:
        print(f"The data has successfully been stored at {basket_name}")
    elif response.status_code != 200:
        raise ValueError(f"The basket name '{basket_name}' has not been created so there is no data to be stored")


def retrieve_data(basket_name: str) -> dict:
    """Retrieve data from Pantry for the given basket name."""
    response = requests.get(url=f"{BASE_URL}/basket/{basket_name}", headers=headers, timeout=10)
    if response.status_code == 200:
        return response.json()
    elif response.status_code != 200:
        raise ValueError(f"The basket name '{basket_name}' has not been created so there is no data to be retrieved")


def clear_data(basket_name: str):
    """Delete data from Pantry for the given basket name."""
    response = requests.delete(url=f"{BASE_URL}/basket/{basket_name}", headers=headers, timeout=10)
    if response.status_code == 200:
        print(f"The data on {basket_name} as successfully been deleted")
    elif response.status_code != 200:
        raise ValueError(f"The basket name '{basket_name}' has not been created so there is no data to be stored")
