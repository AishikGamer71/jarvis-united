import sys
from pathlib import Path
import webbrowser

def website_navigator(parameters: dict, player=None):
    """
    Opens a website in the default browser.
    """
    url = parameters.get("url", "").strip()

    if not url:
        return "Error: Provide a 'url'."

    if not url.startswith("http"):
        url = "https://" + url

    if player:
        player.write_log(f"🌐 Navigating to website: {url}")

    try:
        webbrowser.open(url)
        return f"✅ Opened {url} in your default browser."
    except Exception as e:
        return f"Website navigation failed: {str(e)}"
