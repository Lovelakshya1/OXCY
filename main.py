import flet as ft
import requests
import os
import time

# --- CONFIG ---
# Your API Key (Official YouTube Data API v3)
API_KEY = "AIzaSyBXc97B045znooQD-NDPBjp8SluKbDSbmc"

def main(page: ft.Page):
    page.title = "OXCY"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    
    # --- UI COMPONENTS ---
    status_text = ft.Text("System Ready", color="grey", size=12)
    debug_box = ft.Text("", color="red", size=10, visible=False)
    results_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    audio_player = ft.Audio(autoplay=True)
    page.overlay.append(audio_player)

    def log(msg, color="white"):
        status_text.value = msg
        status_text.color = color
        page.update()

    # --- 1. LIGHTNING FAST SEARCH (API v3) ---
    def run_search(e):
        if not search_bar.value: return
        
        log("Searching YouTube API...", "yellow")
        results_list.controls.clear()
        page.update()
        
        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "part": "snippet",
                "q": f"{search_bar.value} audio", # Optimize for music
                "type": "video",
                "key": API_KEY,
                "maxResults": 15
            }
            # Fast Request
            res = requests.get(url, params=params, timeout=5)
            data = res.json()
            
            items = data.get("items", [])
            if not items:
                log("No results found.", "red")
            else:
                log(f"Found {len(items)} tracks", "green")
                for item in items:
                    results_list.controls.append(create_tile(item))
            page.update()
            
        except Exception as err:
            log(f"Search Error: {str(err)}", "red")

    # --- 2. STREAMING ENGINE (yt-dlp) ---
    def play_track(video_id):
        log(f"Loading stream for {video_id}...", "cyan")
        try:
            import yt_dlp
            ydl_opts = {'format': 'bestaudio[ext=m4a]', 'quiet': True}
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_id, download=False)
                url = info['url']
                
            audio_player.src = url
            audio_player.update()
            log("Now Playing", "green")
            
        except Exception as err:
            log(f"Stream Error: {str(err)}", "red")

    # --- 3. DOWNLOAD ENGINE ---
    def download_track(video_id, title):
        log(f"Downloading {title}...", "yellow")
        try:
            import yt_dlp
            
            # Save to standard Download folder so you can see it
            save_path = "/storage/emulated/0/Download/OXCY"
            
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]', # Pure Audio
                'outtmpl': f'{save_path}/%(title)s.%(ext)s',
                'quiet': True,
                'noplaylist': True,
                'ignoreerrors': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_id])
                
            log(f"Downloaded: {title}", "green")
            page.show_snack_bar(ft.SnackBar(ft.Text(f"Saved to {save_path}"), bgcolor="green"))
            
        except Exception as err:
            log(f"Download Failed: {str(err)}", "red")
            # Permission reminder
            page.show_snack_bar(ft.SnackBar(ft.Text("Check Storage Permissions!"), bgcolor="red"))

    # --- UI HELPER ---
    def create_tile(item):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        channel = item['snippet']['channelTitle']
        
        return ft.Container(
            content=ft.ListTile(
                leading=ft.Icon(ft.Icons.MUSIC_NOTE, color="yellow"),
                title=ft.Text(title, weight="bold", max_lines=1, overflow="ellipsis"),
                subtitle=ft.Text(channel),
                trailing=ft.PopupMenuButton(
                    icon=ft.Icons.MORE_VERT,
                    items=[
                        ft.PopupMenuItem(text="Play", icon=ft.Icons.PLAY_ARROW, on_click=lambda _: play_track(video_id)),
                        ft.PopupMenuItem(text="Download", icon=ft.Icons.DOWNLOAD, on_click=lambda _: download_track(video_id, title)),
                    ]
                ),
                on_click=lambda _: play_track(video_id)
            ),
            bgcolor="#1A1A1A", border_radius=8, margin=ft.margin.only(bottom=5)
        )

    # --- LAYOUT ---
    search_bar = ft.TextField(hint_text="Search Music...", expand=True, border_radius=10, on_submit=run_search)

    page.add(
        ft.Row([ft.Text("OXCY", size=24, weight="bold", color="yellow")], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([search_bar, ft.IconButton(ft.Icons.SEARCH, on_click=run_search)]),
        status_text,
        results_list
    )

ft.app(target=main)
