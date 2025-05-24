# 📺 EPG Auto-Generator (Every 72 Hours)

This repository automatically fetches and merges EPG (Electronic Program Guide) data for a set of IPTV channels using [epg.pw](https://epg.pw), then pushes the result as a single `merged_epg.xml` file.

### ✅ Included Channels

- ATN Bangla UK
- TV One UK
- Islam Channel Bangla
- Deen TV
- Iqra Bangla
- NTV Europe UK
- ION TV
- Geo Entertainment
- Hum TV

> Channel S UK is currently excluded due to lack of reliable XMLTV source.

---

## 🔁 Automation via GitHub Actions

A GitHub Actions workflow (`.github/workflows/epg-update.yml`) runs:

- ⏱️ **Every 72 hours**
- 🧰 Fetches latest EPGs from `epg.pw`
- 🗂️ Merges them into a single XMLTV file
- 🚀 Pushes `merged_epg.xml` back to this repo

---

## 🛠 How to Use

1. Clone or fork this repo
2. Push to your own GitHub account
3. The action will run automatically (or you can trigger it manually)
4. Grab the raw link to `merged_epg.xml`, for example:
