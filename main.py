import requests
import json
import os

# কনফিগারেশন
URL = "https://newapi-roan.vercel.app/main"
REFERER = "https://stumpedtv.pages.dev"

# হেডার সেটআপ (যাতে সার্ভার ব্লক না করে)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Referer": REFERER,
    "Origin": REFERER
}

def update_channels():
    try:
        print("Fetching data from API...")
        response = requests.get(URL, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            formatted_list = []

            # ডাটা লুপ করে সাজানো হচ্ছে
            for item in data:
                # Type ডিটেকশন (MPD না M3U8)
                video_url = item.get("url", "")
                vid_type = "mpd" if ".mpd" in video_url else "m3u8"

                # Keys ফরম্যাটিং
                keys = None
                if item.get("k1") and item.get("k2"):
                    keys = {item["k1"]: item["k2"]}

                # নতুন অবজেক্ট তৈরি
                new_channel = {
                    "id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "type": vid_type,
                    "url": video_url,
                    "keys": keys,
                    "poster": "https://tv.assets.pressassociation.io/bea6d2cc-1051-5f6c-9464-0badeac80a07.jpg"
                }
                formatted_list.append(new_channel)

            # channels.json ফাইলে সেভ করা
            with open("channels.json", "w") as f:
                json.dump(formatted_list, f, indent=2)
            
            print(f"Success! Total channels found: {len(formatted_list)}")
        else:
            print(f"Failed! Status Code: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_channels()
