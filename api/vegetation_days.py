import requests
import api.token_fetcher as fetch_token

token = fetch_token.fetch_token()

def fetch_vegetation_days():
    api_url = "https://api.meteomatics.com/2024-10-06T00:00:00ZP35D:P1D/vegetation_days:d/47.412164,9.340652/html?access_token=" + token
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"