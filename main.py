import os
import sys
import colorama as clr
from colorama import Fore
from time import sleep
import subprocess as sp
import signal
import yt_dlp as YT

from download_logic import  download_video_audio, download_audio_only, download_subtitles, download_video_audio_subtitles
from utilities import clear_screen, handle_error, get_cookies
from colours import *

clr.init(autoreset=True)  

'''this AUTO creates a "Scooped" folder on ur Desktop (if does not exist),
You can Change the Current Default Path, by modifying the DEFAULT_PATH variable below'''
DEFAULT_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "Scooped") # '~' is the user's home directory

def check_ffmpeg():
    try:
        print(Fore.LIGHTCYAN_EX + "Checking if FFmpeg is Installed...\n"); sleep(0.6969)
        sp.run(['ffmpeg', '-version'], stdout=sp.PIPE, stderr=sp.PIPE, check=True)
        return True
    except sp.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

'''Handles Ctrl + C Gracefully'''    
def signal_handler(sig, frame):
    signal_name = signal.Signals(sig).name
    print(f'{Fore.LIGHTMAGENTA_EX}\n\nReceived signal {signal_name} ({sig})')
    print(f'{Fore.LIGHTBLUE_EX}Interrupted at {frame.f_code.co_name}() in {frame.f_code.co_filename} at line {frame.f_lineno}')
    print(Fore.LIGHTYELLOW_EX + '\nExiting gracefully...')
    sys.exit(0)
    
def get_url():
    urls = []
    print(f"{Fore.LIGHTGREEN_EX}Enter URLs (one per line). Type {Fore.WHITE}'done'{Fore.LIGHTGREEN_EX} or {Fore.WHITE}'d'{Fore.LIGHTGREEN_EX} to finish:")
   
    while True:
        try:
            print(Fore.LIGHTRED_EX + "\nPaste URL: ", end='')
            url = input().strip()
            
            if url.lower() in ('done', 'd'):
                if not urls:
                    raise ValueError(Fore.YELLOW + "No URLs entered\n")
                break
            
            if url:  # Check if the URL is not empty
                urls.append(url)
                print(Fore.LIGHTGREEN_EX + "URL added successfully!")
            else:
                print(Fore.LIGHTRED_EX + "Error: URL cannot be empty. Please enter a valid URL.")
            
        except ValueError as e:
            print(Fore.LIGHTRED_EX + f"Error: {str(e)}")
            print(Fore.BLUE + "Enter a valid URL!")       
    return urls
       
def get_save_path():
    print(Fore.LIGHTBLUE_EX + f"\nDefault download path: {DEFAULT_PATH}")

    while True:
        try:
            choice = input("Use default path? (Y/n): ").strip().lower()
            if choice in ('', 'y', 'yes'):
                save_path = DEFAULT_PATH
                break  
            elif choice in ('n', 'no'):
                try:
                    save_path = input(Fore.WHITE + "\nEnter custom path: ").strip()
                                      
                    save_path = save_path.strip('"\'')
                    save_path = os.path.expanduser(save_path)
                    save_path = os.path.expandvars(save_path)

                    if not os.path.exists(save_path):
                        raise ValueError(f"Path: '{save_path}' does not exist!")
                    if not os.path.isdir(save_path):
                        raise ValueError(f"'{save_path}' is not a directory!")
                    
                    break  
                except ValueError as e:
                    print(Fore.RED + f"Error: {e}")
                    print(Fore.YELLOW + "Please enter a valid directory path.\n")
                    
            else:
                raise ValueError("Invalid input. Please enter 'Y' or 'n'.")

        except ValueError as e:
            print(Fore.RED + f"Error: {e}")
            print(Fore.YELLOW + "Please enter 'Y' for yes or 'n' for no.\n")

    return save_path

def main():
    clear_screen()
    signal.signal(signal.SIGINT, signal_handler)
    
    if not check_ffmpeg():
        clear_screen()
        print(Fore.RED + "FFmpeg is not installed or not in PATH!")
        print(Fore.LIGHTBLUE_EX + "FFmpeg is needed to Download Videos"); sleep(1)
        print(Fore.LIGHTYELLOW_EX + "\nDownload FFmpeg from: " + Fore.LIGHTWHITE_EX + "https://ffmpeg.org/download.html\n")
        sys.exit(1)

    clear_screen()
    print(get_next_colour() + " Stream Scooper ".center(50, "=")); sleep(0.5)
    
    for option in ["\n1. Download Video", "2. Download Audio Only", "3. Download Subtitles", "4. Download Video, Audio & Subtitles"]:
        print(get_next_colour() + option); sleep(0.25)
  
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            if choice in ('1', '2', '3', '4'):
                cookie_file = get_cookies()
                clear_screen()
                urls = get_url()
                save_path = get_save_path()
                
                expanded_urls = []
                for url in urls:
                    print(Fore.LIGHTBLACK_EX + "\nProcessing URL...")
                    try:
                        '''Playlist Handling'''
                        ydl_opts = {
                            'quiet': True,
                            'extract_flat': 'in_playlist',
                            'cookiefile': cookie_file if cookie_file else None,
                        }
                        with YT.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(url, download=False)
                            if 'entries' in info:  # if playlist...
                                print(Fore.LIGHTGREEN_EX + f"\nFound playlist with {len(info['entries'])} videos. Processing each...")
                                for entry in info['entries']:
                                    if 'url' in entry:
                                        expanded_urls.append(entry['url'])
                                    else:
                                        print(Fore.YELLOW + f"Skipping invalid entry in playlist: {url}")
                            else:  # Single video
                                expanded_urls.append(url)
                    except Exception as e:
                        print(Fore.RED + f"Error processing {url}: {str(e)}")
                        expanded_urls.append(url)  # Add original URL for fallback processing

                urls = expanded_urls 
                for url in urls:
                    if choice == '1':
                        #print(Fore.BLUE + "\nProcessing URL...")
                        download_video_audio(url, save_path, cookie_file)    
                    elif choice == '2':
                        #print(Fore.BLUE + "\nProcessing URL...")
                        download_audio_only(url, save_path, cookie_file)
                    elif choice == '3':
                        #print(Fore.BLUE + "\nProcessing URL...")
                        download_subtitles(url, save_path, cookie_file)
                    elif choice == '4':
                        #print(Fore.LIGHTRED_EX + "\nProcessing URL...")
                        download_video_audio_subtitles(url, save_path, cookie_file)
                break 
            else:
                raise ValueError(Fore.LIGHTRED_EX + "Invalid choice! Enter 1, 2, 3 or 4")
        
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")
            print(Fore.YELLOW + "Please enter a number between 1 and 4.\n")
        except Exception as e:
            handle_error(e)
                
if __name__ == "__main__":
    main()