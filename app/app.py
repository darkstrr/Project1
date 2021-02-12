import requests
import os
import base64
import datetime
import random
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template
from bs4 import BeautifulSoup

genius_lyrics = ""
def spotify_authentication():
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

def genius_authentication():
    load_dotenv(find_dotenv())
    token = f"{os.getenv('genius_token')}";
    return token
    
def get_random_song():
    #artist test
    artist_id = ["0blbVefuxOGltDBa00dspv", "7BzEKSgHp2yrNC6w5NkFhQ", "7ucOhItVkxNqunNLo8AkzN"] #LiSA, Goosehouse, and FripSide
    Base_URL = f"https://api.spotify.com"
    version = f"v1"
    resource_type = "top-tracks?"
    market = "market=US"
    rand = random.randint(0, 2)
    #endpoint = f"{Base_URL}/{version}/artists/{artist_id[0]}/{resource_type}?offset=0&limit=10&include_groups=single&{market}"
    endpoint = f"{Base_URL}/{version}/artists/{artist_id[rand]}/{resource_type}{market}"
    
    #get authentication token
    authy = spotify_authentication()
    if not(authy):
        print("authentication failed")
    
    headers = {
        "Authorization": f"Bearer {authy}"
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
    
    #print(track_name)
    #print(artist_name)
    #print(track_preview)
    #print(track_image)
    
    #put song information into list
    song_info = [track_name, artist_name, track_preview, track_image]
    
    return song_info

def get_lyrics(song_path):
    base_url = "http://api.genius.com"
    genius_auth = "Bearer " + genius_authentication()
    headers = {'Authorization': genius_auth}
    song_url = base_url + song_path
    response = requests.get(song_url, headers=headers)
    response = response.json()
    path = response['response']['song']['path']
    
    #scrape lyrics from Genius website
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    global genius_lyrics
    genius_lyrics = page_url
    
    #get the HTML text of the song page
    html = BeautifulSoup(page.text, "html.parser")
    
    #remove javascript tags in the middle of the lyrics
    [h.extract() for h in html('script')]
    lyrics = html.find("div", class_="lyrics").get_text()
    return lyrics
    
    
def genius_song_info(song_title, artist_name):
    genius_auth = "Bearer " + genius_authentication()
    headers = {'Authorization': genius_auth}
    base_url = "http://api.genius.com"
    search_url = base_url + "/search"
    params = {'q': song_title}
    song_info = "Not Found"
    
    #get genius info for song
    response = requests.get(search_url, params=params, headers=headers)
    genius_info = response.json()
    song_info = None
    for hit in genius_info['response']['hits']:
        if hit['result']['primary_artist']['name'] == artist_name:
            song_info = hit
            print(song_info)
            break
    #return lyrics if it exists
    if song_info:
        song_path = song_info["result"]["api_path"]
        print(song_path)
        lyrics = get_lyrics(song_path)
        return(lyrics)
    return ""


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@app.route('/')
def main():
    global genius_lyrics
    song_info = get_random_song()
    print(song_info)
    
    #get song info from the genius api (url to lyrics)
    lyrics = genius_song_info(song_info[0], song_info[1])
    
    #check if no lyrics
    if not lyrics:
        lyrics = "no lyrics found\n check Genius link below"
        temp = song_info[0].replace(" ", "%20")
        genius_lyrics = "https://genius.com/search?q=" + temp
    
    return render_template(
        "index.html",
        songs = song_info,
        lyrics_info = lyrics,
        genius_url = genius_lyrics,
    )
    

app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)
