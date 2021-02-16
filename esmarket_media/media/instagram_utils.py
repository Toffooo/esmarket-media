import requests

headers = {
    "accept": "*/*",
    "user-agent": "Instagram 8.1.0 (iPhone7,1; iPhone OS 9_3_2; en_US; scale=2.61; 1080x1920) AppleWebKit/420+"
}
resp = requests.get("https://i.instagram.com/api/v1/friendships/1673406630/followers/",
                    headers=headers)

print(resp.text)
