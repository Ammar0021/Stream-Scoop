# Stream Scoop

A Sleek Script for Downloading Videos, Audios, and Subtitles from most websites using `yt-dlp`.

---

## Requirements

- **FFmpeg**: Required for downloading and processing videos and audios.

  - **MacOS/Linux**: Install via Homebrew (Terminal):
    ```sh
    brew install ffmpeg
    ```
  - **Windows**: Install via Chocolatey (Windows Powershell):
    ```sh
    choco install ffmpeg
    ```
- Install FFmpeg manually from: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

- **Python Packages**: Listed in `requirements.txt`.
  - Install them using:
    ```sh
    pip install -r requirements.txt
    ```

---

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

---

## Optional Tools

### aria2c
- A high-performance External Downloader for Faster downloads.
  - If installed, the script will give you an option to either use `aria2c` or `yt-dlp`.
  - Install `aria2c` via `Terminal`/`Windows Powershell`:
    - **MacOS/Linux**:
      ```sh
      brew install aria2
      ```
    - **Windows**:
      ```sh
      choco install aria2
      ```
  - Install `aria2c` Manually from: [https://aria2.github.io/](https://aria2.github.io/)

- **Note:** `aria2c` is NOT guaranteed to boost download speed.

---

### Cookies Support
- Use a browser extension like [Get cookies.txt (LOCALLY)](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) to export cookies.
- When prompted by the script, enter the PATH to your cookies file (Drag and Drop into terminal works). If you don't have a cookies file, you can skip this step, but note that some videos may not be downloadable without cookies.
- Only use cookies when necessary, such as downloading private content/age-restricted content.

- **Note**: Use a TRUSTED Cookie Extractor, as cookie files hold sensitive data.

---

### Direct URL
- If media downloading is unsupported by a particular site, you can use a Chrome Extension like [Video Download Helper](https://chromewebstore.google.com/detail/video-downloadhelper/lmjnegcaeklhafolokijcfjliaokphfk) to extract the Direct URL, which should work in `yt-dlp`.

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

--- 

## Download Logging

- Every successful download is logged in a file named `download_history.txt` (if accepted by the user).
- The log includes:
  - **URL**: The source URL of the downloaded content.
  - **Save Path**: The directory where the file was saved.
  - **Type**: The type of download (e.g., Video, Audio, Subtitles).
  - **Duration**: The time taken to complete the download.
- This log file is stored in the same directory as the download target folder.

---

## Supported Sites

- Refer to [Supported Sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) for a comprehensive lists of yt-dlp supported sites 
- **Note:** yt-dlp will fallback to a Generic Extractor if you download from an unsupported site (This may NOT work all the time)
- **Note:** [Video Download Helper](https://chromewebstore.google.com/detail/video-downloadhelper/lmjnegcaeklhafolokijcfjliaokphfk) extraction of Direct URL will almost always work

---

## License

This project is licensed under the [MIT License](LICENSE)
