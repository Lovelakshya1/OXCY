import flet as ft
import os
import requests

# --- SAFETY BLOCK ---
# If yt-dlp is missing, the app won't crash. It will just disable download features.
try:
    import yt_dlp
    YTDLP_AVAILABLE = True
except ImportError as e:
    YTDLP_AVAILABLE = False
    YTDLP_ERROR = str(e)

API_KEY = "AIzaSyBXc97B045znooQD-NDPBjp8SluKbDSbmc"

class OxcyLogic:
    def search(self, query):
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {"part": "snippet", "q": f"{query} music", "type": "video", "key": API_KEY, "maxResults": 15}
        try:
            r = requests.get(url, params=params, timeout=5).json()
            return [{'id': i['id']['videoId'], 'title': i['snippet']['title'], 'channel': i['snippet']['channelTitle']} for i in r.get('items', [])]
        except: return []

    def get_stream_url(self, video_id):
        if not YTDLP_AVAILABLE: return None
        try:
            with yt_dlp.YoutubeDL({'format': 'bestaudio[ext=m4a]', 'quiet': True}) as ydl:
                info = ydl.extract_info(video_id, download=False)
                return info['url']
        except: return None

def main(page: ft.Page):
    page.title = "OXCY"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    
    # --- UI COMPONENTS ---
    status_text = ft.Text("Ready", color="grey", size=12)
    results_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    audio_player = ft.Audio(autoplay=True)
    page.overlay.append(audio_player)

    # --- ERROR CHECK ON STARTUP ---
    if not YTDLP_AVAILABLE:
        page.add(ft.Container(
            content=ft.Text(f"CRITICAL ERROR: {YTDLP_ERROR}\nCheck buildozer.spec requirements!", color="white", bgcolor="red"),
            padding=20
        ))

    def run_search(e):
        if not search_bar.value: return
        status_text.value = "Searching..."
        results_list.controls.clear()
        page.update()
        
        tracks = logic.search(search_bar.value)
        if not tracks:
            status_text.value = "No results found."
        else:
            status_text.value = f"Found {len(tracks)} results"
            for t in tracks:
                results_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.Icons.MUSIC_NOTE, color="yellow"),
                            title=ft.Text(t['title'], weight="bold", max_lines=1),
                            subtitle=ft.Text(t['channel']),
                            on_click=lambda _, vid=t['id']: play_track(vid),
                            trailing=ft.IconButton(ft.Icons.PLAY_ARROW, icon_color="white")
                        ),
                        bgcolor="#1A1A1A", border_radius=10, margin=ft.margin.only(bottom=5)
                    )
                )
        page.update()

    def play_track(video_id):
        if not YTDLP_AVAILABLE:
            status_text.value = "Cannot play: Dependency missing."
            page.update()
            return
            
        status_text.value = "Loading Stream..."
        page.update()
        url = logic.get_stream_url(video_id)
        if url:
            audio_player.src = url
            audio_player.update()
            status_text.value = "Playing..."
        else:
            status_text.value = "Stream Failed."
        page.update()

    search_bar = ft.TextField(hint_text="Search...", expand=True, on_submit=run_search)
    
    page.add(
        ft.Row([ft.Text("OXCY", size=24, weight="bold", color="yellow")], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([search_bar, ft.IconButton(ft.Icons.SEARCH, on_click=run_search)]),
        status_text,
        results_list
    )

ft.app(target=main)
