# xsliv-downloader

Парсер и загрузчик фото/видео с xxsliv.com

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/murfixtap/xsliv_downloader.git
cd xsliv_downloader
```

2. Создайте виртуальное окружение (рекомендуется):
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Установите yt-dlp для видео:
```bash
pip install yt-dlp
```

## Запуск
```bash
python main.py
```

## Использование
1. Введите ссылку на страницу модели (пример: `https://xxsliv.com/model-name.html`)
2. Подтвердите загрузку медиа
3. Выберите тип контента:
   - Фото
   - Видео
   - Оба
4. Укажите папку для сохранения
5. Дождитесь завершения загрузки

Структура после скачивания:
```
model_name/
├── photos/
│   ├── photo_001.jpg
│   └── ...
└── videos/
    ├── model_name_01.mp4
    └── ...
```

Требования:
- Python 3.13+
- Обязательно установленный [yt-dlp](https://github.com/yt-dlp/yt-dlp)
