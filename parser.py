from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

ua = UserAgent()


def fetch_html(url: str) -> str:
    headers = {"User-Agent": ua.random}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def parse_model_info(url: str) -> tuple[str, list[str], str, str]:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    name_elem = soup.select_one(".girls-name")
    model_name = name_elem.get_text(strip=True) if name_elem else "UnknownModel"

    h_photos = soup.select_one("h2.mb-3")
    h_videos = soup.select_one("h2.my-3")
    photos_header = h_photos.get_text(strip=True) if h_photos else "Фотографии (недоступно)"
    videos_header = h_videos.get_text(strip=True) if h_videos else "Видео (недоступно)"

    gallery = soup.select_one(".girls-gallery")
    image_urls = []
    if gallery:
        links = gallery.select('a[href$=".webp"], a[href$=".jpg"], a[href$=".png"]')
        for a in links:
            href = a.get("href")
            if not href:
                continue
            if not href.startswith("http"):
                href = f"https://xxsliv.com{href}"
            image_urls.append(href)

    return model_name, image_urls, photos_header, videos_header
