import os
import questionary
from rich.console import Console
from parser import parse_model_info
from photo_downloader import download_and_convert_images
from video_downloader import download_videos
from utils import sanitize_folder_name, ensure_dir

console = Console()


def interactive_prompt():
    url = questionary.text("Введите ссылку на модель (https://xxsliv.com/...):").ask()
    if not url or not url.startswith("https://xxsliv.com/"):
        console.print("[red]Неверная ссылка[/red]")
        return

    model_name, image_urls, h_photos, h_videos = parse_model_info(url)

    console.print(f"[bold]Модель:[/] {model_name}")
    console.print(f"{h_photos}, {h_videos}")

    confirm = questionary.confirm("Скачать медиа?").ask()
    if not confirm:
        return

    options = []
    if "Фотографии" in h_photos:
        options.append("Фото")
    if "Видео" in h_videos:
        options.append("Видео")
    if len(options) == 2:
        options.append("Оба")

    choice = questionary.select("Что скачать?", choices=options).ask()
    if not choice:
        return

    base = questionary.path("Укажите путь для сохранения:").ask()
    if not base:
        return
    base = os.path.expanduser(base)

    model_dir = os.path.join(base, sanitize_folder_name(model_name))
    ensure_dir(model_dir)

    if "Фото" in choice or "Оба" in choice:
        photo_dir = os.path.join(model_dir, "photos") if "Оба" in choice else model_dir
        console.print("[blue]Скачиваем фото...[/blue]")
        ok, fail = download_and_convert_images(image_urls, photo_dir)
        console.print(f"[green]Успешно:[/] {ok}, [red]Ошибки:[/] {fail}")

    if "Видео" in choice or "Оба" in choice:
        video_dir = os.path.join(model_dir, "videos") if "Оба" in choice else model_dir
        video_dir = os.path.expanduser(video_dir)
        download_videos(url, video_dir, model_name)
