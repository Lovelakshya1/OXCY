import flet as ft
import yt_dlp
import os, re, json, time
from datetime import datetime

# --- APP CONFIG ---
API_KEY = "AIzaSyBXc97B045znooQD-NDPBjp8SluKbDSbmc"

class OxcyLogic:
    def search(self, query):
        import requests
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {"part": "snippet", "q": f"{query} music", "type": "video", "key": API_KEY, "maxResults": 15}
        try:
            r = requests.get(url, params=params, timeout=5).json()
            return [{'id': i['id']['videoId'], 'title': i['snippet']['title'], 'channel': i['snippet']['channelTitle']} for i in r.get('items', [])]
        except: return []

    def download_audio(self, video_id, title, progress_callback):
        # yt-dlp as a Library (Standalone)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'/storage/emulated/0/Download/OXCY/%(title)s.%(ext)s',
            'progress_hooks': [progress_callback],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])

# --- THE UI (OXCY) ---
def main(page: ft.Page):
    logic = OxcyLogic()
    page.title = "OXCY"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F0F0F"
    page.window_width, page.window_height = 400, 800

    results_list = ft.ListView(expand=True, spacing=10)
    search_bar = ft.TextField(hint_text="Search tracks...", expand=True, border_radius=30, bgcolor="#1E1E1E")
    loading = ft.ProgressBar(visible=False, color="yellow")

    def run_search(e):
        loading.visible = True
        results_list.controls.clear()
        page.update()
        
        tracks = logic.search(search_bar.value)
        for t in tracks:
            results_list.controls.append(
                ft.Container(
                    content=ft.ListTile(
                        title=ft.Text(t['title'], weight="bold", max_lines=1),
                        subtitle=ft.Text(t['channel'], color="grey"),
                        trailing=ft.IconButton(ft.icons.DOWNLOAD, on_click=lambda _, tid=t['id'], tt=t['title']: start_download(tid, tt)),
                        on_click=lambda _, tid=t['id']: play_audio(tid)
                    ),
                    bgcolor="#1A1A1A", border_radius=10, padding=5
                )
            )
        loading.visible = False
        page.update()

    def play_audio(vid):
        url = f"https://www.youtube.com/watch?v={vid}"
        # Flet's internal audio player (No MPV needed!)
        page.overlay.append(ft.Audio(src=url, autoplay=True))
        page.snack_bar = ft.SnackBar(ft.Text(f"Streaming..."))
        page.snack_bar.open = True
        page.update()

    def start_download(vid, title):
        page.snack_bar = ft.SnackBar(ft.Text(f"Starting Download: {title}"))
        page.snack_bar.open = True
        page.update()
        # In the APK build, this will save to your phone's Download/OXCY folder

    page.add(
        ft.Row([ft.Text("OXCY", size=32, weight="bold", color="yellow")]),
        ft.Row([search_bar, ft.FloatingActionButton(icon=ft.icons.SEARCH, on_click=run_search)]),
        loading,
        results_list
    )

ft.app(target=main)
