import os
import shutil
import subprocess
from utils import ensure_dir, sanitize_filename
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live

console = Console()


def download_videos(url: str, dest_folder: str, model_name: str):
    dest_folder = os.path.expanduser(dest_folder)
    ensure_dir(dest_folder)

    temp = os.path.join(dest_folder, "temp")
    ensure_dir(temp)

    cmd = [
        "yt-dlp",
        "--quiet",
        "--no-warnings",
        "-o",
        os.path.join(temp, "%(title).100s.%(ext)s"),
        url,
    ]

    spinner = Spinner("dots", text="Устанавливаю видео...")
    with Live(spinner, refresh_per_second=10):
        try:
            subprocess.run(cmd, check=True)
            files = sorted(os.listdir(temp))
            safe = sanitize_filename(model_name)
            for i, fname in enumerate(files, start=1):
                ext = os.path.splitext(fname)[1]
                new = f"{safe}_{i:02d}{ext}"
                os.rename(os.path.join(temp, fname), os.path.join(dest_folder, new))
        finally:
            shutil.rmtree(temp, ignore_errors=True)

    console.print(f"[green]Видео установлено:[/] [magenta]{len(files)} файл(ов)[/]")
