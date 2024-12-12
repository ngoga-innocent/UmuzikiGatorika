import requests
from requests.exceptions import RequestException
import time
from .models import Device
def send_push_notification(expo_push_token, title, body, data=None, retries=3, delay=5):
    url = "https://exp.host/--/api/v2/push/send"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json"
    }
    payload = {
        "to": expo_push_token,
        "sound": "default",
        "title": title,
        "body": body,
        "data":data or {"url": "umuzikiGatorika://home"}
    }

    for attempt in range(retries):
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                print("Notification sent successfully.")
                return response.json()  # Success case, returning response from Expo
            else:
                # Log or handle unsuccessful response
                print(f"Error: {response.status_code} - {response.text}")
                response.raise_for_status()  # Raise error for debugging if needed

        except RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:  # Wait before retrying
                time.sleep(delay)
            else:
                print("All attempts to send the notification have failed.")
                raise e  # Reraise exception if all retries fail

    return None  # Return None if all retries failed

def send_to_allDevice(title,body,data=None):
    devices=Device.objects.all()
    for device in devices:
        if device.token:  # Ensure the device has a valid token
            try:
                send_push_notification(device.token, title, body, data)
            except Exception as e:
                print(f"Failed to send notification to device {device.id} {device.token}: {e}")
def send_email():
    pass                