import requests
import os
import base64
import datetime
from dotenv import load_dotenv, find_dotenv

#do a lookup for a token
load_dotenv(find_dotenv())
client_creds = f"{os.getenv('client_id')}:{os.getenv('client_secret')}"
client_creds_b64 = base64.b64encode(client_creds.encode())
token_url = "https://accounts.spotify.com/api/token"
method = "POST"
token_data = {
    "grant_type": "client_credentials"
    
}
token_headers = {
    "Authorization": f"Basic {client_creds_b64.decode()}"
}
# request for authentication
r = requests.post(token_url, data = token_data, headers=token_headers)
print(r.json())

#check for valid request
valid_request = r.status_code in range(200, 299)
#if request is valid, make a expiration checker
if valid_request:
    token_response_data = r.json()
    now = datetime.datetime.now()
    access_token = token_response_data['access_token']
    expires_in = token_response_data['expires_in']
    expires = now + datetime.timedelta(seconds=expires_in)
    did_expire = expires < now
    print(expires)
    
#artist test
artist_id = ["0blbVefuxOGltDBa00dspv"] #LiSA
Base_URL = f"https://api.spotify.com"
version = f"v1"
resource_type = "albums"
market = "market=ES"
#endpoint = f"{Base_URL}/{version}/artists/{artist_id[0]}/{resource_type}?offset=0&limit=10&include_groups=single&{market}"
#endpoint = f"https://api.spotify.com/v1/artists/0blbVefuxOGltDBa00dspv/top-tracks?market=ES"
endpoint = f"https://api.spotify.com/v1/browse/new-releases?country=ES&offset=0&limit=10"
headers = {
    "Authorization": f"Bearer {access_token}"
}

#send request for LISA albums
#request_album = requests.get(endpoint, headers=headers)
#lisa_albums = request_album.json()
new_releases = requests.get(endpoint, headers=headers)
new_releases = new_releases.json()
#print(lisa_albums)

#print 10 tracks
for i in range(0,10):
    print(new_releases["albums"].get("items")[i]["name"])
