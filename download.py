# Importing BeautifulSoup for parsing HTML content
from bs4 import BeautifulSoup
# Importing HTMLSession from requests_html to handle HTTP requests and render JavaScript
from requests_html import HTMLSession
# Importing Path from pathlib to handle file paths
from pathlib import Path

# Importing yt_dlp, yt_dlp is a library that allows you to download videos from YouTube. It is a fork of youtube-dl with additional features and improvements.
import yt_dlp
# Importing requests for making HTTP requests
import requests
# Importing pandas for handling CSV files and data manipulation
import pandas
# Importing os for interacting with the operating system
import os

def DownloadVideosFromTitles(los): 
    # Initialize an empty list to store video IDs
    ids = []
    # Loop through the list of song titles
    for item in los:
        # Scrape the video ID for each song title
        vid_id = ScrapeVidId(item)
        # Append the video ID to the list if it's not None
        if vid_id:
            ids.append(vid_id) #append the video id to the list
        else:
            print(f"Skipping download for: {item}")
    if ids:
        print("Downloading songs")
        DownloadVideosFromIds(ids) 
    else:
        print("No valid video IDs found.")
    # Download videos using the list of video IDs
    DownloadVideosFromIds(ids)

def DownloadVideosFromIds(lov): #lov = list of video ids
    SAVE_PATH = str(os.path.join(Path.home(), "Downloads/songs")) #save path for the downloaded songs
    try:
        os.mkdir(SAVE_PATH)
    except FileExistsError:
        print("Download folder already exists")
    
    ydl_opts = {
        'format': 'bestaudio/best', 
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': SAVE_PATH + '/%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={vid_id}" for vid_id in lov])

def ScrapeVidId(query):
    print("Getting video id for:", query)

    # Use the YouTube Data API to fetch video ID based on the song title
    api_key = '...'  # Replace with your YouTube API key
    search_url = "https://www.googleapis.com/youtube/v3/search"
    
    params = {
        'part': 'snippet',
        'q': query,
        'key': api_key,
        'type': 'video',
        'maxResults': 1
    }
    
    response = requests.get(search_url, params=params)
    
    if response.status_code == 200: # status code 200 means the request was successful
        results = response.json().get('items')
        if results:
            return results[0]['id']['videoId']
        else:
            print(f"No video found for {query}")
            return None
    else:
        print(f"Error fetching data from YouTube API: {response.status_code}") 
        return None

def __main__():
    # Read the CSV file containing song names
    data = pandas.read_csv('songs.csv')
    # Convert the 'song names' column to a list
    data = data['song names'].tolist()
    print("Found ", len(data), " songs!")
    # Download videos for the list of songs
    DownloadVideosFromTitles(data)

# Check if the script is being run directly
if __name__ == "__main__":
    __main__()