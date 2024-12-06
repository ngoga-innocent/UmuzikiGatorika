import requests

def send_push_notification(expo_push_token, title, body, data=None):
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
        "data": data or {"someData": "goes here"}
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()  # Returns the response from Expo
    else:
        # Log or handle the error as needed
        print(f"Failed to send push notification: {response.status_code} - {response.text}")
        response.raise_for_status()
