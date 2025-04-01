import os
from time import sleep
import sys
import yt_dlp as YT
import colorama as clr
from colorama import Fore
import subprocess as sp
import readchar
from time import perf_counter

from utilities import clear_screen, log_download, unique_filename, handle_error, create_progress_hook
from colours import *

clr.init(autoreset=True)


def download_video_audio(url, save_path, cookie_file=None, use_aria2c=False):
    try:
        progress_hook, get_duration = create_progress_hook()
        
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
                tbr = f.get('tbr', 0) or 0 
                if res not in video_qualities or (f.get('tbr') is not None and f.get('tbr', 0) > video_qualities[res]['tbr']):
                    video_qualities[res] = {
                        'format_id': f['format_id'],
                        'height': f.get('height', 0),
                        'tbr': tbr,
                    }

            sorted_qualities = sorted(video_qualities.items(), key=lambda x: -x[1]['height'])
            if not sorted_qualities:
                raise ValueError("No downloadable video formats found!")

            clear_screen()
            print(Fore.CYAN + "Available Qualities:\n")
            for i, (res, details) in enumerate(sorted_qualities, 1):
                print(get_next_colour() + f"{i}: {res}")

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
                'keepalive': True, 
                'force_ip': '4',
                'cookiefile': cookie_file if cookie_file else None,
                'progress_hooks': [progress_hook],
            }
            if use_aria2c:
                download_opts['external_downloader'] = 'aria2c'
            
            clear_screen()
            print(Fore.CYAN + " Downloading Video... ".center(50, "="))
            start_time = perf_counter()
            with YT.YoutubeDL(download_opts) as ydl:
                ydl.download([url])
            end_time = perf_counter()

            duration = get_duration() if not use_aria2c else end_time - start_time
            logged = log_download(url, save_path, "Video", duration)
            clear_screen()
            print(Fore.GREEN + "Download completed successfully!\n")
            print(Fore.LIGHTMAGENTA_EX + "Your video has been saved in:" + Fore.LIGHTYELLOW_EX + f" {save_path}")
            if logged:
                print(Fore.LIGHTBLUE_EX + f"\nYour Download has been Logged in 'download_history.txt")

    except Exception as e:
        handle_error(e)

def download_audio_only(url, save_path, cookie_file=None, use_aria2c=False):
    try:
        progress_hook, get_duration = create_progress_hook()
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
                print(get_next_colour() + f"{i}: {fmt['bitrate']}kbps ({fmt['ext']})")

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

            download_opts = {
                'format': selected_format['format_id'],  
                'outtmpl': os.path.join(save_path, f"{unique_filename('%(title)s')}.{selected_format['ext']}"),
                'restrictfilenames': True,
                'cookiefile': cookie_file if cookie_file else None,
                'keepalive': True, 
                'force_ip': '4',
                'progress_hooks': [progress_hook],
            }
            if use_aria2c:
                download_opts['external_downloader'] = 'aria2c'

            clear_screen()
            print(Fore.CYAN + f" Downloading Audio ({selected_format['bitrate']}kbps)... ".center(50, "="))
            with YT.YoutubeDL(download_opts) as ydl:
                ydl.download([url])

            duration = get_duration()
            logged = log_download(url, save_path, "Audio", duration)
            print(Fore.GREEN + "\nAudio download completed!")
            print(Fore.LIGHTMAGENTA_EX + "Your Audio has been saved in" + Fore.LIGHTYELLOW_EX + f" {save_path}")
            if logged:
                print(Fore.LIGHTBLUE_EX + f"\nYour Download has been Logged in 'download_history.txt")

    except Exception as e:
        handle_error(e)

def download_subtitles(url, save_path, cookie_file=None) :
    try:
        progress_hook, get_duration = create_progress_hook()
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
                    print(get_next_colour() + f"{i + 1}: {sub['lang'].upper()} ({sub_type}) - {sub['ext'].upper()}")
                
                sys.stdout.flush() 

            current_page = 0
            
            while True:
                display_page(current_page)
                print(Fore.YELLOW + "\nNavigate with " + 
                      Fore.CYAN + "←/A" + Fore.YELLOW +
                      Fore.CYAN + " →/D" + Fore.YELLOW + " | Select " +
                      Fore.CYAN + "number" + Fore.YELLOW + " to choose")
                
                try:
                    key = readchar.readkey()
                    
                    if key == readchar.key.LEFT:
                        key = 'a'
                    elif key == readchar.key.RIGHT:
                        key = 'd'
                    else:
                        key = key.lower()
                    
                    if key in ('a', 'd'):
                        # Wrap-around page navigation
                        if key == 'a':
                            current_page = current_page - 1 if current_page > 0 else total_pages - 1
                        else:
                            current_page = current_page + 1 if current_page < total_pages - 1 else 0
                        continue
                    
                    if key.isdigit():
                        choice_idx = int(key) - 1
                        if 0 <= choice_idx < len(all_subtitles):
                            selected = all_subtitles[choice_idx]
                            break
                        else:
                            print(Fore.RED + f"Error: Invalid selection. Choose 1-{len(all_subtitles)}")
                    else:
                        print(Fore.RED + "Invalid input. Use arrows/A/D or numbers")

                except Exception as e:
                    print(Fore.RED + f"Error: {str(e)}")

            selected_ext = selected['ext']
            selected_lang = selected['lang']
            
            download_opts = {
                'writesubtitles': not selected['is_auto'],
                'writeautomaticsub': selected['is_auto'],
                'subtitleslangs': [selected['lang']],
                'subtitlesformat': selected['ext'],
                'skip_download': True,  # Only download subtitles
                'outtmpl': os.path.join(save_path, f"{unique_name}"), 
                'restrictfilenames': True,
                'cookiefile': cookie_file if cookie_file else None,
                'progress_hooks': [progress_hook],
            }
            
            clear_screen()
            title = f" Downloading {selected['lang'].upper()} Subtitles ({selected['ext'].upper()})... "
            print(Fore.CYAN + title.center(50, "="))
            
            with YT.YoutubeDL(download_opts) as ydl:
                ydl.download([url])
            
            duration = get_duration()
            logged = log_download(url, save_path, "Subtitles", duration)
            print(Fore.GREEN + "\nSubtitles downloaded successfully!")
            print(Fore.LIGHTMAGENTA_EX + "Your Subtitle has been saved in" + Fore.LIGHTYELLOW_EX + f" {save_path}")
            if logged:
                print(Fore.LIGHTBLUE_EX + f"\nYour Download has been Logged in 'download_history.txt")
            
            while True:
                try:
                    convert_to_srt = input(f"\n{Fore.LIGHTRED_EX}Convert subtitles to .srt? ({Fore.WHITE}Y/n): ").strip().lower()
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

        print(Fore.YELLOW + f"\nDEBUG: Checking for file -> {subtitle_file}")
        sleep(1)  # Debug line

        if current_ext == 'srt':
            print(Fore.YELLOW + "Subtitles are already in .srt format.")
            return
        
        sp.run(
            ['ffmpeg', '-i', subtitle_file, '-c:s', 'srt', srt_file], 
            check=True, 
            stdout=sp.PIPE, 
            stderr=sp.PIPE, 
            text=True
        )
        
        # Remove original file after successful conversion
        if os.path.exists(subtitle_file):
            os.remove(subtitle_file)
        
        print(Fore.GREEN + f"\nConverted to .srt: {srt_file}")

    except sp.CalledProcessError as e:
        print(Fore.RED + f"FFmpeg Error: {e.stderr}")
        
        # Cleanup failed output
        if os.path.exists(srt_file):
            os.remove(srt_file)
    except Exception as e:
        print(Fore.RED + f"General Error: {str(e)}")
        if os.path.exists(srt_file):
            os.remove(srt_file)
        
def download_video_audio_subtitles(url, save_path, cookie_file=None, use_aria2c=False):
    try:
        print(Fore.LIGHTCYAN_EX + " \nDownloading Video and Audio... ".center(50, "="))
        download_video_audio(url, save_path, cookie_file)
        
        print(Fore.LIGHTCYAN_EX + " \n\nDownloading Subtitles... ".center(50, "="))
        download_subtitles(url, save_path, cookie_file)
        
        print(Fore.GREEN + "\nAll downloads completed successfully!")
        print(Fore.LIGHTMAGENTA_EX + "Your files have been saved in:" + Fore.LIGHTYELLOW_EX + f" {save_path}")
    
    except Exception as e:
        handle_error(e)
