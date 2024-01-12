import requests

def SaveAnalyticsInDatabase(data, period, userId):
    # Replace the URL with the URL of your deployed Firebase Cloud Function
    firebase_function_url = "https://us-central1-yandex-analytics-lobos.cloudfunctions.net/saveAnalytics"
    # Define your parameters
    params = {
        'data': data,
        'period': period,
        'userId': userId,
    }

    try:
        response = requests.get(firebase_function_url, params=params)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the content from the response
            content = response.text
            return content
        else:
            return response.status_code
    except Exception as e:
        return 500

def GetAnalyticsFromDatabase(userId):
    # Replace the URL with the URL of your deployed Firebase Cloud Function
    firebase_function_url = "https://us-central1-yandex-analytics-lobos.cloudfunctions.net/getAnalytics"
    # Define your parameters
    params = {
        'userId': userId,
    }

    try:
        response = requests.get(firebase_function_url, params=params)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the content from the response
            content = response.text
            return content,
        else:
            return response.status_code
    except Exception as e:
        return 500
