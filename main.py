import flet as ft
import subprocess, os, re, json, time

# --- LOGIC FROM OXCY.PY ---
API_KEY = "AIzaSyBXc97B045znooQD-NDPBjp8SluKbDSbmc"

class AppLogic:
    def clean_title(self, title):
        patterns = [r'\(Official Video\)', r'\[Official Video\]', r'\(Lyrics\)', r'\|.*$']
        for p in patterns: title = re.sub(p, '', title, flags=re.IGNORECASE)
        return title.strip()

    def search_music(self, query):
        import requests
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {"part": "snippet", "q": f"{query} music", "type": "video", "key": API_KEY, "maxResults": 10}
        try:
            data = requests.get(url, params=params).json()
            return [{'id': i['id']['videoId'], 'title': self.clean_title(i['snippet']['title']), 'channel': i['snippet']['channelTitle']} for i in data.get('items', [])]
        except: return []

# --- ULTIMATE UI ---
def main(page: ft.Page):
    logic = AppLogic()
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#121212"
    
    results_list = ft.ListView(expand=True, spacing=10)
    search_bar = ft.TextField(hint_text="Search Music...", expand=True, border_radius=30)
    
    def handle_search(e):
        results_list.controls.clear()
        page.update()
        data = logic.search_music(search_bar.value)
        for track in data:
            results_list.controls.append(
                ft.ListTile(
                    title=ft.Text(track['title'], weight="bold"),
                    subtitle=ft.Text(track['channel']),
                    trailing=ft.IconButton(ft.icons.DOWNLOAD, on_click=lambda _: print(f"Downloading {track['id']}")),
                )
            )
        page.update()

    page.add(
        ft.Row([search_bar, ft.FloatingActionButton(icon=ft.icons.SEARCH, on_click=handle_search)]),
        results_list
    )

ft.app(target=main)
