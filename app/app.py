import requests
import os
import base64
import datetime
import random
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template


def authentication():
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
    #print(r.json())
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
        return access_token
    else:
        return ""

def get_random_song():
    #artist test
    artist_id = ["0blbVefuxOGltDBa00dspv", "7BzEKSgHp2yrNC6w5NkFhQ", "7ucOhItVkxNqunNLo8AkzN"] #LiSA, Goosehouse, and FripSide
    Base_URL = f"https://api.spotify.com"
    version = f"v1"
    resource_type = "top-tracks?"
    market = "market=ES"
    rand = random.randint(0, 2)
    #endpoint = f"{Base_URL}/{version}/artists/{artist_id[0]}/{resource_type}?offset=0&limit=10&include_groups=single&{market}"
    endpoint = f"{Base_URL}/{version}/artists/{artist_id[rand]}/{resource_type}{market}"
    headers = {
        "Authorization": f"Bearer {authentication()}"
    }
    
    #send request for top tracks
    request_tracks = requests.get(endpoint, headers=headers)
    tracks = request_tracks.json()
    #print(tracks)
    
    #get track previews and names
    rand2 = random.randint(0, 9)
    track_name = (tracks["tracks"][rand2]["name"])
    track_preview = tracks["tracks"][rand2]["preview_url"]
    artist_name = tracks["tracks"][rand2]["artists"][0].get("name")
    track_image = tracks['tracks'][rand2].get("album").get("images")[0].get("url")
    
    print(track_name)
    print(artist_name)
    print(track_preview)
    print(track_image)
    
    #put song information into list
    song_info = [track_name, artist_name, track_preview, track_image]
    
    return song_info


app = Flask(__name__)
@app.route('/')
def main():
    song_info = get_random_song()
    print(song_info)
    """
    return render_template(
        "index.html",
        songs = song_info
    )
    """

main()