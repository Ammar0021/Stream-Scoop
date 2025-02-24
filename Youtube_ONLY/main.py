import os
import sys
import colorama as clr
from colorama import Fore
import random as rand
from time import sleep
from urllib.parse import urlparse
import subprocess as sp
import signal

from download_utils import clear_screen, download_video_audio, download_audio_only, download_subtitles, handle_error, get_cookies, download_video_audio_subtitles

clr.init(autoreset=True)  

'''this AUTO creates a "Videos" folder in ur Desktop (if does not exist),
You can Change the Current Default Path, by modifying the DEFAULT_PATH variable below'''
DEFAULT_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "Videos") # '~' is the user's home directory

RANDOM_COLOURS = [Fore.RED, Fore.LIGHTRED_EX, Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.YELLOW, Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.CYAN, Fore.LIGHTCYAN_EX,]

def check_ffmpeg():
    try:
        print(Fore.LIGHTCYAN_EX + "Checking if FFmpeg is Installed...\n"); sleep(1.1)
        sp.run(['ffmpeg', '-version'], stdout=sp.PIPE, stderr=sp.PIPE, check=True)
        return True
    except sp.CalledProcessError:
        return False
    except FileNotFoundError:
        return False
    
def signal_handler(sig, frame):
    '''Handles Ctrl+C Gracefully'''
    signal_name = signal.Signals(sig).name
    print(f'{Fore.LIGHTMAGENTA_EX}\n\nReceived signal {signal_name} ({sig})')
    print(f'{Fore.LIGHTBLUE_EX}Interrupted at {frame.f_code.co_name}() in {frame.f_code.co_filename} at line {frame.f_lineno}')
    print(Fore.LIGHTYELLOW_EX + '\nExiting gracefully...');sleep(0.69696969)
    sys.exit(0)
    
def get_url():
    urls = []
    from colorama import Fore
    print(f"{Fore.LIGHTGREEN_EX}Enter YouTube URLs (one per line). Type {Fore.WHITE}'done'{Fore.LIGHTGREEN_EX} or {Fore.WHITE}'d'{Fore.LIGHTGREEN_EX} to finish:")
   
    while True:
        try:
            print(Fore.LIGHTRED_EX + "\nPaste YouTube URL: ", end='')
            url = input().strip()
            
            if url.lower() in ('done', 'd'):
                if not urls:
                    raise ValueError(Fore.YELLOW + "No URLs entered\n")
                break
            
            validate_url(url)
            urls.append(url)
            print(Fore.LIGHTGREEN_EX + "URL added successfully!")
            
        except ValueError as e:
            print(Fore.LIGHTRED_EX + f"Error: {str(e)}")
            print(Fore.BLUE + "Enter a valid YouTube URL!")       
    return urls    
     
def validate_url(url):
    if url.lower() in ('done', 'd'):
        return True
    
    parsed = urlparse(url)
    valid_schemes = ["http", "https"]
    valid_domains = ["youtube.com","www.youtube.com", "www.youtu.be", "youtu.be"]

    if parsed.scheme not in valid_schemes:
        raise ValueError(f"Invalid URL scheme. Expected {Fore.WHITE}'http' {Fore.LIGHTRED_EX}or {Fore.WHITE}'https'.")
    
    if parsed.netloc not in valid_domains:
        raise ValueError(f"Invalid domain. Expected {Fore.WHITE}'youtube.com' {Fore.LIGHTRED_EX}or {Fore.WHITE}'youtu.be'.")
    return True

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
    print(Fore.LIGHTRED_EX + " YouTube Downloader ".center(50, "=")); sleep(0.5)

    for option in ["\n1. Download Video", "2. Download Audio Only", "3. Download Subtitles", "4. Download Video, Audio & Subtitles"]:
        print(rand.choice(RANDOM_COLOURS) + option); sleep(0.25)
  
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            if choice in ('1', '2', '3', '4'):
                cookie_file = get_cookies()
                clear_screen()
                urls = get_url()
                save_path = get_save_path()

                for url in urls:
                    if choice == '1':
                        print(Fore.BLUE + "\nProcessing URL...")
                        download_video_audio(url, save_path, cookie_file)    
                    elif choice == '2':
                        print(Fore.BLUE + "\nProcessing URL...")
                        download_audio_only(url, save_path, cookie_file)
                    elif choice == '3':
                        print(Fore.BLUE + "\nProcessing URL...")
                        download_subtitles(url, save_path, cookie_file)
                    elif choice == '4':
                        print(Fore.LIGHTRED_EX + "\nProcessing URL...")
                        download_video_audio_subtitles(url, save_path, cookie_file)
                break 
            else:
                raise ValueError(Fore.LIGHTRED_EX + "Invalid choice! Enter 1, 2, or 3.")
        
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")
            print(Fore.YELLOW + "Please enter a number between 1 and 3.\n")
        except Exception as e:
            handle_error(e)
                
if __name__ == "__main__":
    main()
