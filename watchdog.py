import requests
import time
import os

USERNAME = "prag1337bot"
TARGET = 1337

def get_solved_count():
    url = "https://leetcode.com/graphql"
    payload = {
        "query": """
        query getUserProfile($username: String!) {
          matchedUser(username: $username) {
            submitStats {
              acSubmissionNum {
                difficulty
                count
              }
            }
          }
        }
        """,
        "variables": {"username": USERNAME}
    }
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        stats = data.get("data", {}).get("matchedUser", {}).get("submitStats", {}).get("acSubmissionNum", [])
        for item in stats:
            if item.get("difficulty") == "All":
                return item.get("count")
    return None

print(f"Starting watchdog for {USERNAME}...")

while True:
    try:
        current_solved = get_solved_count()
        
        if current_solved is not None:
            print(f"Watchdog tracking: {current_solved} / {TARGET} solved.")
            
            if current_solved >= TARGET:
                print(f"\Target {TARGET} hit.")
                os.system("pkill -f submitter.py")
                print("Exiting.")
                break
        else:
            print("Could not fetch profile. Make sure your username is correct.")
            
    except Exception as e:
        pass
        
    time.sleep(10)
