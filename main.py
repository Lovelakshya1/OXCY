import flet as ft
import os

# --- APP CONFIG ---
API_KEY = "AIzaSyBXc97B045znooQD-NDPBjp8SluKbDSbmc"

def main(page: ft.Page):
    page.title = "OXCY"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    page.padding = 10
    
    # --- UI ELEMENTS ---
    status_text = ft.Text("System Ready. Waiting for command...", color="green", size=12)
    results_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    # Debug Console on screen (To see errors without crashing)
    debug_box = ft.Text("", color="red", size=10, selectable=True)

    def log(msg):
        print(msg)
        debug_box.value = f"{str(msg)}\n{debug_box.value}"
        page.update()

    # --- SAFE FUNCTIONS (Imports happen HERE, not at startup) ---
    def run_search(e):
        if not search_bar.value: return
        status_text.value = "Initializing Network..."
        page.update()
        
        try:
            # LAZY IMPORT: Only loads when you click button
            import requests 
            log("Network Module Loaded.")
            
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "part": "snippet",
                "q": f"{search_bar.value} music",
                "type": "video",
                "key": API_KEY,
                "maxResults": 15
            }
            res = requests.get(url, params=params, timeout=5)
            data = res.json()
            
            tracks = [{'id': i['id']['videoId'], 'title': i['snippet']['title'], 'channel': i['snippet']['channelTitle']} for i in data.get('items', [])]
            
            results_list.controls.clear()
            if not tracks:
                status_text.value = "No results found."
            else:
                status_text.value = f"Found {len(tracks)} results"
                for t in tracks:
                    results_list.controls.append(create_track_tile(t))
            log("Search Complete.")
            
        except Exception as err:
            log(f"SEARCH ERROR: {err}")
            status_text.value = "Search Failed (See Debug Log)"
        page.update()

    def play_track(video_id):
        status_text.value = "Loading Audio Engine..."
        page.update()
        try:
            # LAZY IMPORT: Only loads when you click play
            import yt_dlp
            log("yt-dlp Module Loaded.")
            
            ydl_opts = {'format': 'bestaudio[ext=m4a]', 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_id, download=False)
                url = info['url']
                
            page.overlay.append(ft.Audio(src=url, autoplay=True))
            status_text.value = f"Streaming: {video_id}"
            log(f"Playing URL: {url[:30]}...")
            
        except Exception as err:
            log(f"PLAYBACK ERROR: {err}")
            status_text.value = "Playback Failed (See Debug Log)"
        page.update()

    def create_track_tile(t):
        return ft.Container(
            content=ft.ListTile(
                leading=ft.Icon(ft.Icons.MUSIC_NOTE, color="yellow"),
                title=ft.Text(t['title'], weight="bold", max_lines=1),
                subtitle=ft.Text(t['channel']),
                trailing=ft.IconButton(ft.Icons.PLAY_ARROW, icon_color="white"),
                on_click=lambda _, vid=t['id']: play_track(vid)
            ),
            bgcolor="#1A1A1A", border_radius=8, margin=ft.margin.only(bottom=5)
        )

    # --- LAYOUT ---
    search_bar = ft.TextField(
        hint_text="Search Music...", 
        expand=True, 
        border_radius=10,
        on_submit=run_search
    )

    page.add(
        ft.Row([ft.Text("OXCY v2", size=24, weight="bold", color="yellow")], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([search_bar, ft.IconButton(ft.Icons.SEARCH, on_click=run_search)]),
        status_text,
        ft.ExpansionTile(
            title=ft.Text("Debug Logs (Tap to see errors)", color="red", size=12),
            controls=[debug_box]
        ),
        results_list
    )

ft.app(target=main)
