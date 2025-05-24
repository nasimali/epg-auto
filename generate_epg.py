import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pytz
import json

# Load channel mapping from JSON file
with open("channels.json", "r") as f:
    sky_channels = json.load(f)

# Constants
EPG_API_URL = "https://awk.epgsky.com/hawk/linear/schedule"
TIMEZONE = pytz.timezone("Europe/London")

# Date range: -1 to +3 days
dates = [
    (datetime.now(TIMEZONE) + timedelta(days=offset)).strftime('%Y%m%d')
    for offset in range(-1, 4)
]

# XMLTV root
tv = ET.Element("tv", attrib={"generator-info-name": "epg-custom"})

# Channel metadata
for name, info in sky_channels.items():
    ch_elem = ET.SubElement(tv, "channel", id=info["tvg-id"])
    ET.SubElement(ch_elem, "display-name").text = name

# Fetch and populate EPG data
for name, info in sky_channels.items():
    sid = info["sid"]
    tvg_id = info["tvg-id"]

    for date in dates:
        try:
            url = f"{EPG_API_URL}/{date}/{sid}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            events = data.get("schedule", [])[0].get("events", [])

            for ev in events:
                start = datetime.fromtimestamp(ev["st"], tz=TIMEZONE)
                end = start + timedelta(seconds=ev["d"])
                start_str = start.strftime('%Y%m%d%H%M%S %z')
                end_str = end.strftime('%Y%m%d%H%M%S %z')

                prog = ET.SubElement(tv, "programme", start=start_str, stop=end_str, channel=tvg_id)
                ET.SubElement(prog, "title").text = ev.get("t", "No Title")

                # Description + marketing message
                desc = ev.get("sy", "")
                if ev.get("marketingmessage"):
                    desc += f"\n\n{ev['marketingmessage']}"
                ET.SubElement(prog, "desc").text = desc.strip()

                # Subtitle and episode-num
                if ev.get("seasonnumber") and ev.get("episodenumber"):
                    subtitle = f"S{ev['seasonnumber']}E{ev['episodenumber']}"
                    ET.SubElement(prog, "sub-title").text = subtitle
                    ET.SubElement(prog, "episode-num", system="onscreen").text = subtitle

                # Rating
                if ev.get("r"):
                    rating = ET.SubElement(prog, "rating")
                    ET.SubElement(rating, "value").text = ev["r"]

                # New tag
                if ev.get("new"):
                    ET.SubElement(prog, "new")

        except Exception as e:
            print(f"Failed to fetch or parse EPG for {name} on {date}: {e}")

# Save XMLTV file
with open("merged_epg.xml", "wb") as f:
    ET.ElementTree(tv).write(f, encoding="utf-8", xml_declaration=True)