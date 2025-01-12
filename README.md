# Spotify AI Playlist Categorizer

Playing around with Spotify API and AI to create categories and playlists based on my Liked songs


## Problem

I'm super lazy when it comes to my Spotify songs. I simply press "Like" on songs that I enjoy and have basically one giant list of songs - this makes it diffiult when I want to listen to certain songs (for gym, upbeat, etc.) - I'm too lazy on the go to categorize things into playlists.
## Goal

This project aims to utilize Liked Songs in my Spotify and then leverage AI to automatically create categories and then playlists from those categories.

## Initial Steps

I threw this all into ChatGPT to see if it could help me get started - here's the output

```
You can use the Spotify Web API to access and manage your Liked Songs and playlists. However, the Spotify API itself does not include advanced AI capabilities for categorizing songs based on their features or content.

To automatically categorize your Liked Songs into playlists, you would typically need to:

Access your Liked Songs: Use the Spotify API to retrieve your saved tracks.
Analyze Song Features: Use Spotify's audio features endpoint to get details like danceability, energy, tempo, etc.
Categorize Songs: Apply some logic or use an external AI/ML service to categorize songs based on their features.
Create Playlists: Use the Spotify API to create and populate playlists with the categorized songs.
For the categorization step, you might consider using an external AI service or a machine learning model. Some potential options include:

Pre-trained Models/APIs: Services like Google Cloud AI, IBM Watson, or Azure Cognitive Services offer pre-built models that can analyze and categorize text and audio data.
Custom ML Models: You could train a custom machine learning model using a platform like TensorFlow or PyTorch to categorize songs based on their audio features.
Here is a high-level outline of how you might implement this:

Set Up Spotify API: Authenticate and get access tokens.
Retrieve Liked Songs: Use the GET /me/tracks endpoint.
Analyze Features: Use the GET /audio-features endpoint for each track.
Categorize Songs: Use an AI service or custom model to categorize the songs.
Create and Populate Playlists:
Use the POST /users/{user_id}/playlists endpoint to create playlists.
Use the POST /playlists/{playlist_id}/tracks endpoint to add tracks to the playlists.
Combining these steps would allow you to automate the categorization and organization of your Liked Songs into playlists.
```

## Usage

Clone the `.env.sample` file into a `.env` file in order for the scripts to pull from your API keys

## Environment Setup

This project requires Spotify API credentials to function. Follow these steps to set up your environment:

1. Clone the `.env.sample` file for both development and testing:
   ```bash
   # For development
   cp .env.sample .env

   # For testing
   cp .env.sample .env.test
   ```

2. Update both files with your Spotify API credentials:
   - Get your credentials from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - For development (`.env`): Use your production application credentials
   - For testing (`.env.test`): Use separate test application credentials

3. Set the required environment variables:

   **For Local Development & Testing** (in `.env` and `.env.test`):
   ```
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
   ```

   **For GitHub Actions**:
   ```
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
   ```
   Note: While the `SPOTIFY_REDIRECT_URI` isn't used in CI tests (which use a different authentication method), 
   you can still include it in your GitHub Secrets to maintain consistency with the local environment.

Note: Both `.env` and `.env.test` files are git-ignored for security. Never commit these files or share your credentials.