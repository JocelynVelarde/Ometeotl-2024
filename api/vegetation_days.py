import requests

def fetch_vegetation_days():
    api_url = "https://api.meteomatics.com/2024-10-06T00:00:00ZP35D:P1D/vegetation_days:d/47.412164,9.340652/html?access_token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2IjoxLCJ1c2VyIjoidmVsYXJkZV9qb2NlbHluIiwiaXNzIjoibG9naW4ubWV0ZW9tYXRpY3MuY29tIiwiZXhwIjoxNzI4MTg5MTg5LCJzdWIiOiJhY2Nlc3MifQ.kFhUp2HiUGXAiJda_NVL49IgA-EmBPxiH0AYxOeazzCQNt8cJWDU2ZSPl7HxmlJM6Cr9CGCOkUvokAOe3ZCg_Q"
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"