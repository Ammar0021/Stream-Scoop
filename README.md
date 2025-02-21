# Stream Scoop

A simple yet powerful script that lets you download videos, audios, and subtitles from various websites

## Requirements

- **FFmpeg**: Required for downloading and processing videos and audios.
  - Install FFmpeg manually from: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- **Python Packages**: Listed in `requirements.txt`
  - Install them using: `pip install -r requirements.txt`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Ammar0021/Stream-Scoop.git
    ```
    ```sh
    cd Stream-Scoop
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Ensure FFmpeg is installed and added to your system's PATH.
    ```sh
    MacOS/Linux: brew install ffmpeg 
    Windows: choco install ffmpeg

## Usage

1. Run the script:
    ```sh
    python main.py
    ```

2. Follow the on-screen instructions to download videos, audios, or subtitles.

## Features

- **Download Videos**: Download videos in various qualities, including 8K,4K and HD
- **Download Audios**: Extract and download audio tracks in multiple bitrates and formats.
- **Download Subtitles**:  Fetch and download subtitles in different languages, including automatic captions.
- **Cookies Support**: Use cookies to download age-restricted or private videos. The script will prompt you to provide a cookies file if needed.

## Supported Sites

Refer to [Supported Sites](supportedsites.md) for a comprehensive lists of yt-dlp supported sites 

## Cookies

- Use a browser extension like [Get cookies.txt (LOCALLY)](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) to Export cookies.
- When prompted by the script, enter the PATH to your cookies file (Drag and Drop works). If you don't have a cookies file, you can skip this step, but note that some videos may not be downloadable without cookies.

## Testing

Refer to [testing.md](testing.md) for scenarios that have been tested to improve the program 

## License

This project is licensed under the MIT License.
