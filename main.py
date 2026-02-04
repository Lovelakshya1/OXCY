import flet as ft
from googleapiclient.discovery import build
import yt_dlp

# --- IDENTITY & INTEL ---
API_KEY = "AIzaSyBXc97B045znooQD-NDPBjp8SluKbDSbmc"
YOUTUBE = build('youtube', 'v3', developerKey=API_KEY)

def search_youtube(query):
    # Lightning fast API search
    request = YOUTUBE.search().list(q=query, part='snippet', type='video', maxResults=10)
    response = request.execute()
    results = []
    for item in response['items']:
        results.append({
            "title": item['snippet']['title'],
            "video_id": item['id']['videoId'],
            "thumb": item['snippet']['thumbnails']['default']['url']
        })
    return results

def main(page: ft.Page):
    page.title = "OXCY ULTIMATE"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"
    page.padding = 20

    # Modern Audio Engine
    audio_player = ft.Audio(src="", autoplay=False)
    page.overlay.append(audio_player)

    search_input = ft.TextField(label="Search Signal", border_color="blue700", expand=True)
    results_list = ft.ListView(expand=1, spacing=10, padding=10)

    def select_track(video_id, title):
        page.snack_bar = ft.SnackBar(ft.Text(f"Targeting: {title}"))
        page.snack_bar.open = True
        # Using yt-dlp as a library to extract stream URL
        with yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'quiet': True}) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            audio_player.src = info['url']
            audio_player.play()
        page.update()

    def run_search(e):
        results_list.controls.clear()
        data = search_youtube(search_input.value)
        for item in data:
            results_list.controls.append(
                ft.ListTile(
                    leading=ft.Image(src=item['thumb'], border_radius=5),
                    title=ft.Text(item['title'], color="white", weight="bold"),
                    subtitle=ft.Text(f"ID: {item['video_id']}", color="blue400"),
                    on_click=lambda _, vid=item['video_id'], t=item['title']: select_track(vid, t)
                )
            )
        page.update()

    page.add(
        ft.Row([search_input, ft.IconButton(ft.icons.SEARCH, on_click=run_search, icon_color="blue700")]),
        results_list
    )

ft.app(target=main)
