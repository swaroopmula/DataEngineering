import sys 
import requests
import json

artist_name = input("Enter an Artist Name: ")
n = int(input("No of songs: "))

response = requests.get(f"https://itunes.apple.com/search?entity=song&limit=2&term=" + artist_name)

deets = response.json()
#use "json.dumps(deets, indent = 2)" for clean representation of entire json file

print(json.dumps(deets, indent = 2))

# print()
# for item in deets.get("results"):
#     print(item.get("trackName"))
# print()
