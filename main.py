import requests
import json
import os

# কনফিগারেশন
URL = "https://newapi-roan.vercel.app/main"
REFERER = "https://stumpedtv.pages.dev"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Referer": REFERER,
    "Origin": REFERER
}

def update_channels():
    try:
        print("Fetching data...")
        response = requests.get(URL, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            formatted_list = []

            for item in data:
                # Type ডিটেকশন
                video_url = item.get("url", "")
                vid_type = "mpd" if ".mpd" in video_url else "m3u8"

                # Keys ফরম্যাটিং (Optional)
                keys_data = None
                if item.get("k1") and item.get("k2"):
                    keys_data = {item["k1"]: item["k2"]}

                # নতুন অবজেক্ট তৈরি
                new_channel = {
                    "id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "type": vid_type,
                    "url": video_url,
                    "keys": keys_data,
                    "poster": "https://tv.assets.pressassociation.io/bea6d2cc-1051-5f6c-9464-0badeac80a07.jpg"
                }
                formatted_list.append(new_channel)

            # ==========================================
            # SPECIAL FORMATTING FOR NS PLAYER
            # ==========================================
            
            # প্রথমে সাধারণ JSON টেক্সট বানাই
            json_str = json.dumps(formatted_list, indent=2)

            # এবার 'keys' সেকশনটাকে ধরে এক লাইনে করে ফেলি
            # (এটা একটু হ্যাক, কিন্তু কাজ করবে ১০০%)
            lines = json_str.split('\n')
            final_lines = []
            skip = False
            
            for i, line in enumerate(lines):
                if '"keys": {' in line:
                    # keys শুরু হলে পরের লাইনগুলো চেক করে এক লাইনে জোড়া লাগাই
                    key_val_line = lines[i+1].strip().replace('"', '').replace(',', '') # key: value বের করা
                    # "key_id": "key_value" ফরম্যাট বানানো
                    key_parts = lines[i+1].strip().replace('"', '').replace(',', '').split(': ')
                    if len(key_parts) == 2:
                        k, v = key_parts
                        # এক লাইনে বসিয়ে দেওয়া
                        final_lines.append(f'    "keys": {{ "{k}": "{v}" }},')
                    else:
                        # যদি ফরম্যাট না মেলে, আগেরটাই রাখি
                        final_lines.append(line)
                        final_lines.append(lines[i+1])
                        final_lines.append(lines[i+2])
                    
                    skip = True # পরের ২ লাইন স্কিপ করব কারণ ওগুলো ভেঙে ছিল
                
                elif skip:
                    if '}' in line and not ':' in line: # ব্র্যাকেট বন্ধ হওয়া পর্যন্ত স্কিপ
                        skip = False
                    continue
                else:
                    final_lines.append(line)

            final_json = '\n'.join(final_lines)

            # ফাইলে সেভ করা
            with open("channels.json", "w") as f:
                f.write(final_json)
            
            print(f"Success! Fixed JSON saved.")
        else:
            print(f"Failed! Status Code: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_channels()
