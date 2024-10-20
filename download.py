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
        ids.append(vid_id)
    else:
            print(f"Skipping download for: {item}")
  if ids:
        print("Downloading songs")
        DownloadVideosFromIds(ids)
  else:
        print("No valid video IDs found.")
  # Download videos using the list of video IDs
  DownloadVideosFromIds(ids)

def DownloadVideosFromIds(lov):
    SAVE_PATH = str(os.path.join(Path.home(), "Downloads/songs"))
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
  
  # Use youtube_dl to download videos with the specified options
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download(lov)

def ScrapeVidId(query):
    print("Getting video id for:", query)
    BASIC = "https://www.youtube.com/results?search_query="
    URL = BASIC + query.replace(" ", "+")
    
    session = HTMLSession()
    response = session.get(URL)
    
    try:
        response.html.render(sleep=1)  # Render the page to load dynamic content
    except Exception as e:
        print(f"Error rendering page for {query}: {e}")
        return None
    
    soup = BeautifulSoup(response.html.html, "html.parser")
    
    # Find the first video result in the search
    results = soup.find('a', href=True, title=True)
    
    if results and '/watch?v=' in results['href']:
        # Extract the video ID from the href attribute
        try:
            video_id = results['href'].split('/watch?v=')[1].split('&')[0]
            return video_id
        except IndexError:
            print(f"Could not extract video ID from href: {results['href']}")
            return None
    else:
        print(f"No valid video link found for {query}")
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

