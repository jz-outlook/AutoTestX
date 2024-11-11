import requests




def api_automation_test():
    url = "https://api-test-ws.myaitalk.vip/lesson/lastAsset.php"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
