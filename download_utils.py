import os
from time import sleep
import sys
import yt_dlp as YT
import colorama as clr
from colorama import Fore
from tqdm import tqdm
import re
import random as rand

RANDOM_COLOURS = [Fore.RED, Fore.LIGHTRED_EX, Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.YELLOW, Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.CYAN, Fore.LIGHTCYAN_EX,]

clr.init(autoreset=True)

def clear_screen():
    if sys.platform == "win32":
        os.system("cls")
    elif sys.platform in ["linux", "darwin"]:
        os.system("clear")
    else:
        print("\033c", end="")        

def create_progress_hook(desc):
    pbar = None

    def progress_hook(d):
        nonlocal pbar
        if d['status'] == 'downloading':
            if pbar is None:
                pbar = tqdm(
                    total=100,
                    desc=desc,
                    unit="%",
                    bar_format="{l_bar}{bar}| {n:.1f}% [{elapsed}<{remaining}]",
                    colour='yellow'  
                )
            if '_percent_str' in d:
                # Remove ANSI color codes and strip '%'
                percent_str = re.sub(r'\x1b\[[0-9;]*m', '', d['_percent_str'])
                current_percent = float(percent_str.strip('%'))
                pbar.update(current_percent - pbar.n)

                # Change color to green when nearing completion
                if current_percent >= 95:
                    pbar.colour = 'green'
        elif d['status'] == 'finished':
            if pbar:
                pbar.colour = 'green' 
                pbar.close()
                pbar = None

    return progress_hook

def log_download(url, save_path, download_type):
    log_file = os.path.join(save_path, "download_history.txt")
    with open(log_file, "a") as f:
        f.write(f"{download_type} | {url} | {save_path}\n")

def unique_filename(save_path, title, ext):
    base_filename = os.path.join(save_path, f"{title}.{ext}")
    if not os.path.exists(base_filename):
        return base_filename

    counter = 1
    while True:
        new_filename = os.path.join(save_path, f"{title}{counter}.{ext}")
        if not os.path.exists(new_filename):
            return new_filename
        counter += 1

def download_video_audio(url, save_path):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True
        }

        with YT.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:  # Check if it's a playlist
                print(Fore.CYAN + "Playlist detected. Displaying videos...\n"); sleep(1.5)
                entries = info['entries']
                for i, entry in enumerate(entries, 1):
                    print(f"{i}. {entry['title']}")

                while True:
                    try:
                        choices = input("\nEnter the numbers of the videos to download (comma-separated, e.g., 1,3,5): ").strip()
                        choice_indices = [int(x) - 1 for x in choices.split(',')]
                        if all(0 <= idx < len(entries) for idx in choice_indices):
                            break
                        else:
                            raise ValueError("Invalid selection. Please choose numbers from the list.")
                    except ValueError as e:
                        print(Fore.RED + f"Error: {str(e)}")
                        print(Fore.YELLOW + f"Please enter valid numbers separated by commas.\n")

                selected_entries = [entries[idx] for idx in choice_indices]
                ydl_opts.update({
                    'outtmpl': os.path.join(save_path, '%(playlist_title)s/%(title)s.%(ext)s'),
                    'progress_hooks': [create_progress_hook("Downloading Playlist")],
                })
                with YT.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([entry['webpage_url'] for entry in selected_entries])
                log_download(url, save_path, "Playlist")
                clear_screen()
                print(Fore.GREEN + "Selected videos from playlist downloaded successfully!\n")
                print(Fore.LIGHTMAGENTA_EX + "Your videos have been saved in" + Fore.LIGHTYELLOW_EX + f" {save_path}")
                return

            if info.get('is_live'):
                raise ValueError("Live streams cannot be Downloaded, You can still Download Live Streams that are Over tho") 
            formats = info.get('formats', [])
            video_qualities = {}

            for f in formats:
                if f.get('vcodec') == 'none' or f.get('format_note') == 'storyboard' or f.get('quality') == -1:
                    continue

                res = f"{f.get('height', '?')}p" 
                if res not in video_qualities or f.get('tbr', 0) > video_qualities[res]['tbr']:
                    video_qualities[res] = {
                        'format_id': f['format_id'],
                        'height': f.get('height', 0),
                        'tbr': f.get('tbr', 0)
                    }

            sorted_qualities = sorted(video_qualities.items(), key=lambda x: -x[1]['height'])
            if not sorted_qualities:
                raise ValueError("No downloadable video formats found!")  
            
            resolution_names = {
                "4320p": " (8K)",
                "2160p": " (4K)",
                "1440p": " (Quad HD)",
                "1080p": " (Full HD)",
                "720p": " (HD)"
            }
            
            clear_screen()
            print(Fore.CYAN + "Available Qualities:\n")
            for i, (res, details) in enumerate(sorted_qualities, 1):
                res_name = resolution_names.get(res, "")
                print(rand.choice(RANDOM_COLOURS) + f"{i}: {res}{res_name}")

            while True:
                try:
                    choice = input("\nChoose quality (number): ").strip()
                    choice_idx = int(choice) - 1
                    
                    if 0 <= choice_idx < len(sorted_qualities):
                        break  
                    else:
                        raise ValueError("Invalid selection. Please choose a number from the list.")
                except ValueError as e:
                    print(Fore.RED + f"Error: {str(e)}")
                    print(Fore.YELLOW + f"Please enter a number between 1 and {len(sorted_qualities)}.\n")
                    
            selected_height = sorted_qualities[choice_idx][1]['height']
            
            download_opts = {
                    'format': f"bestvideo[height={selected_height}]+bestaudio/best",
                    'outtmpl': unique_filename(save_path, '%(title)s.%(ext)s'),
                    'restrictfilenames': True,
                    'merge_output_format': 'mp4',  # This already triggers merging to MP4
                    'progress_hooks': [create_progress_hook("Downloading Video+Audio")],
                    #'concurrent-fragments': 5,
             }

            clear_screen()
            print(Fore.CYAN + " Downloading Video+Audio... ".center(50, "="))
            with YT.YoutubeDL(download_opts) as ydl:
                ydl.download([url])
            
            log_download(url, save_path, "Video")
            clear_screen()
            print(Fore.GREEN + "Download completed successfully!\n")
            print(Fore.LIGHTMAGENTA_EX + "Your Video has been saved in" + Fore.LIGHTYELLOW_EX + f" {save_path}")

    except Exception as e:
        handle_error(e)

def download_audio_only(url, save_path):
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with YT.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])

            audio_formats = []
            for f in formats:
                abr = f.get('abr', 0)
                if f.get('vcodec') == 'none' and abr and abr > 0:
                    audio_formats.append({
                        'format_id': f['format_id'],
                        'bitrate': f.get('abr', 0) or 0,  
                        'ext': f.get('ext', 'mp3')  
                    })
  
            audio_formats.sort(key=lambda x: x['bitrate'], reverse=True)
            if not audio_formats:
                raise ValueError("No downloadable audio formats found!")  
       
            clear_screen()
            print(Fore.CYAN + "Available Audio Qualities:\n")
            for i, fmt in enumerate(audio_formats, 1):
                print(rand.choice(RANDOM_COLOURS) + f"{i}: {fmt['bitrate']}kbps ({fmt['ext']})")

            while True:
                try:
                    choice = input("\nChoose quality (number): ").strip()
                    choice_idx = int(choice) - 1

                    if 0 <= choice_idx < len(audio_formats):
                        break  
                    else:
                        print(Fore.RED + f"Error: Invalid selection. Please choose a number between 1 and {len(audio_formats)}.")
                except ValueError:
                    print(Fore.RED + "Error: Invalid input. Please enter a valid number.")

            selected_format = audio_formats[choice_idx]

            bitrate = selected_format.get('bitrate', 0)
            preferred_quality = max(0, min(int(bitrate // 32), 9)) if bitrate > 0 else 5

            opts = {
                'format': selected_format['format_id'],  
                'outtmpl': unique_filename(save_path, '%(title)s.%(ext)s'),
                'restrictfilenames': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': str(preferred_quality),
                    #'concurrent-fragments': 7,  
                }],
                'progress_hooks': [create_progress_hook("Downloading Audio")],
            }

            clear_screen()
            print(Fore.CYAN + f" Downloading Audio ({selected_format['bitrate']}kbps)... ".center(50, "="))
            with YT.YoutubeDL(opts) as ydl:
                ydl.download([url])

            log_download(url, save_path, "Audio")
            print(Fore.GREEN + "\nAudio download completed!")
            print(Fore.LIGHTMAGENTA_EX + "Your Audio has been saved in" + Fore.LIGHTYELLOW_EX + f" {save_path}")

    except Exception as e:
        handle_error(e)

def download_subtitles(url, save_path):
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with YT.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            all_subtitles = []
            for lang, formats in info.get('subtitles', {}).items():
                for fmt in formats:
                    all_subtitles.append({
                        'lang': lang,
                        'ext': fmt.get('ext', 'vtt'),
                        'is_auto': False,
                        'name': fmt.get('name', '')
                    })

            for lang, formats in info.get('automatic_captions', {}).items():
                for fmt in formats:
                    all_subtitles.append({
                        'lang': lang,
                        'ext': fmt.get('ext', 'vtt'),
                        'is_auto': True,
                        'name': fmt.get('name', '')
                    })
            
            if not all_subtitles:
                raise ValueError("No subtitles available for this video!")
            
            filter_english = input("Display only English subtitles? (Y/n): ").strip().lower()
            if filter_english in ('', 'y', 'yes'):
                all_subtitles = [sub for sub in all_subtitles if sub['lang'].lower() == 'en']
                if not all_subtitles:
                    raise ValueError("No English subtitles available for this video!")

            page_size = 20
            total_pages = (len(all_subtitles) + page_size - 1) // page_size

            def display_page(page):
                clear_screen()
                start = page * page_size
                end = min(start + page_size, len(all_subtitles))
                print(Fore.CYAN + f"Available Subtitles (Page {page + 1}/{total_pages}):\n")
                for i in range(start, end):
                    sub = all_subtitles[i]
                    sub_type = "Auto" if sub['is_auto'] else "Manual"
                    print(rand.choice(RANDOM_COLOURS) + f"{i + 1}: {sub['lang'].upper()} ({sub_type}) - {sub['ext'].upper()}")

            current_page = 0
            while True:
                display_page(current_page)
                try:
                    choice = input("\nChoose subtitle (number) or navigate (n: next, p: previous): ").strip()
                    if choice.lower() == 'n' and current_page < total_pages - 1:
                        current_page += 1
                    elif choice.lower() == 'p' and current_page > 0:
                        current_page -= 1
                    else:
                        choice_idx = int(choice) - 1
                        if 0 <= choice_idx < len(all_subtitles):
                            selected = all_subtitles[choice_idx]
                            break
                        else:
                            print(Fore.RED + f"Error: Invalid selection. Please choose a number between 1 and {len(all_subtitles)}.")
                except ValueError:
                    print(Fore.RED + "Error: Invalid input. Please enter a valid number or navigation command.")

            opts = {
                'writesubtitles': not selected['is_auto'],
                'writeautomaticsub': selected['is_auto'],
                'subtitleslangs': [selected['lang']],
                'subtitlesformat': selected['ext'],
                'skip_download': True,  # Only download subtitles
                'outtmpl': unique_filename(save_path, '%(title)s.%(ext)s'),
                'restrictfilenames': True,
                'progress_hooks': [create_progress_hook("Downloading Subtitles")],
            }

            clear_screen()
            title = f" Downloading {selected['lang'].upper()} Subtitles ({selected['ext'].upper()})... "
            print(Fore.CYAN + title.center(50, "="))
            
            with YT.YoutubeDL(opts) as ydl:
                ydl.download([url])
            
            log_download(url, save_path, "Subtitles")
            print(Fore.GREEN + "\nSubtitles downloaded successfully!")
            print(Fore.LIGHTMAGENTA_EX + "Your Subtitle has been saved in" + Fore.LIGHTYELLOW_EX + f" {save_path}")

    except Exception as e:
        handle_error(e)
        
def handle_error(e):
    print(Fore.LIGHTRED_EX + f"\nError: {str(e)}")
    err_msg = str(e).lower()
    
    if "unreachable" in err_msg or "connection" in err_msg:
        print(Fore.YELLOW + "Check your internet connection! (🌐)")
    elif "age restricted" in err_msg:
        print(Fore.LIGHTMAGENTA_EX + "Age-restricted content! Use cookies (🍪).")
    elif "private" in err_msg:
        print(Fore.YELLOW + "Video is private or requires login (🥷)")
    elif "copyright" in err_msg:
        print(Fore.YELLOW + "Content blocked due to copyright (©️)")
    elif "ffmpeg" in err_msg:
        print(Fore.YELLOW + "FFmpeg error. Ensure it's installed and in PATH")
    else:
        print(Fore.YELLOW + "Unknown error occurred. Please try again")

        

