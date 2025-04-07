import os
import time
import sqlite3
import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging to output to both console and log file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler("radio_tracker.log"),
        logging.StreamHandler()
    ]
)

# URL of the radio station's song history page
URL = 'https://player.listenlive.co/33421/en/songhistory'

# Configure options for headless mode
options = Options()
options.headless = True

# Specify the path to the Firefox binary
firefox_binary_path = 'C:/Program Files/Mozilla Firefox/firefox.exe'  # Update this path if needed
options.binary_location = firefox_binary_path

# Get the current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))
geckodriver_path = os.path.join(current_dir, 'geckodriver.exe')

# Log the geckodriver path
logging.info(f"Geckodriver path: {geckodriver_path}")

# Initialize the WebDriver (assuming geckodriver is in the same directory as this script)
service = Service(geckodriver_path)
driver = webdriver.Firefox(service=service, options=options)

# Initialize SQLite database
conn = sqlite3.connect('tracked_songs.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        song TEXT,
        artist TEXT,
        timestamp TEXT
    )
''')
conn.commit()

def get_now_playing():
    driver.get(URL)
    try:
        # Ensure the page is fully loaded
        time.sleep(5)
        driver.refresh()
        wait = WebDriverWait(driver, 10)
        song_artist_info = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'info')))
        
        song = song_artist_info.find_element(By.CLASS_NAME, 'title').text.strip()
        artist = song_artist_info.find_element(By.CLASS_NAME, 'artist').text.strip()
        logging.info(f"Retrieved song: {song}, artist: {artist}")
        return song, artist
    except Exception as e:
        logging.error(f"Error retrieving now playing song: {e}")
        return None, None

def track_songs(interval=60):
    last_song = None
    last_artist = None

    while True:
        try:
            song, artist = get_now_playing()
            if song and artist:
                if song != last_song or artist != last_artist:
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute('INSERT INTO songs (song, artist, timestamp) VALUES (?, ?, ?)', (song, artist, timestamp))
                    conn.commit()
                    logging.info(f"Logged song: {song}, artist: {artist} at {timestamp}")
                    last_song = song
                    last_artist = artist
                else:
                    logging.info(f"Song {song} by {artist} is still playing. No log entry created.")
            else:
                logging.warning("Could not retrieve song and artist information.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    try:
        track_songs()
    except KeyboardInterrupt:
        logging.info("Tracking stopped by user.")
    finally:
        driver.quit()
        conn.close()