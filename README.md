# Spotify App

App to visually view statistics for music using Spotify's Web API.  
Currently a work in progress, so functionality is limited. In the future, users will be able to view statistics for their entire song library and create "filters" to organize their music into playlists.

## Tools / Frameworks Used
Currently, the following tools and frameworks are being used for development. These may be subject to change as the project progresses.
- Docker / Docker-Compose
- Flask (backend framework)
    - flask-login for remembering User sessions
- Google Cloud Firestore (database)
- Spotify API
- Basic HTML/CSS for front-end

## Setting up Project
1.  **Clone the repository**
```bash
$ git clone git@github.com:zainosaurus/spotify-app.git
```

2.  **Install Docker on local machine**  
    Installation instructions are located at https://docs.docker.com

4. **Set Up Environment Variables**
    Create a `.env` file with access keys to be used to access the Spotify API and Google Cloud Platform.  
    By default, the `docker-compose.yml` file expects this to be located in the `secrets/` subdirectory, named `secrets.env`.  
    Contents of `secrets.env`:
    ```bash
    # Spotify
    SPOTIFY_CLIENT_ID=(Spotify Client ID)
    SPOTIFY_CLIENT_SECRET=(Spotify Client Secret)

    # Google Cloud Firestore
    GOOGLE_APPLICATION_CREDENTIALS=(Absolute path to Google CLoud Firestore secret key json file)
    ```

3.  **Build project**
    Build the project using docker-compose from the root directory
    ```bash
    $ docker-compose build
    ```

## Running Locally
1.  Use docker-compose to run the project
    ```bash
    $ docker-compose up
    ```