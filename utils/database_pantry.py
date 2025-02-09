from collections import deque
import requests
from configuration import PANTRY_ID, MAX_MESSAGE

BASE_URL = f"https://getpantry.cloud/apiv1/pantry/{PANTRY_ID}"
headers = {"Content-Type": "application/json"}


def create_basket(basket_name: str):
    """Create a new basket in Pantry."""
    data = {}
    response = requests.post(f"{BASE_URL}/basket/{basket_name}", headers=headers, json=data, timeout=10)
    response.raise_for_status()
    if response.status_code == 200:
        print(f"The basket name '{basket_name}' has successfully been created")
    elif response.status_code != 200:
        raise ValueError(f"The basket name '{basket_name}' maybe has already been created")


def store_data(basket_name: str, data: dict):
    """Store data in Pantry under the given basket name."""
    payload = {key: list(value) if isinstance(value, deque) else value for key, value in data.items()}
    response = requests.put(url=f"{BASE_URL}/basket/{basket_name}", headers=headers, json=payload, timeout=10)
    if response.status_code == 200:
        print(f"The data has successfully been stored at {basket_name}")
    elif response.status_code != 200:
        raise ValueError(f"The basket name '{basket_name}' has not been created so there is no data to be stored")


def retrieve_data(basket_name: str) -> dict:
    """Retrieve data from Pantry for the given basket name."""
    response = requests.get(url=f"{BASE_URL}/basket/{basket_name}", headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        return {key: deque(value, maxlen=MAX_MESSAGE) if isinstance(value, list) else value for key, value in data.items()}
    elif response.status_code != 200:
        raise ValueError(f"The basket name '{basket_name}' has not been created so there is no data to be retrieved")


def delete_basket(basket_name: str):
    """Delete data from Pantry for the given basket name."""
    response = requests.delete(url=f"{BASE_URL}/basket/{basket_name}", headers=headers, timeout=10)
    if response.status_code == 200:
        print(f"The basket name '{basket_name}' has successfully been deleted")
    elif response.status_code != 200:
        raise ValueError(f"The basket name '{basket_name}' has not been created so there is no data to be stored")
