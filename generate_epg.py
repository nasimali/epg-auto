import requests
import xml.etree.ElementTree as ET

epg_channels = {
    "12114": "ATN Bangla UK",
    "12535": "TV One UK",
    "12423": "Islam Channel Bangla",
    "12071": "Deen TV",
    "12445": "Iqra Bangla",
    "12244": "NTV Europe UK",
    "60504": "ION TV",
    "9363": "Geo Entertainment",
    "9364": "Hum TV"
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

tree = ET.ElementTree(tv)
tree.write("merged_epg.xml", encoding="utf-8", xml_declaration=True)
print("✅ Merged EPG saved to merged_epg.xml")
