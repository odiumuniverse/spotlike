# Spotify Playlist Liker 🎵

A script to automatically add all songs from a Spotify playlist to your library (Liked Songs).

## Why???

- Because I don’t see the point of playlists — I keep everything in Liked Songs, but when I transfer tracks from other apps, they all end up as separate playlists  
- I just want to

## Features

- Automatic Spotify OAuth authorization  
- Fetches all tracks from a playlist (including large ones)  
- Skips tracks that are already liked  
- Adds tracks to your library in batches  
- Detailed progress output

## Requirements

- Python 3.6+  
- Spotify Developer Account  
- Client ID and Client Secret from your Spotify App

## Installation

1. Clone the repository or download the files

## Setting up your Spotify App

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)  
2. Click **"Create app"**  
3. Fill in:
   - **App name**: anything (e.g., "Playlist Liker")  
   - **App description**: anything  
   - **Redirect URI**: `http://example.com/callback`
4. Save the app  
5. Copy the **Client ID** and **Client Secret**

## Script Setup

> On first run, the script will prompt you to enter your credentials.

## Usage

#### Run the script

```bash
python3 -m venv venv
source venv/bin/activate
python spotify_like_playlist.py
```

#### First Run Instructions

1. A browser will open to authorize the app via Spotify  
2. Grant access to the app  
3. You'll be redirected to `example.com` — copy the **full URL** from the address bar and paste it into the terminal when prompted  
4. Enter the playlist URL or ID:
   - **Full URL**: `https://open.spotify.com/playlist/37hfuiahfibqiwbgfiuer`
   - **Just the ID**: `37hfuiahfibqiwbgfiuer`  
5. The script will show playlist info and the number of new tracks  
6. Confirm to add the tracks to your library  


#### Notes

- The Spotify API allows adding up to **50 tracks per request**
- The script **automatically splits** large playlists into chunks
- **Already liked tracks** are skipped
- For **private playlists**, you must be the owner or have access


#### Possible Issues

- **"Redirect URI mismatch"** — Make sure the Spotify App has `http://example.com/callback` set as a redirect URI  
- **"Invalid client"** — Check that your Client ID and Client Secret are correct  
- **"Insufficient client scope"** — Delete the `.cache` file and re-authenticate  


**P.S.** If something goes wrong — I’m not responsible for it. The license says so, and the whole thing was written by an AI.
