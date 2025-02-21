import os
from time import sleep
import sys
import yt_dlp as YT
import colorama as clr
from colorama import Fore
import random as rand
from datetime import datetime

RANDOM_COLOURS = [Fore.RED, Fore.LIGHTRED_EX, Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.YELLOW, Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.CYAN, Fore.LIGHTCYAN_EX,]

clr.init(autoreset=True)

def clear_screen():
    if sys.platform == "win32":
        os.system("cls")
    elif sys.platform in ["linux", "darwin"]:
        os.system("clear")
    else:
        print("\033c", end="") 
        
def get_cookies():
    while True:
        print(Fore.LIGHTBLUE_EX + "\n(🍪) Enter the path to your Cookies File (Press ENTER to Skip): ", end= '')
        cookie_file = input().strip()
        
        cookie_file = cookie_file.strip('"\'')
        
        if not cookie_file:
            print(Fore.LIGHTYELLOW_EX + "\nProceeding without Cookies.."); sleep(0.9)  
            return None
        
        if os.path.exists(cookie_file):
            print(Fore.LIGHTGREEN_EX + "Using Cookies from: " + Fore.WHITE + cookie_file); sleep(0.9)
            return cookie_file
        else:
            print(Fore.LIGHTRED_EX + f"Error: Cookie File {Fore.WHITE}'{cookie_file}'{Fore.LIGHTRED_EX} does not exist!")

def log_download(url, save_path, download_type):
    log_file = os.path.join(save_path, "download_history.txt")
    os.makedirs(save_path, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file, "a") as f:
        f.write(f"{download_type} | {url} | {save_path} | {timestamp}\n\n")

def unique_filename(title):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{title}_{timestamp}"

def download_video_audio(url, save_path, cookie_file=None):
    try:
        resolution_names = {
            "4320p": " (8K)",
            "2160p": " (4K)",
            "1440p": " (Quad HD)",
            "1080p": " (Full HD)",
            "720p": " (HD)"
        }

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'noprogress': False
        }
        
        if cookie_file:
            ydl_opts['cookiefile'] = cookie_file

        with YT.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

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
                        selected_height = sorted_qualities[choice_idx][1]['height']
                        break
                    else:
                        raise ValueError("Invalid selection. Choose a number from the list.")
                except ValueError as e:
                    print(Fore.RED + f"Error: {str(e)}")
                    print(Fore.YELLOW + f"Enter a number between 1 and {len(sorted_qualities)}.\n")
                    
            download_opts = {
                'format': f"bestvideo[height={selected_height}]+bestaudio/best",
                'outtmpl': os.path.join(save_path, f"{unique_filename('%(title)s')}.%(ext)s"),
                'restrictfilenames': True,
                'merge_output_format': 'mp4',
                'concurrent_fragment_downloads': 3,
                'keepalive': True, 
                'force_ip': '4',
                'cookiefile': cookie_file if cookie_file else None,
            }
            
            clear_screen()
            print(Fore.CYAN + " Downloading Video... ".center(50, "="))
            with YT.YoutubeDL(download_opts) as ydl:
                ydl.download([url])

            log_download(url, save_path, "Video")
            clear_screen()
            print(Fore.GREEN + "Download completed successfully!\n")
            print(Fore.LIGHTMAGENTA_EX + "Your video has been saved in:" + Fore.LIGHTYELLOW_EX + f" {save_path}")
            print(Fore.LIGHTBLUE_EX + f"\nYour Download has been Logged in 'download_history.txt")

    except Exception as e:
        handle_error(e)

def download_audio_only(url, save_path, cookie_file=None):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'noprogress': False
        }
        
        if cookie_file:
            ydl_opts['cookiefile'] = cookie_file
            
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
                }],
                'cookiefile': cookie_file if cookie_file else None,
            }

            clear_screen()
            print(Fore.CYAN + f" Downloading Audio ({selected_format['bitrate']}kbps)... ".center(50, "="))
            with YT.YoutubeDL(opts) as ydl:
                ydl.download([url])

            log_download(url, save_path, "Audio")
            print(Fore.GREEN + "\nAudio download completed!")
            print(Fore.LIGHTMAGENTA_EX + "Your Audio has been saved in" + Fore.LIGHTYELLOW_EX + f" {save_path}")
            print(Fore.LIGHTBLUE_EX + f"\nYour Download has been Logged in 'download_history.txt")

    except Exception as e:
        handle_error(e)

def download_subtitles(url, save_path, cookie_file=None) :
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'noprogress': False
        }
        
        if cookie_file:
            ydl_opts['cookiefile'] = cookie_file
            
        with YT.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')  
            unique_name = unique_filename(title) 
            
            
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
        
            while True:
                try:
                    filter_english = input("Display only English subtitles? (Y/n): ").strip().lower()
                    
                    if filter_english in ('', 'y', 'yes', 'n', 'no'):
                        if filter_english in ('', 'y', 'yes'):
                            all_subtitles = [sub for sub in all_subtitles if sub['lang'].lower() == 'en']
                            if not all_subtitles:
                                raise ValueError(Fore.LIGHTRED_EX + "\nNo English subtitles available for this video!")
                        break  
                    else:
                        raise ValueError(Fore.LIGHTRED_EX + "\nInvalid input. Please enter 'Y', 'y', 'Yes', 'N', or 'n'.")
                except ValueError as e:
                    print(e)


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
                
                sys.stdout.flush() 

            current_page = 0
            while True:
                display_page(current_page)
                try:
                    choice = input(f"\nChoose subtitle (number) or navigate ({Fore.YELLOW}n{Fore.WHITE}: next, {Fore.YELLOW}p{Fore.WHITE}: previous): ").strip().lower()

                    if choice == 'n': 
                        if current_page < total_pages - 1:
                            current_page += 1
                        else:
                            current_page = 0  # Wrap around to the first page if on the last page

                    elif choice == 'p':  
                        if current_page > 0:
                            current_page -= 1
                        else:
                            current_page = total_pages - 1  # Wrap around to the last page if on the first page

                    else:
                        choice_idx = int(choice) - 1
                        if 0 <= choice_idx < len(all_subtitles):
                            selected = all_subtitles[choice_idx]
                            break
                        else:
                            print(Fore.RED + f"Error: Invalid selection. Please choose a number between 1 and {len(all_subtitles)}.")
                except ValueError:
                    print(Fore.RED + "Error: Invalid input. Please enter a valid number or navigation command.")

            selected_ext = selected['ext']
            selected_lang = selected['lang']
            
            opts = {
                'writesubtitles': not selected['is_auto'],
                'writeautomaticsub': selected['is_auto'],
                'subtitleslangs': [selected['lang']],
                'subtitlesformat': selected['ext'],
                'skip_download': True,  # Only download subtitles
                'outtmpl': os.path.join(save_path, f"{unique_name}"), 
                'restrictfilenames': True,
                'cookiefile': cookie_file if cookie_file else None,
            }
            
            clear_screen()
            title = f" Downloading {selected['lang'].upper()} Subtitles ({selected['ext'].upper()})... "
            print(Fore.CYAN + title.center(50, "="))
            
            with YT.YoutubeDL(opts) as ydl:
                ydl.download([url])
            
            log_download(url, save_path, "Subtitles")
            print(Fore.GREEN + "\nSubtitles downloaded successfully!")
            print(Fore.LIGHTMAGENTA_EX + "Your Subtitle has been saved in" + Fore.LIGHTYELLOW_EX + f" {save_path}")
            print(Fore.LIGHTBLUE_EX + f"\nYour Download has been Logged in 'download_history.txt")
            
        while True:
            try:
                convert_to_srt = input(f"\n{Fore.YELLOW}Convert subtitles to .srt? ({Fore.WHITE}Y/n): ").strip().lower()
                if convert_to_srt in ('', 'y', 'yes'):
                    subtitle_base = os.path.join(save_path, f"{unique_name}.{selected_lang}") 
                    convert_subtitles_to_srt(subtitle_base, selected_ext)  
                    break
                elif convert_to_srt in ('n', 'no'):
                    break
                else:
                    raise ValueError("Invalid input.")
            except ValueError as e:
                print(e)

    except Exception as e:
        handle_error(e)

def convert_subtitles_to_srt(file_base, current_ext):
    try:
        subtitle_file = f"{file_base}.{current_ext}"
        srt_file = f"{file_base}.srt"

        print(Fore.YELLOW + f"\nDEBUG: Checking for file -> {subtitle_file}");sleep(2)  # Debug line

        if current_ext != 'srt':
            if os.path.exists(subtitle_file):
                os.rename(subtitle_file, srt_file)
                print(Fore.GREEN + f"\nConverted to .srt: {srt_file}")
            else:
                print(Fore.RED + f"Error: File not found: {subtitle_file}")
        else:
            print(Fore.YELLOW + "Subtitles are already in .srt format.")

    except Exception as e:
        print(Fore.RED + f"Error during conversion: {e}")

def download_video_audio_subtitles(url, save_path, cookie_file=None):
    try:
        print(Fore.LIGHTCYAN_EX + " \nDownloading Video and Audio... ".center(50, "="))
        download_video_audio(url, save_path, cookie_file)
        
        print(Fore.LIGHTCYAN_EX + " \n\nDownloading Subtitles... ".center(50, "="))
        download_subtitles(url, save_path, cookie_file)
        
        print(Fore.GREEN + "\nAll downloads completed successfully!")
        print(Fore.LIGHTMAGENTA_EX + "Your files have been saved in:" + Fore.LIGHTYELLOW_EX + f" {save_path}")
        print(Fore.LIGHTBLUE_EX + f"\nYour Download has been Logged in 'download_history.txt'")
    
    except Exception as e:
        handle_error(e)
        

def handle_error(e):
    print(Fore.LIGHTRED_EX + f"\nError: {str(e)}")
    err_msg = str(e).lower()

    if "unable to download webpage" in err_msg or "network" in err_msg or "connection" in err_msg:
        print(Fore.YELLOW + "Check your internet connection! (🌐)")
    
    elif "age restricted" in err_msg or "sign in" in err_msg or "login" in err_msg:
        print(Fore.LIGHTMAGENTA_EX + "Age-restricted or login-required content! Use cookies (🍪).")
    
    elif "private" in err_msg or "unavailable" in err_msg or "not available" in err_msg:
        print(Fore.YELLOW + "Video is private, unavailable, or requires login (🥷)")

    elif "copyright" in err_msg or "blocked" in err_msg or "content not available" in err_msg:
        print(Fore.YELLOW + "Content blocked due to copyright or regional restrictions (©️)")

    elif "ffmpeg" in err_msg or "postprocessing" in err_msg:
        print(Fore.YELLOW + "FFmpeg error. Ensure it's installed and in PATH.")
    
    elif "cookies" in err_msg or "authentication" in err_msg:
        print(Fore.YELLOW + "Cookies error. Ensure the cookies file is valid and up-to-date.")

    elif "live" in err_msg or "streaming" in err_msg:
        print(Fore.YELLOW + "Live streams cannot be downloaded. You can download completed live streams tho.")

    elif "invalid url" in err_msg or "unsupported url" in err_msg:
        print(Fore.YELLOW + "Invalid or unsupported URL. Please check the URL and try again.")
 
    elif "format" in err_msg or "quality" in err_msg or "no video formats found" in err_msg:
        print(Fore.YELLOW + "No downloadable formats found. The video may not be available in the requested format.")
        
    else:
        print(Fore.YELLOW + "An unknown error occurred. Please check the URL, Update yt-dlp, and try again.")
