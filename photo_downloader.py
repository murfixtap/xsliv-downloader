import os
import requests
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from utils import ensure_dir

console = Console()


def download_single_image(url: str, index: int, dest_folder: str) -> tuple[int, str]:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("RGB")
        filename = f"photo_{index:03d}.jpg"
        img.save(os.path.join(dest_folder, filename), "JPEG")
        return index, "success"
    except Exception as e:
        return index, f"error: {e}"


def download_and_convert_images(image_urls: list[str], dest_folder: str) -> tuple[int, int]:
    ensure_dir(dest_folder)
    total = len(image_urls)
    success = 0

    with Progress(
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("📷 Скачивание изображений...", total=total)

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {
                executor.submit(download_single_image, url, i + 1, dest_folder): i
                for i, url in enumerate(image_urls)
            }

            for future in as_completed(futures):
                result = future.result()
                if result[1] == "success":
                    success += 1
                else:
                    console.print(f"[red]✗[/red] {result[0]}: {result[1]}")
                progress.update(task, advance=1)

    return success, total - success
