import os
import sys
from time import sleep
from datetime import datetime
from colorama import init, Fore
from time import perf_counter

init(autoreset=True)

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
            
def create_progress_hook():
    start_time = None
    end_time = None

    def progress_hook(d):
        nonlocal start_time, end_time
        if d['status'] == 'downloading':
            if start_time is None:
                start_time = perf_counter()
        elif d['status'] == 'finished':
            end_time = perf_counter()

    def get_duration():
        if start_time and end_time is not None:
            return end_time - start_time
        return None

    return progress_hook, get_duration

def log_download(url, save_path, download_type, duration=None):
    def ask_log():
        while True:
            try:
                choice = input(Fore.LIGHTMAGENTA_EX + "\nLog this download? (Y/n): ").strip().lower()
                if choice in ('', 'y', 'yes'):
                    return True
                elif choice in ('n', 'no'):
                    return False
                else:
                    raise ValueError("Invalid input. Please enter 'Y' or 'n'.")
            except ValueError as e:
                print(Fore.RED + f"Error: {str(e)}")
    
    if not ask_log():
        return False
            
    log_file = os.path.join(save_path, "download_history.txt")
    os.makedirs(save_path, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    duration_str = ""
    if duration:
        total_seconds = duration
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        
        if hours > 0:
            duration_str = f"{hours}hr {minutes}min {seconds}s"
        elif minutes > 0:
            duration_str = f"{minutes}min {seconds}s"
        else:
            duration_str = f"{seconds}s"
    
    with open(log_file, "a") as f:
        log_entry = f"{download_type} | {url} | {save_path} | {timestamp}"
        if duration_str:
            log_entry += f" | Duration: {duration_str}"
        f.write(log_entry + "\n\n")
    
    return True


def unique_filename(title):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{title}_{timestamp}"

def ask_use_aria2c(aria2c_installed):
    use_aria2c = False
    if aria2c_installed:
        while True:
            choice = input(Fore.LIGHTCYAN_EX + "\nUse Aria2c for Faster Downloads? (Y/n): ").strip().lower()
            if choice in ('', 'y', 'yes'):
                print(Fore.LIGHTGREEN_EX + "Using Aria2c...") ;sleep(0.69)
                use_aria2c = True
                break
            elif choice in ('n', 'no'):
                print(Fore.LIGHTYELLOW_EX + "Using yt-dlp built in Downloader...") ;sleep(0.69)
                use_aria2c = False
                break
            else:
                print(Fore.RED + "Invalid input. Please enter 'Y' or 'n'.")
    return use_aria2c

def handle_error(e):
    print(Fore.LIGHTRED_EX + f"\nError: {str(e)}")
    err_msg = str(e).lower()

    if "unable to download webpage" in err_msg or "network" in err_msg or "connection" in err_msg:
        print(Fore.YELLOW + "Check your internet connection! (🌐)")
    
    elif "age restricted" in err_msg or "sign in" in err_msg or "login required" in err_msg:
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
        print(Fore.YELLOW + "Live streams cannot be downloaded. You can download completed live streams though.")

    elif "invalid url" in err_msg or "unsupported url" in err_msg:
        print(Fore.YELLOW + "Invalid or unsupported URL. Please check the URL and try again.")
 
    elif "format" in err_msg or "quality" in err_msg or "no video formats found" in err_msg:
        print(Fore.YELLOW + "No downloadable formats found. The video may not be available in the requested format.")
        
    else:
        print(Fore.YELLOW + "An unknown error occurred. Please check the URL, your settings, and try again.")