# 📺 EPG Auto-Generator (Every 24 Hours)

This repository automatically fetches and merges EPG (Electronic Program Guide) data for a set of IPTV channels, then pushes the result as a single `merged_epg.xml` file.

### ✅ Included Channels

- ATN Bangla UK
- TV One UK
- Islam Channel Bangla
- Deen TV
- Iqra Bangla
- NTV Europe UK
- ION TV
- CH S UK
- Geo Entertainment
- Hum TV

---

## 🔁 Automation via GitHub Actions

A GitHub Actions workflow (`.github/workflows/epg-update.yml`) runs:

- ⏱️ **Every 24 hours**
- 🧰 Fetches latest EPGs from web
- 🗂️ Merges them into a single XMLTV file
- 🚀 Pushes `merged_epg.xml` back to this repo

---

## 🛠 How to Use

1. Clone or fork this repo
2. Push to your own GitHub account
3. The action will run automatically (or you can trigger it manually)
4. Grab the raw link to `merged_epg.xml`, for example:
   [Click here to view or use the raw XMLTV file](https://raw.githubusercontent.com/nasimali/epg-auto/release/main-epg/epg_data/merged_epg.xml)
