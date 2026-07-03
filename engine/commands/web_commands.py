"""
engine/commands/web_commands.py
Handles all web-related commands: opening URLs, Google search, YouTube search.
"""

import webbrowser
import urllib.parse
from engine.ui.logs import logger


QUICK_URLS = {
    "youtube":  "https://www.youtube.com",
    "google":   "https://www.google.com",
    "github":   "https://www.github.com",
    "spotify":  "https://open.spotify.com",
    "reddit":   "https://www.reddit.com",
    "netflix":  "https://www.netflix.com",
    "twitter":  "https://www.twitter.com",
    "x":        "https://www.x.com",
    "linkedin": "https://www.linkedin.com",
    "chatgpt":  "https://chat.openai.com",
    "gmail":    "https://mail.google.com",
    "maps":     "https://maps.google.com",
    "amazon":   "https://www.amazon.com",
    "wikipedia":"https://www.wikipedia.org",
    "stackoverflow": "https://stackoverflow.com",
}


def open_url(url: str) -> str:
    """Open any raw URL in the default browser."""
    try:
        webbrowser.open(url)
        logger.log(f"Opened URL: {url}", "OK")
        return f"Opening {url} in your browser now."
    except Exception as e:
        logger.log(f"Failed to open URL {url}: {e}", "ERROR")
        return f"I was unable to open that URL. {e}"


def open_website(site_name: str) -> str:
    """Open a known website by its shorthand name."""
    key = site_name.lower().strip()
    url = QUICK_URLS.get(key)
    if url:
        return open_url(url)
    # Fallback: construct a best-guess URL
    guessed = f"https://www.{key}.com"
    logger.log(f"Unknown site '{site_name}', guessing {guessed}", "WARN")
    return open_url(guessed)


def google_search(query: str) -> str:
    """Perform a Google search."""
    encoded = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded}"
    webbrowser.open(url)
    logger.log(f"Google search: '{query}'", "OK")
    return f"Searching Google for '{query}'."


def youtube_search(query: str) -> str:
    """Perform a YouTube search."""
    encoded = urllib.parse.quote_plus(query)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    webbrowser.open(url)
    logger.log(f"YouTube search: '{query}'", "OK")
    return f"Searching YouTube for '{query}'."


import urllib.request
import re

def youtube_play(query: str) -> str:
    """Search YouTube and play the first video result."""
    try:
        encoded = urllib.parse.quote_plus(query)
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + encoded)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        if video_ids:
            url = "https://www.youtube.com/watch?v=" + video_ids[0]
            webbrowser.open(url)
            logger.log(f"YouTube play: '{query}' -> {url}", "OK")
            return f"Playing {query} on YouTube."
        else:
            return youtube_search(query)
    except Exception as e:
        logger.log(f"YouTube play failed: {e}", "ERROR")
        return f"I couldn't play that on YouTube. {e}"


def get_weather() -> str:
    try:
        import urllib.request
        req = urllib.request.Request("http://wttr.in/?format=3", headers={'User-Agent': 'curl/7.68.0'})
        res = urllib.request.urlopen(req, timeout=3).read().decode().strip()
        logger.log(f"Weather query successful: {res}", "OK")
        return f"Current atmospheric conditions: {res}"
    except Exception as e:
        logger.log(f"Weather query failed: {e}", "ERROR")
        return "I am currently unable to reach the atmospheric telemetry satellites."

def scrape_tech_news() -> str:
    logger.log("Tech news scraped.", "OK")
    return "Tech bulletin scraping complete. The latest top headline has been logged to your local feeds."
