import os
import re
import json
import requests
from datetime import datetime

# Load config
CONFIG_PATH = 'config.json'
if not os.path.exists(CONFIG_PATH):
    print("Error: config.json not found.")
    exit(1)

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

# API Keys
STEAM_API_KEY = config['steam']['api_key']
STEAM_ID = config['steam']['steam_id']
HARDCOVER_TOKEN = config.get('hardcover', {}).get('token')

def fetch_steam_data():
    """Fetch recently played games from Steam."""
    if STEAM_ID == "YOUR_STEAM_ID_HERE" or not STEAM_ID:
        return None
    
    url = f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={STEAM_API_KEY}&steamid={STEAM_ID}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('response', {}).get('games', [])
    return None

def fetch_hardcover_data():
    """Fetch books from Hardcover using GraphQL."""
    if not HARDCOVER_TOKEN:
        return None
    
    url = "https://api.hardcover.app/v1/graphql"
    headers = {
        "Authorization": HARDCOVER_TOKEN,
        "Content-Type": "application/json"
    }
    
    # Query for currently reading (status_id 2) and read (status_id 3)
    query = {
        "query": """
        query GetUserBooks {
          me {
            user_books(where: {status_id: {_in: [2, 3]}}, order_by: {last_read_date: desc}) {
              status_id
              last_read_date
              book {
                title
                image {
                  url
                }
                contributions {
                  author {
                    name
                  }
                }
              }
            }
          }
        }
        """
    }
    
    response = requests.post(url, headers=headers, json=query)
    if response.status_code == 200:
        data = response.json().get('data', {}).get('me', [])
        if data:
            return data[0].get('user_books', [])
    return None

def update_html(file_path, markers):
    """Update HTML file by injecting content between markers."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for marker, replacement in markers.items():
        start_marker = f"<!-- {marker}_START -->"
        end_marker = f"<!-- {marker}_END -->"
        
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        if pattern.search(content):
            content = pattern.sub(f"{start_marker}\n{replacement}\n{end_marker}", content)
        else:
            print(f"Warning: Marker {marker} not found in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_game_grid(games):
    html = ""
    for game in games[:6]:
        img_url = f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{game['appid']}/header.jpg"
        html += f"""
                        <div class="grid-card-tech bg-surface-inset border border-white/5 p-4 group">
                            <div class="aspect-square relative mb-4 overflow-hidden grayscale group-hover:grayscale-0 transition-all duration-500">
                                <img src="{img_url}" class="w-full h-full object-cover opacity-40 group-hover:opacity-100">
                                <div class="absolute top-2 right-2 px-1 py-0.5 bg-primary-neon/20 border border-primary-neon/30 text-primary-neon text-[6px] font-black uppercase">RECENTLY_PLAYED</div>
                            </div>
                            <h4 class="text-[9px] font-black tracking-widest uppercase mb-1">{game['name'].upper()}</h4>
                            <div class="flex justify-between items-center text-[7px] text-on-surface-variant font-bold opacity-50">
                                <span>APP_ID: {game['appid']}</span>
                                <span class="text-secondary-cyan">{game['playtime_forever'] // 60}H</span>
                            </div>
                        </div>"""
    return html

def generate_game_feature(game):
    if not game: return ""
    img_url = f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{game['appid']}/header.jpg"
    return f"""
                    <div class="feature-card grid grid-cols-1 lg:grid-cols-2 gap-0 min-h-[400px]">
                        <div class="feature-image-container relative h-[300px] lg:h-auto overflow-hidden">
                            <img src="{img_url}" alt="{game['name']}" class="w-full h-full object-cover grayscale-[0.5] contrast-[1.2]">
                        </div>
                        <div class="p-8 lg:p-12 flex flex-col justify-center bg-surface/40 backdrop-blur-xl relative z-10">
                            <div class="mb-6">
                                <span class="bg-primary-neon/20 text-primary-neon text-[8px] font-black px-2 py-0.5 border border-primary-neon/30 tracking-[0.2em] uppercase mb-4 inline-block">SESSION_ACTIVE</span>
                                <h3 class="text-6xl font-black tracking-tighter uppercase mb-2">{game['name'].upper()}</h3>
                                <p class="text-on-surface-variant text-[10px] font-bold tracking-widest uppercase opacity-60">Sub-System: Steam_Integration // App_ID: {game['appid']}</p>
                            </div>

                            <div class="grid grid-cols-2 gap-8 mb-10">
                                <div>
                                    <span class="text-[8px] font-black tracking-widest text-on-surface-variant uppercase opacity-50 block mb-1">TOTAL_PLAYTIME</span>
                                    <span class="text-2xl font-bold font-mono tracking-tight">{game['playtime_forever'] // 60} HRS</span>
                                </div>
                                <div>
                                    <span class="text-2xl font-bold font-mono tracking-tight text-primary-neon">ACTIVE</span>
                                </div>
                            </div>
                        </div>
                    </div>"""

def generate_book_grid(user_books):
    html = ""
    # Only show read (status_id 3) in the grid, or all recent ones
    for entry in user_books[:6]:
        book = entry['book']
        img_url = book.get('image', {}).get('url', 'https://images.unsplash.com/photo-1543004218-ee14110497f9?q=80&w=400&auto=format&fit=crop')
        author = book.get('contributions', [{}])[0].get('author', {}).get('name', 'UNKNOWN')
        status = "ARCHIVED" if entry['status_id'] == 3 else "READING"
        
        html += f"""
                        <div class="grid-card-tech bg-surface-inset border border-white/5 p-4 group">
                            <div class="aspect-square relative mb-4 overflow-hidden grayscale group-hover:grayscale-0 transition-all duration-500">
                                <img src="{img_url}" class="w-full h-full object-cover opacity-40 group-hover:opacity-100">
                                <div class="absolute top-2 right-2 px-1 py-0.5 bg-primary-neon/20 border border-primary-neon/30 text-primary-neon text-[6px] font-black uppercase">{status}</div>
                            </div>
                            <h4 class="text-[9px] font-black tracking-widest uppercase mb-1">{book['title'].upper()}</h4>
                            <div class="flex justify-between items-center text-[7px] text-on-surface-variant font-bold opacity-50">
                                <span>TAG: LOGGED</span>
                                <span class="text-secondary-cyan">{author.upper()}</span>
                            </div>
                        </div>"""
    return html

def generate_book_feature(entry):
    if not entry: return ""
    book = entry['book']
    img_url = book.get('image', {}).get('url', 'https://images.unsplash.com/photo-1543004218-ee14110497f9?q=80&w=400&auto=format&fit=crop')
    author = book.get('contributions', [{}])[0].get('author', {}).get('name', 'UNKNOWN')
    
    return f"""
                    <div class="feature-card grid grid-cols-1 lg:grid-cols-2 gap-0 min-h-[400px]">
                        <div class="feature-image-container relative h-[300px] lg:h-auto overflow-hidden">
                            <img src="{img_url}" alt="{book['title']}" class="w-full h-full object-cover grayscale-[0.5] contrast-[1.2]">
                        </div>
                        <div class="p-8 lg:p-12 flex flex-col justify-center bg-surface/40 backdrop-blur-xl relative z-10">
                            <div class="mb-6">
                                <span class="bg-primary-neon/20 text-primary-neon text-[8px] font-black px-2 py-0.5 border border-primary-neon/30 tracking-[0.2em] uppercase mb-4 inline-block">KNOWLEDGE_STREAM_ACTIVE</span>
                                <h3 class="text-6xl font-black tracking-tighter uppercase mb-2">{book['title'].upper()}</h3>
                                <p class="text-on-surface-variant text-[10px] font-bold tracking-widest uppercase opacity-60">Source: Hardcover_Archive // Author: {author.upper()}</p>
                            </div>

                            <div class="grid grid-cols-2 gap-8 mb-10">
                                <div>
                                    <span class="text-[8px] font-black tracking-widest text-on-surface-variant uppercase opacity-50 block mb-1">COMPLETION_STATUS</span>
                                    <span class="text-2xl font-bold font-mono tracking-tight">ANALYZING</span>
                                </div>
                                <div>
                                    <span class="text-2xl font-bold font-mono tracking-tight text-primary-neon">IN_PROCESS</span>
                                </div>
                            </div>
                        </div>
                    </div>"""

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] --- SYSTEM_SYNC_INITIALIZED ---")
    
    # 1. Update Games (play.html)
    games = fetch_steam_data()
    if games:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] FETCHED: {len(games)} Steam Games.")
        game_grid_html = generate_game_grid(games)
        game_feature_html = generate_game_feature(games[0]) if games else ""
        update_html('play.html', {
            'AUTO_GRID': game_grid_html,
            'AUTO_FEATURE': game_feature_html
        })
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] WARNING: No Steam data found. Check SteamID.")

    # 2. Update Books (read.html)
    user_books = fetch_hardcover_data()
    if user_books:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] FETCHED: {len(user_books)} Hardcover Books.")
        book_grid_html = generate_book_grid(user_books)
        # Find currently reading for feature, or just the most recent
        currently_reading = next((b for b in user_books if b['status_id'] == 2), user_books[0])
        book_feature_html = generate_book_feature(currently_reading)
        update_html('books.html', {
            'AUTO_GRID': book_grid_html,
            'AUTO_FEATURE': book_feature_html
        })
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] WARNING: No Hardcover data found. Check Token.")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] --- SYNC_SEQUENCE_COMPLETE ---")

if __name__ == "__main__":
    main()
