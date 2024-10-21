
# **MyMusicLibrary.mp3**  

## **Overview**  
**MyMusicLibrary.mp3** is a web-based Python application that integrates with the **Spotify API** to fetch a user’s saved tracks and downloads their corresponding YouTube versions as MP3 files. The project leverages **Flask** for web functionality, **Spotipy** for accessing the Spotify Web API, and **yt-dlp** to download media from YouTube. It provides a simple way to manage and archive your music offline.

---

## **Features**
- **Spotify Integration**: Authenticate users via Spotify and retrieve their saved tracks.
- **CSV Export**: Save the song library as a CSV file for easy access.
- **YouTube MP3 Downloads**: Download audio files of the tracks from YouTube.
- **Token Management**: Refreshes Spotify tokens automatically for seamless access.
- **Web-based Interface**: Powered by Flask for a lightweight, user-friendly interface.

---

## **Installation**

### **Prerequisites**  
Ensure you have **Python 3.6+** installed on your system. Install the necessary libraries by following the steps below.

### **Setup and Installation Steps**  
1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd MyMusicLibrary.mp3
   ```

2. **Install dependencies** using the setup script:
   ```bash
   python setup.py install
   ```

3. **Spotify API Credentials**:
   - Create a Spotify Developer account at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
   - Register a new application and get the **Client ID** and **Client Secret**.
   - Replace the placeholders in `create_spotify_oauth()` with your credentials.

4. **YouTube API Key** (Optional but recommended for accuracy):
   - Get a YouTube Data API key from the [Google Cloud Console](https://console.cloud.google.com/).
   - Replace `'...'` in the `ScrapeVidId()` function with your YouTube API key.

---

## **Usage Instructions**

1. **Run the Flask server**:
   ```bash
   python app.py
   ```

2. **Access the app**:  
   Open your browser and visit:  
   `http://127.0.0.1:5000/`

3. **Login with Spotify**:  
   - You will be redirected to Spotify’s login page.
   - Grant permission to access your saved tracks.

4. **Retrieve Your Library**:  
   - After logging in, your songs will be fetched and saved as `songs.csv`.

5. **Download YouTube Versions**:
   - Run the following command to download the MP3 versions:
     ```bash
     python app.py
     ```

---

## **Project Structure**  
```
MyMusicLibrary.mp3/
│
├── app.py              # Main Flask app and Spotify integration logic
├── setup.py            # Setup script to install dependencies
├── songs.csv           # CSV file containing saved songs (generated at runtime)
└── README.md           # Documentation (this file)
```

---

## **Code Snippet: Setup Script**  

```python
from setuptools import setup, find_packages

required = [
    'flask',
    'spotipy',
    'html5lib',
    'requests',
    'requests_html',
    'beautifulsoup4',
    'yt-dlp',
    'pathlib',
    'pandas'
]  

setup(
    name='MyMusicLibrary.mp3',
    version='1.0',
    description='An app that imports your Spotify library and downloads the YouTube version of it',
    author='Anjan Upreti',
    author_email='anjanuprety787@gmail.com',
    keywords='music, flask, spotify, youtube',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required
)
```

---

## **How It Works**

1. **Login and Authorization**:  
   The user logs in with Spotify through OAuth2, and the app fetches their saved tracks.  
   
2. **Song Retrieval and CSV Export**:  
   The application retrieves up to 50 tracks per batch, storing the song titles and artist names in `songs.csv`.  

3. **MP3 Download from YouTube**:  
   For each song in the CSV, the app uses YouTube’s Data API to find the best-matching video and downloads the audio as an MP3 file.  

---

## **Dependencies**

- **Flask**: Web framework for Python.  
- **Spotipy**: Python client for the Spotify Web API.  
- **yt-dlp**: Fork of youtube-dl for downloading YouTube media.  
- **BeautifulSoup4**: HTML parsing library.  
- **requests-html**: To handle HTTP requests and JavaScript rendering.  
- **Pandas**: For CSV and data handling.  

To install all dependencies manually:  
```bash
pip install -r requirements.txt
```

---
## **Code Overview**
A. app.py (Spotify Playlist Manager)
This is a Flask web application that allows users to log in with Spotify, retrieve their saved tracks, and store the playlist in a CSV file.

login(): Redirects users to Spotify for OAuth2 authentication.
authorize(): Handles the callback from Spotify and stores the access token in a session.
logout(): Clears the session data and logs the user out.
get_all_tracks(): Fetches the user’s saved tracks in batches of 50 and saves them to a CSV file.
get_token(): Verifies and refreshes expired tokens.
create_spotify_oauth(): Creates the Spotify OAuth object using the client credentials.
B. download.py (YouTube Video Downloader)
This script uses yt-dlp and web scraping to download songs as audio files based on the titles stored in the CSV file.

ScrapeVidId(query): Uses the YouTube API to fetch a video ID for a given song title.
DownloadVideosFromTitles(los): Takes a list of song titles, retrieves video IDs, and downloads the audio files.
DownloadVideosFromIds(lov): Downloads videos using yt-dlp based on the given video IDs.
__main__(): Reads the CSV file generated by the web app, extracts song names, and triggers the download process.
---

## **Usage**

Running the Web Application (app.py)
Start the Flask app by running:
```bash
python app.py
```
Visit http://localhost:5000 in your browser.
Log in using your Spotify account to grant the app access to your saved songs.
After login, the app will retrieve your saved tracks and store them in a CSV file named songs.csv.
Running the Download Script (download.py)
Ensure the songs.csv file is generated by the Flask app.
Run the downloader script:
```bash
python download.py
```
The script will read the song titles from the CSV, retrieve the corresponding video IDs from YouTube, and download the audio files in MP3 format.
---

## **Workflow**

User Authentication with Spotify:

The user logs in via the Spotify OAuth page.
The application retrieves the user’s saved tracks.
Generate CSV File:

The tracks are saved in a CSV file (songs.csv).
Download YouTube Videos:

The download script reads the song titles from the CSV.
It fetches the corresponding video IDs from YouTube and downloads them as audio files.
--- 

## **Achievements and Practical Applications**  
This project simplifies the **offline management of streaming music**, offering a practical way to **backup** or **archive Spotify playlists**. It automates the entire process from **song retrieval to download**, making it an ideal solution for users who want to access their playlists without an internet connection. Additionally, it showcases the practical integration of **multiple APIs**, handling **authentication tokens**, and **data manipulation** with ease.  

---

## **Author**  
**Anjan Upreti**  
anjanuprety787@gmail.com  

---

