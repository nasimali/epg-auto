import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pytz
import json

os.makedirs("epg_data", exist_ok=True)

with open("channels.json", "r") as f:
    sky_channels = json.load(f)

EPG_API_URL = "https://awk.epgsky.com/hawk/linear/schedule"
TIMEZONE = pytz.timezone("Europe/London")

dates = [
    (datetime.now(TIMEZONE) + timedelta(days=offset)).strftime('%Y%m%d')
    for offset in range(-1, 4)
]

tv = ET.Element("tv", attrib={"generator-info-name": "epg-custom"})

for name, info in sky_channels.items():
    ch_elem = ET.SubElement(tv, "channel", id=info["tvg-id"])
    ET.SubElement(ch_elem, "display-name").text = name

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
                start = datetime.fromtimestamp(ev["st"] + (3600 if TIMEZONE.localize(datetime.fromtimestamp(ev["st"])).dst().total_seconds() != 0 else 0), tz=TIMEZONE)
                end = start + timedelta(seconds=ev["d"])
                start_str = start.strftime('%Y%m%d%H%M%S %z')
                end_str = end.strftime('%Y%m%d%H%M%S %z')

                prog = ET.SubElement(tv, "programme", start=start_str, stop=end_str, channel=tvg_id)
                ET.SubElement(prog, "title").text = ev.get("t", "No Title")

                desc = ev.get("sy", "")
                if ev.get("marketingmessage"):
                    desc += f"\n\n{ev['marketingmessage']}"
                ET.SubElement(prog, "desc").text = desc.strip()

                if ev.get("seasonnumber") and ev.get("episodenumber"):
                    subtitle = f"S{ev['seasonnumber']}E{ev['episodenumber']}"
                    ET.SubElement(prog, "sub-title").text = subtitle
                    ET.SubElement(prog, "episode-num", system="onscreen").text = subtitle

                if ev.get("r"):
                    rating = ET.SubElement(prog, "rating")
                    ET.SubElement(rating, "value").text = ev["r"]

                if ev.get("new"):
                    ET.SubElement(prog, "new")

        except Exception as e:
            print(f"Failed to fetch or parse EPG for {name} on {date}: {e}")

with open("epg_data/merged_epg.xml", "wb") as f:
    ET.ElementTree(tv).write(f, encoding="utf-8", xml_declaration=True)