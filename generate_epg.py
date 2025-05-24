import os
import requests
import xml.etree.ElementTree as ET

# Create the folder if it doesn't exist
output_dir = "epg_data"
os.makedirs(output_dir, exist_ok=True)

epg_channels = {
    "12114": "ATN Bangla UK",
    "12535": "TV One UK",
    "12423": "Islam Channel Bangla",
    "12071": "Deen TV",
    "12445": "Iqra Bangla",
    "12244": "NTV Europe UK",
    "60504": "ION TV",
    "12504": "CHSTV",
    "12507": "Geo Entertainment",
    "12446": "Hum TV"
}

tv = ET.Element("tv")

for channel_id, display_name in epg_channels.items():
    url = f"https://epg.pw/api/epg.xml?channel_id={channel_id}"
    try:
        print(f"Fetching EPG for {display_name}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        xml_tree = ET.fromstring(response.content)
        for elem in xml_tree:
            tv.append(elem)
    except Exception as e:
        print(f"❌ Failed for {display_name} ({channel_id}): {e}")

# Save XML to epg_data/merged_epg.xml
output_file = os.path.join(output_dir, "merged_epg.xml")
tree = ET.ElementTree(tv)
tree.write(output_file, encoding="utf-8", xml_declaration=True)

print(f"✅ Merged EPG saved to {output_file}")