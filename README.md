# Stream Scoop

A sleek script for downloading videos, audios, and subtitles from most websites using `yt-dlp`.

---

## Requirements

- **FFmpeg**: Required for downloading and processing videos and audios.
  - Install FFmpeg manually from: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
  - **MacOS/Linux**: Install via Homebrew:
    ```sh
    brew install ffmpeg
    ```
  - **Windows**: Install via Chocolatey:
    ```sh
    choco install ffmpeg
    ```

- **Python Packages**: Listed in `requirements.txt`.
  - Install them using:
    ```sh
    pip install -r requirements.txt
    ```

---

## Optional Tools

- **aria2c**: A high-performance external downloader for faster downloads.
  - If installed, the script will automatically use `aria2c` for optimized downloading.
  - Install `aria2c`:
    - **MacOS/Linux**:
      ```sh
      brew install aria2
      ```
    - **Windows**:
      ```sh
      choco install aria2
      ```

---

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Ammar0021/Stream-Scoop.git
    cd Stream-Scoop
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Ensure FFmpeg is installed and added to your system's PATH.

---

## Usage

1. Run the script:
    - **Windows**:
      ```sh
      python main.py
      ```
    - **MacOS/Linux**:
      ```sh
      python3 main.py
      ```

2. Follow the on-screen instructions to:
    - Download videos in various qualities (e.g., 8K, 4K, HD).
    - Extract and download audio tracks in multiple bitrates and formats.
    - Fetch and download subtitles in different languages, including automatic captions.

3. If `aria2c` is installed, it will be used automatically for faster downloads.

---

## Features

- **Video Downloads**: Download videos in multiple resolutions, including 8K, 4K, and HD.
- **Audio Downloads**: Extract and download audio tracks in various bitrates and formats.
- **Subtitle Downloads**: Fetch and download subtitles in different languages, including automatic captions.
- **Cookies Support**: Use cookies to download age-restricted or private videos. The script will prompt you to provide a cookies file if needed.
- **Optimized Downloads**: Supports `aria2c` for faster and more reliable downloads.

---

## Supported Sites

Stream Scoop supports all websites supported by `yt-dlp`. For a full list, refer to the [Supported Sites](supportedsites.md) page.

---

## Cookies

To download age-restricted or private videos, you may need to provide a cookies file. Follow these steps:

1. Use a browser extension like [Get cookies.txt (LOCALLY)](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) to export cookies.
2. When prompted by the script, drag and drop the cookies file or enter its path.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Troubleshooting

- **FFmpeg not found**: Ensure FFmpeg is installed and added to your system's PATH.
- **aria2c not detected**: Install `aria2c` and ensure it is added to your system's PATH.
- **Permission issues**: Run the script with elevated privileges if necessary.