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


def youtube_play(query: str) -> str:
    """Convenience wrapper — same as youtube_search but with speech variation."""
    return youtube_search(query)
