from setuptools import setup, find_packages  #importing setup and find_packages from setuptools

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
] #list of required packages for the app 

setup(
	name='MyMusicLibrary.mp3',
  	version = '1.0',
    description= 'An app that imports you music library from both Spotify and downloads the YouTube version of it',
    author='Anjan Upreti',
    author_email='anjanuprety787@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data= True,
    install_requires= required
) #setting up the app with the required packages and the author details.