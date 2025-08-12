import sys
import json
import asyncio
from json import dumps, loads
from time import sleep, time
import threading
from datetime import datetime, timedelta
import aiohttp
import discord
import random
import platform
import os
import requests
from colorama import init, Fore, Back, Style
import psutil 
import io
import base64


init()

VOICE_THREADS = []
VOICE_LOOP_TASKS = {}  
USER_TOKEN = None
ALLOWED_USER_ID = None
PREFIX = None
REPLY_ACTIVE = False
client = discord.Client(intents=discord.Intents.all())
spam_states = {}
spam_threads = {}
spam_files = {}
spam_datoken_files = {}
start_time = time()
replied_users = set()  
MAX_FILE_SIZE = 100 * 1024 * 1024  


GIF_LINKS = [
    "https://imgur.com/a/2wYOPOL",
    "https://imgur.com/a/hRWNtLC",
    "https://imgur.com/a/jNtnbkm",
    "https://imgur.com/a/Y6Pme39",
    "https://imgur.com/a/WzzRTFm",
    "https://imgur.com/a/xNUjtQz",
    "https://imgur.com/a/iJMWtca",
    "https://imgur.com/a/Mol84zi",
    "https://imgur.com/a/yBVW9ep"
]

API_URL = "http://dangkhoadeptrai.com"
ASCII_ART = [
    f"{Fore.RED}⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.RED}\n\n{Style.RESET_ALL}",  
    f"{Fore.YELLOW}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.YELLOW}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠶⠚⠉⢉⣩⠽⠟⠛⠛⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.LIGHTYELLOW_EX}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠉⠀⢀⣠⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.LIGHTYELLOW_EX}⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⠁⠀⠀⣰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.GREEN}⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠀⠀⠀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⡤⠤⠄⢤⣄⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.GREEN}⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠒⠋⠉⠀⠀⠀⣀⣤⠴⠒⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.BLUE}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⡄⠀⠀⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⢳⡄⢀⡴⠚⠉⠀⠀⠀⠀⠀⣠⠴⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.BLUE}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠘⣧⠀⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠹⡏⠀⠀⠀⠀⠀⣀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.CYAN}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⢬⣳⣄⣠⠤⠤⠶⠶⠒⠋⠀⠀⠀⠀⠹⡀⠀⠀⠀⠀⠈⠉⠛⠲⢦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.CYAN}⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠤⠖⠋⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⡀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠉⢳⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.MAGENTA}⠀⠀⠀⠀⠀⠀⠀⠀⣠⠖⠋⠀⠀⠀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢱⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⢃⠈⠙⠲⣄⡀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.MAGENTA}⠀⠀⠀⠀⠀⠀⢠⠞⠁⠀⠀⠀⢀⢾⠃⠀⠀⠀⠀⠀⠀⠀⠀⢢⠀⠀⠀⠀⠀⠀⠀⢣⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⠮⣄⠀⠀⠀⠙⢦⡀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.RED}⠀⠀⠀⠀⠀⣰⠋⠀⠀⢀⡤⡴⠃⠈⠦⣀⠀⠀⠀⠀⠀⠀⢀⣷⢸⠀⠀⠀⠀⢀⣀⠘⡄⠤⠤⢤⠔⠒⠂⠉⠁⠀⠀⠀⠑⢄⡀⠀⠀⠙⢦⡀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.YELLOW}⠀⠀⠀⠀⣼⠃⠀⠀⢠⣞⠟⠀⠀⠀⡄⠀⠉⠒⠢⣤⣤⠄⣼⢻⠸⠀⠀⠀⠀⠉⢤⠀⢿⡖⠒⠊⢦⠤⠤⣀⣀⡀⠀⠀⠀⠈⠻⡝⠲⢤⣀⠙⢦⠀⠀{Style.RESET_ALL}",  
    f"{Fore.LIGHTYELLOW_EX}⠀⠀⠀⢰⠃⠀⠀⣴⣿⠎⠀⠀⢀⣜⠤⠄⢲⠎⠉⠀⠀⡼⠸⠘⡄⡇⠀⠀⠀⠀⢸⠀⢸⠘⢆⠀⠘⡄⠀⠀⠀⢢⠉⠉⠀⠒⠒⠽⡄⠀⠈⠙⠮⣷⡀{Style.RESET_ALL}",  
    f"{Fore.GREEN}⠀⠀⠀⡟⠀⠀⣼⢻⠧⠐⠂⠉⡜⠀⠀⡰⡟⠀⠀⠀⡰⠁⡇⠀⡇⡇⠀⠀⠀⠀⢺⠇⠀⣆⡨⢆⠀⢽⠀⠀⠀⠈⡷⡄⠀⠀⠀⠀⠹⡄⠀⠀⠀⠈⠁{Style.RESET_ALL}",  
    f"{Fore.BLUE}⠀⠀⢸⠃⠀⠀⢃⠎⠀⠀⠀⣴⠃⠀⡜⠹⠁⠀⠀⡰⠁⢠⠁⠀⢸⢸⠀⠀⠀⢠⡸⢣⠔⡏⠀⠈⢆⠀⣗⠒⠀⠀⢸⠘⢆⠀⠀⠀⠀⢳⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.CYAN}⠀⠀⢸⠀⠀⠀⡜⠀⠀⢀⡜⡞⠀⡜⠀⠘⠀⠀⢰⠃⠀⠀⡇⠈⠁⠀⢿⠀⠀⠀⢀⡇⠀⢇⢁⠀⠀⠈⢆⢰⠀⠀⠀⠈⡄⠈⢢⠀⠀⠀⠈⣇⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.MAGENTA}⠀⠀⢸⡀⠀⢰⠁⠀⢀⢮⠀⠇⡜⠀⠘⠀⠀⢰⠃⠀⠀⢸⠀⠀⠀⠀⠀⡇⠀⠀⡆⠀⠀⣘⣼⠤⠤⠤⣈⡞⡀⠀⠀⠀⡇⠰⡄⢣⡀⠀⠀⢻⠀⠀⠀{Style.RESET_ALL}", 
    f"{Fore.RED}⠀⠀⠈⡇⠀⡜⠀⢀⠎⢸⢸⢰⠁⠀⠄⠀⢠⠃⠀⠀⢸⠀⠀⠀⠀⠀⡇⠀⠀⡸⠀⠀⠀⣶⣿⡿⠿⡛⢻⡟⡇⠀⠀⠀⡇⠀⣿⣆⢡⠀⠀⢸⡇⠀⠀{Style.RESET_ALL}",  
    f"{Fore.YELLOW}⠀⠀⢠⡏⠀⠉⢢⡎⠀⡇⣿⠊⠀⠀⠀⢠⡏⠀⠀⠀⠎⠀⠀⠀⠀⠀⡇⠀⡸⠀⠀⠀⡇⠀⢰⡆⡇⢸⢠⢹⠀⠀⠀⡇⠀⢹⠈⢧⣣⠀⠘⡇⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.LIGHTYELLOW_EX}⠀⠀⢸⡇⠀⠀⠀⡇⠀⡇⢹⠀⠀⠀⢀⡾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢠⠃⠀⠀⠠⠟⡯⣻⣇⢃⠇⢠⠏⡇⠀⢸⡆⠀⢸⠀⠈⢳⡀⠀⡇⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.GREEN}⠀⠀⠀⣇⠀⡔⠋⡇⠀⢱⢼⠀⠀⡂⣼⡇⢹⣶⣶⣶⣤⣤⣀⠀⠀⠀⣇⠇⠀⠀⠀⠀⣶⡭⢃⣏⡘⠀⡎⠀⠇⠀⡾⣷⠀⣼⠀⠀⠀⢻⡄⡇⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.BLUE}⠀⠀⠀⣹⠜⠋⠉⠓⢄⡏⢸⠀⠀⢳⡏⢸⠹⢀⣉⢭⣻⡽⠿⠛⠓⠀⠋⠀⠀⠀⠀⠀⠘⠛⠛⠓⠀⡄⡇⠀⢸⢰⡇⢸⡄⡟⠀⠀⠀⠀⢳⡇⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.CYAN}⠀⣠⠞⠁⠀⠀⠀⠀⠀⢙⠌⡇⠀⣿⠁⠀⡇⡗⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠀⠀⠀⠀⠀⠀⠁⠁⠀⢸⣼⠀⠈⣇⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.MAGENTA}⢸⠁⠀⠀⢀⡠⠔⠚⠉⠉⢱⣇⢸⢧⠀⠀⠸⣱⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡤⠦⡔⠀⠀⠀⠀⠀⢀⡼⠀⠀⣼⡏⠀⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}", 
    f"{Fore.RED}⢸⠀⠀⠀⠋⠀⠀⠀⢀⡠⠤⣿⣾⣇⣧⠀⠀⢫⡆⠀⠀⠀⠀⠀⠀⠀⢨⠀⠀⣠⠇⠀⠀⢀⡠⣶⠋⠀⠀⡸⣾⠁⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.YELLOW}⢸⡄⠀⠀⠀⠀⠠⠊⠁⠀⠀⢸⢃⠘⡜⡵⡀⠈⢿⡱⢲⡤⠤⢀⣀⣀⡀⠉⠉⣀⡠⡴⠚⠉⣸⢸⠀⠀⢠⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.LIGHTYELLOW_EX}⠀⢧⠀⠀⠀⠀⠀⠀⠀⣀⠤⠚⠚⣤⣵⡰⡑⡄⠀⢣⡈⠳⡀⠀⠀⠀⢨⡋⠙⣆⢸⠀⠀⣰⢻⡎⠀⠀⡎⡇⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.GREEN}⠀⠈⢷⡀⠀⠀⠀⠀⠀⠁⠀⠀⠀⡸⢌⣳⣵⡈⢦⡀⠳⡀⠈⢦⡀⠀⠘⠏⠲⣌⠙⢒⠴⡧⣸⡇⠀⡸⢸⠇⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.BLUE}⠀⠀⢠⣿⠢⡀⠀⠀⠀⠠⠄⡖⠋⠀⠀⠙⢿⣳⡀⠑⢄⠹⣄⡀⠙⢄⡠⠤⠒⠚⡖⡇⠀⠘⣽⡇⢠⠃⢸⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.CYAN}⠀⠀⣾⠃⠀⠀⠀⠀⠀⢀⡼⣄⠀⠀⠀⠀⠀⠑⣽⣆⠀⠑⢝⡍⠒⠬⢧⣀⡠⠊⠀⠸⡀⠀⢹⡇⡎⠀⡿⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}", 
    f"{Fore.MAGENTA}⠀⡼⠁⠀⠀⠀⠀⠀⠀⢀⠻⣺⣧⠀⠀⠀⠰⢢⠈⢪⡷⡀⠀⠙⡄⠀⠀⠱⡄⠀⠀⠀⢧⠀⢸⡻⠀⢠⡇⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}",  
    f"{Fore.GREEN}⢰⠇⠀⠀⠀⠀⠀⠀⠀⢸⠀⡏⣿⠀⠀⠀⠀⢣⢇⠀⠑⣄⠀⠀⠸⡄⠀⠀⠘⡄⠀⠀⠸⡀⢸⠁⠀⡾⢰⡏⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}"  
]

cyan = Fore.CYAN      
magenta = Fore.MAGENTA  

BANNER = [
    f"{cyan}        _    _      _    {Style.RESET_ALL}",
    f"{cyan}       | |  (_)    | |   {Style.RESET_ALL}",
    f"{cyan}   __ _| | ___  ___| |_  {Style.RESET_ALL}",
    f"{cyan}  / _` | |/ / |/ _ \\ __| {Style.RESET_ALL}",
    f"{cyan} | (_| |   <| |  __/ |_  {Style.RESET_ALL}",
    f"{cyan}  \\__, |_|\\_\\_|\\___|\\__| {Style.RESET_ALL}",
    f"{cyan}   __/ |                 {Style.RESET_ALL}",
    f"{cyan}  |___/                  {Style.RESET_ALL}",
    f"{magenta}      #Bot Discord Version 3  {Style.RESET_ALL}"  
]

cyan = Fore.CYAN + Style.BRIGHT
magenta = Fore.MAGENTA + Style.BRIGHT
green = Fore.GREEN + Style.BRIGHT
yellow = Fore.YELLOW + Style.BRIGHT
red = Fore.RED + Style.BRIGHT
reset = Style.RESET_ALL

def log_info(message):
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"{cyan}╔════ INFO [{timestamp}] ════╗{reset}")
    print(f"{cyan}║ {message:<30} ║{reset}")
    print(f"{cyan}╚════════════════════════════╝{reset}")

def log_success(message):
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"{green}╔════ SUCCESS [{timestamp}] ════╗{reset}")
    print(f"{green}║ {message:<30} ║{reset}")
    print(f"{green}╚══════════════════════════════╝{reset}")

def log_error(message):
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"{red}╔════ ERROR [{timestamp}] ════╗{reset}")
    print(f"{red}║ {message:<30} ║{reset}")
    print(f"{red}╚═════════════════════════════╝{reset}")

def log_warning(message):
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"{yellow}╔════ WARNING [{timestamp}] ════╗{reset}")
    print(f"{yellow}║ {message:<30} ║{reset}")
    print(f"{yellow}╚═══════════════════════════════╝{reset}")

def kiểm_tra_key(user_key):
    payload = {"action": "verify", "key": user_key}
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        if response.status_code != 200:
            log_error(f"API trả về mã lỗi {response.status_code}")
            return False
        data = response.json()
        return data.get("status") == "success" and data.get("message") == "Key is valid"
    except Exception as e:
        log_error(f"Không thể kết nối tới API: {e}")
        return False

def kiểm_tra_api_key():
    log_info("Xin chào, tôi là Nguyễn Đăng Khoa")
    log_info("Chào mừng đến với Bot Discord v3 © Nguyễn Đăng Khoa")
    while True:
        user_key = input(f"{yellow}[INPUT] Vui lòng nhập key: {reset}").strip()
        if not user_key:
            log_error("Key không được để trống!")
            continue
        if kiểm_tra_key(user_key):
            log_success("Key hợp lệ! Bot đang khởi động...")
            for line in BANNER:
                print(f"{cyan}{line}{reset}")
            return user_key
        else:
            log_error("Key không hợp lệ hoặc đã bị thay đổi!")
            retry = input(f"{yellow}[INPUT] Thử lại? (y/n): {reset}").strip().lower()
            if retry != "y":
                log_error("Thoát bot do key không hợp lệ.")
                sys.exit(1)

def lấy_thông_tin_token(token, guild_id=None):
    headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=5)
        if response.status_code != 200:
            return {"error": f"Lỗi {response.status_code}"}
        user_data = response.json()
        user_id = user_data.get("id", "Không rõ")
        created_at = datetime.fromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        nick = user_data.get("username", "Không rõ")
        if guild_id:
            guild_response = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}", headers=headers, timeout=5)
            if guild_response.status_code == 200:
                member_data = guild_response.json()
                nick = member_data.get("nick") or member_data.get("user", {}).get("username", "Không rõ")
        return {
            "username": user_data.get("username", "Không rõ"),
            "user_id": user_id,
            "created_at": created_at,
            "nick": nick
        }
    except Exception as e:
        return {"error": str(e)}

def đổi_tên_hiển_thị(token, guild_id, new_nickname):
    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    payload = {"nick": new_nickname}
    try:
        response = requests.patch(f"https://discord.com/api/v9/guilds/{guild_id}/members/@me", headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            log_success(f"Đổi tên hiển thị trong server {guild_id} thành '{new_nickname}'")
            return f"✅ Đã đổi tên hiển thị thành '{new_nickname}'"
        else:
            log_error(f"Đổi tên hiển thị thất bại - Mã lỗi: {response.status_code}")
            return f"❌ Lỗi đổi tên hiển thị: {response.status_code}"
    except Exception as e:
        log_error(f"Đổi tên hiển thị thất bại: {e}")
        return f"❌ Lỗi: {str(e)}"

def in_thông_tin(info, label="Thông tin"):
    if "error" in info:
        return f"[Bot] Lỗi: {info['error']}"
    return (
        f"ℹ️ **{label}**:\n"
        f"  - Tên: {info['username']}\n"
        f"  - Tên hiển thị: {info['nick']}\n"
        f"  - ID: {info['user_id']}\n"
        f"  - Ngày tạo: {info['created_at']}"
    )

def tính_thời_gian_hoạt_động():
    uptime_seconds = int(time() - start_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}g {minutes}p {seconds}s"

def lưu_thông_tin_vào_file(token, user_id, prefix):
    with open("tt.txt", "w", encoding="utf-8") as file:
        file.write(f"USER_TOKEN={token}\n")
        file.write(f"ALLOWED_USER_ID={user_id}\n")
        file.write(f"PREFIX={prefix}\n")
    log_success("Đã lưu thông tin vào tt.txt")

def đọc_thông_tin_từ_file():
    if not os.path.exists("tt.txt"):
        return None
    try:
        with open("tt.txt", "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
            config = {}
            for line in lines:
                if "=" in line:
                    key, value = line.split("=", 1)
                    config[key] = value.strip()
            if "USER_TOKEN" in config and "ALLOWED_USER_ID" in config and "PREFIX" in config:
                return config
            return None
    except Exception as e:
        log_error(f"Không thể đọc file tt.txt: {e}")
        return None
def check_token_status(token):
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            log_success(f"Token {token[:10]}... hoạt động")
            return {
                "status": "active",
                "username": data.get("username", "Không rõ"),
                "user_id": data.get("id", "Không rõ"),
                "message": "Token đang hoạt động!"
            }
        elif response.status_code == 401:
            log_warning(f"Token {token[:10]}... không hợp lệ")
            return {
                "status": "inactive",
                "message": "Token không hợp lệ hoặc đã hết hạn!"
            }
        else:
            log_error(f"Token {token[:10]}... lỗi {response.status_code}")
            return {
                "status": "error",
                "message": f"Lỗi {response.status_code}: Không thể kiểm tra token!"
            }
    except Exception as e:
        log_error(f"Token {token[:10]}... lỗi kết nối: {str(e)}")
        return {
            "status": "error",
            "message": f"Lỗi kết nối: {str(e)}"
        }


def đổi_tên_hiển_thị_đa_token(tokens, guild_id, new_nickname):
    success_count = 0
    for token in tokens:
        result = đổi_tên_hiển_thị(token, guild_id, new_nickname)
        if "✅" in result:
            success_count += 1
        sleep(1)
    log_success(f"Đã đổi tên hiển thị cho {success_count}/{len(tokens)} token")
    return f"✅ Đã đổi tên hiển thị cho {success_count}/{len(tokens)} token"

def đọc_tokens_từ_file():
    try:
        with open("tokens.txt", "r", encoding="utf-8") as file:
            return [token.strip() for token in file.read().splitlines() if token.strip()]
    except Exception as e:
        log_error(f"Không đọc được tokens.txt: {e}")
        return []

def đọc_spam_từ_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception as e:
        log_error(f"Không đọc được file {filename}: {e}")
        return ""

def đọc_nhây_từ_file():
    try:
        with open("nhay.txt", "r", encoding="utf-8") as file:
            messages = [line.strip() for line in file.read().splitlines() if line.strip()]
            return messages if messages else ["HOANG GIA KIET BA DAO DISCORD 🧃🍃⛈️㊄㊄☔︎︎"]
    except Exception as e:
        log_error(f"Không đọc được nhay.txt: {e}")
        return ["NGUYỄN ĐĂNG KHOA BA DAO DISCORD 🧃🍃⛈️㊄㊄☔︎︎"]

def ghi_spam_vào_file(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content + "\n")
        log_success(f"Đã ghi nội dung vào {filename}")
        return True
    except Exception as e:
        log_error(f"Ghi file {filename} thất bại: {e}")
        return False

def tải_cài_đặt():
    global replied_users
    if os.path.exists("settings.json"):
        with open("settings.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            replied_users = set(int(uid) for uid in data.get("replied_users", []))  
    else:
        with open("settings.json", "w", encoding="utf-8") as file:
            json.dump({"replied_users": []}, file)
        replied_users = set()
def lưu_cài_đặt():
    with open("settings.json", "w", encoding="utf-8") as file:
        json.dump({"replied_users": list(replied_users)}, file)

def spam_message(channel, channel_id, tags=None):
    state = spam_states.get(channel_id, {})
    if state.get("n", False):
        try:
            messages = đọc_nhây_từ_file()
            if not messages:
                return
            index = 0
            while spam_states.get(channel_id, {}).get("n", False):  
                success = False
                while not success and spam_states.get(channel_id, {}).get("n", False):  
                    try:
                        content = messages[index % len(messages)]
                        if tags:
                            content += " " + " ".join(tags)
                        asyncio.run_coroutine_threadsafe(channel.send(content), client.loop).result()
                        success = True
                    except Exception:
                        sleep(10)  
                if success:
                    index += 1
                    sleep(1)
        except Exception:
            pass

def so_spam_message(channel, channel_id, tags=None):
    state = spam_states.get(channel_id, {})
    if state.get("s", False):
        try:
            with open("so.txt", "r", encoding="utf-8") as file:
                messages = [line.strip() for line in file.read().splitlines() if line.strip()]
            if not messages:
                return
            index = 0
            while spam_states.get(channel_id, {}).get("s", False):  
                success = False
                while not success and spam_states.get(channel_id, {}).get("s", False):  
                    try:
                        content = messages[index % len(messages)]
                        if tags:
                            content += " " + " ".join(tags)
                        asyncio.run_coroutine_threadsafe(channel.send(content), client.loop).result()
                        success = True
                    except Exception:
                        sleep(10)
                if success:
                    index += 1
                    sleep(1)
        except Exception:
            pass

def spam_webhook(webhook_url, channel_id):
    state = spam_states.get(channel_id, {})
    if state.get("spwh", False):
        try:
            spam_file = spam_files.get(channel_id)
            if not spam_file or not os.path.exists(spam_file):
                return
            content = đọc_spam_từ_file(spam_file)
            if not content:
                return
            while spam_states.get(channel_id, {}).get("spwh", False):  
                success = False
                while not success and spam_states.get(channel_id, {}).get("spwh", False):  
                    try:
                        response = requests.post(webhook_url, json={"content": content})
                        if response.status_code == 429:  
                            retry_after = response.json().get("retry_after", 10000) / 1000  
                            sleep(retry_after)
                            continue
                        response.raise_for_status()
                        success = True
                    except requests.exceptions.RequestException:
                        sleep(10)
                if success:
                    sleep(5)
        except Exception:
            pass

def spam_image(channel, channel_id, image_url):
    state = spam_states.get(channel_id, {})
    if state.get("fsm", False):
        try:
            while spam_states.get(channel_id, {}).get("fsm", False):  
                success = False
                while not success and spam_states.get(channel_id, {}).get("fsm", False):  
                    try:
                        asyncio.run_coroutine_threadsafe(channel.send(image_url), client.loop).result()
                        success = True
                    except Exception:
                        sleep(10)
                if success:
                    sleep(1.5)
        except Exception:
            pass

def spam_chui(channel, channel_id, image_url):
    state = spam_states.get(channel_id, {})
    if state.get("chui", False):
        try:
            messages = đọc_nhây_từ_file()
            if not messages:
                return
            index = 0
            while spam_states.get(channel_id, {}).get("chui", False):
                success = False
                while not success and spam_states.get(channel_id, {}).get("chui", False): 
                    try:
                        content = f"{messages[index % len(messages)]}\n{image_url}"
                        asyncio.run_coroutine_threadsafe(channel.send(content), client.loop).result()
                        success = True
                    except Exception:
                        sleep(10)
                if success:
                    index += 1
                    sleep(1.5)
        except Exception:
            pass
def spam_cfsm(channel, channel_id, user_tag, image_url):
    state = spam_states.get(channel_id, {})
    if state.get("cfsm", False):
        try:
            messages = đọc_nhây_từ_file()
            if not messages:
                return
            index = 0
            while spam_states.get(channel_id, {}).get("cfsm", False):  
                success = False
                while not success and spam_states.get(channel_id, {}).get("cfsm", False):  
                    try:
                        content = messages[index % len(messages)].strip()
                        message_content = f"> > {user_tag} [{content}]({image_url})"
                        asyncio.run_coroutine_threadsafe(channel.send(message_content), client.loop).result()
                        success = True
                    except Exception:
                        sleep(10)
                if success:
                    index += 1
                    sleep(1.5)
        except Exception:
            pass
def nhay_datoken_thread(token, channel_id, messages, start_index, total_tokens, tags=None):
    state = spam_states.get(channel_id, {})
    if state.get("ndt", False):
        headers = {"Authorization": token, "Content-Type": "application/json"}
        index = start_index
        while spam_states.get(channel_id, {}).get("ndt", False):  
            success = False
            while not success and spam_states.get(channel_id, {}).get("ndt", False):  
                try:
                    content = messages[index % len(messages)]
                    if tags:
                        content += " " + " ".join(tags)
                    response = requests.post(
                        f"https://discord.com/api/v9/channels/{channel_id}/messages",
                        headers=headers,
                        json={"content": content}
                    )
                    if response.status_code == 429:  
                        retry_after = response.json().get("retry_after", 10000) / 1000  
                        sleep(retry_after)
                        continue
                    response.raise_for_status()
                    success = True
                except requests.exceptions.RequestException:
                    sleep(10)
            if success:
                index += total_tokens
                sleep(1)
def nhay_datoken(channel, channel_id, tags=None):
    state = spam_states.get(channel_id, {})
    if state.get("ndt", False):
        try:
            tokens = đọc_tokens_từ_file()
            if not tokens:
                return
            messages = đọc_nhây_từ_file()
            if not messages:
                return
            spam_threads[channel_id]["ndt"] = []
            for i, token in enumerate(tokens):
                thread = threading.Thread(
                    target=nhay_datoken_thread,
                    args=(token, channel_id, messages, i, len(tokens), tags),
                    daemon=True
                )
                spam_threads[channel_id]["ndt"].append(thread)
                thread.start()
        except Exception:
            pass

def so_datoken_thread(token, channel_id, messages, start_index, total_tokens, tags=None):
    state = spam_states.get(channel_id, {})
    if state.get("sdt", False):
        headers = {"Authorization": token, "Content-Type": "application/json"}
        index = start_index
        while spam_states.get(channel_id, {}).get("sdt", False):  
            success = False
            while not success and spam_states.get(channel_id, {}).get("sdt", False):  
                try:
                    content = messages[index % len(messages)]
                    if tags:
                        content += " " + " ".join(tags)
                    response = requests.post(
                        f"https://discord.com/api/v9/channels/{channel_id}/messages",
                        headers=headers,
                        json={"content": content}
                    )
                    if response.status_code == 429:  
                        retry_after = response.json().get("retry_after", 10000) / 1000  
                        sleep(retry_after)
                        continue
                    response.raise_for_status()
                    success = True
                except requests.exceptions.RequestException:
                    sleep(10)
            if success:
                index += total_tokens
                sleep(1)
def so_datoken(channel, channel_id, tags=None):
    state = spam_states.get(channel_id, {})
    if state.get("sdt", False):
        try:
            tokens = đọc_tokens_từ_file()
            if not tokens:
                return
            with open("so.txt", "r", encoding="utf-8") as file:
                messages = [line.strip() for line in file.read().splitlines() if line.strip()]
            if not messages:
                return
            spam_threads[channel_id]["sdt"] = []
            for i, token in enumerate(tokens):
                thread = threading.Thread(
                    target=so_datoken_thread,
                    args=(token, channel_id, messages, i, len(tokens), tags),
                    daemon=True
                )
                spam_threads[channel_id]["sdt"].append(thread)
                thread.start()
        except Exception:
            pass
def spam_datoken(channel, channel_id):
    state = spam_states.get(channel_id, {})
    if state.get("spdt", False):
        try:
            tokens = đọc_tokens_từ_file()
            if not tokens:
                return
            spam_datoken_file = spam_datoken_files.get(channel_id)
            if not spam_datoken_file or not os.path.exists(spam_datoken_file):
                return
            content = đọc_spam_từ_file(spam_datoken_file)
            if not content:
                return
            async def spam_forever():
                while spam_states.get(channel_id, {}).get("spdt", False):  
                    for token in tokens:
                        headers = {"Authorization": token, "Content-Type": "application/json"}
                        success = False
                        while not success and spam_states.get(channel_id, {}).get("spdt", False):  
                            try:
                                response = requests.post(
                                    f"https://discord.com/api/v9/channels/{channel_id}/messages",
                                    headers=headers,
                                    json={"content": content}
                                )
                                if response.status_code == 429:  
                                    retry_after = response.json().get("retry_after", 10000) / 1000  
                                    await asyncio.sleep(retry_after)
                                    continue
                                response.raise_for_status()
                                success = True
                            except requests.exceptions.RequestException:
                                await asyncio.sleep(10)
                        if success:
                            await asyncio.sleep(0.3)
                    await asyncio.sleep(5)
            client.loop.create_task(spam_forever())
        except Exception:
            pass
def webhook_datoken(webhook_url, channel_id):
    state = spam_states.get(channel_id, {})
    if state.get("whdt", False):
        try:
            tokens = đọc_tokens_từ_file()
            if not tokens:
                return
            spam_datoken_file = spam_datoken_files.get(channel_id)
            if not spam_datoken_file or not os.path.exists(spam_datoken_file):
                return
            content = đọc_spam_từ_file(spam_datoken_file)
            if not content:
                return
            async def webhook_forever():
                while spam_states.get(channel_id, {}).get("whdt", False):  
                    for token in tokens:
                        success = False
                        while not success and spam_states.get(channel_id, {}).get("whdt", False):  
                            try:
                                response = requests.post(
                                    webhook_url,
                                    json={"content": f"{content} (Token: {token[:10]}...)"}
                                )
                                if response.status_code == 429:  
                                    retry_after = response.json().get("retry_after", 10000) / 1000  
                                    await asyncio.sleep(retry_after)
                                    continue
                                response.raise_for_status()
                                success = True
                            except requests.exceptions.RequestException:
                                await asyncio.sleep(10)
                        if success:
                            await asyncio.sleep(0.3)
                    await asyncio.sleep(5)
            client.loop.create_task(webhook_forever())
        except Exception:
            pass

async def voice_loop(channel, delay_leave=1, delay_join=1):
    if not channel:
        return "❌ Không tìm thấy kênh voice!"
    
    try:
        while not asyncio.current_task().cancelled():  
            vc = await channel.connect()
            log_success(f"Đã tham gia {channel.name} (ID: {channel.id})")
            await asyncio.sleep(delay_leave)
            await vc.disconnect()
            log_info(f"Đã rời {channel.name}")
            await asyncio.sleep(delay_join)
            
    except discord.Forbidden:
        log_error(f"Không có quyền tham gia kênh {channel.name}")
        return "❌ Bot không có quyền tham gia kênh voice!"
    except discord.errors.ClientException:
        log_warning(f"Bot đã ở kênh khác, thử rời và vào lại {channel.name}")
        if client.voice_clients:
            for vc in client.voice_clients:
                await vc.disconnect()
        await asyncio.sleep(1)
    except asyncio.CancelledError:
        if client.voice_clients:
            for vc in client.voice_clients:
                if vc.channel.id == channel.id:
                    await vc.disconnect()
                    log_info(f"Đã ngắt kết nối khỏi {channel.name} do dừng lệnh")
                    break
        raise  
    except Exception as e:
        log_error(f"Lỗi trong voice loop {channel.name}: {e}")
        await asyncio.sleep(1)  
async def raid_server(guild_id, new_server_name):
    guild = client.get_guild(int(guild_id))
    if not guild:
        return "❌ Không tìm thấy server hoặc bot không có quyền truy cập!"
    avatar_urls = [
        "https://files.catbox.moe/b9zt7z.jpeg",
        "https://i.imgur.com/n6mR8lX.jpeg",
        "https://i.imgur.com/bkOXhW7.jpeg",
        "https://i.imgur.com/EMPrZA2.jpeg",
        "https://i.imgur.com/OMgkD7J.jpeg",
        "https://i.imgur.com/ju3Gtet.jpeg",
        "https://i.imgur.com/RYxcu4G.jpeg",
        "https://i.imgur.com/NARYR6T.jpeg",
        "https://i.imgur.com/YV1ayky.jpeg",
        "https://i.imgur.com/oc2ISMB.jpeg",
        "https://i.imgur.com/zBrG0H7.jpeg",
        "https://i.imgur.com/Ty0vbmR.jpeg",
        "https://i.imgur.com/zfppgot.jpeg",
        "https://i.imgur.com/aDN8Raz.jpeg"
    ]
    avatar_data_list = []
    async with aiohttp.ClientSession() as session:
        for url in avatar_urls:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        if len(data) > 0:
                            avatar_data_list.append(data)
                            log_success(f"Đã tải trước ảnh từ {url}")
                        else:
                            log_warning(f"Dữ liệu ảnh trống từ {url}")
                    elif resp.status == 429:
                        log_warning(f"Rate limit (429) khi tải {url}, bỏ qua")
                        await asyncio.sleep(5)  
                    else:
                        log_warning(f"Không tải được ảnh từ {url}: {resp.status}")
            except Exception as e:
                log_error(f"Lỗi khi tải trước ảnh từ {url}: {e}")
            await asyncio.sleep(1) 

    if not avatar_data_list:
        log_warning("Không tải được ảnh nào, sử dụng webhook/server không avatar")
    try:
        await guild.edit(name=new_server_name)
        log_success(f"Đã đổi tên server thành '{new_server_name}'")
    except discord.Forbidden:
        log_error("Không có quyền đổi tên server!")
    except Exception as e:
        log_error(f"Lỗi khi đổi tên server: {e}")
    try:
        if avatar_data_list:
            await guild.edit(icon=random.choice(avatar_data_list))
            log_success("Đã thay đổi avatar server từ danh sách đã tải trước")
        else:
            log_warning("Không có ảnh để đổi avatar server")
    except discord.Forbidden:
        log_error("Không có quyền thay đổi avatar server!")
    except Exception as e:
        log_error(f"Lỗi khi thay đổi avatar server: {e}")
    try:
        for channel in guild.channels:
            await channel.delete()
            log_success(f"Đã xóa kênh {channel.name}")
            await asyncio.sleep(0.01)
    except discord.Forbidden:
        log_error("Không có quyền xóa kênh!")
    except Exception as e:
        log_error(f"Lỗi khi xóa kênh: {e}")
    try:
        for role in guild.roles[1:]: 
            await role.delete()
            log_success(f"Đã xóa role {role.name}")
            await asyncio.sleep(0.2)
    except discord.Forbidden:
        log_error("Không có quyền xóa role!")
    except Exception as e:
        log_error(f"Lỗi khi xóa role: {e}")
    font_styles = [
        "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓐̂𝓐̆𝓔̂𝓞̂𝓞̛𝓤̛𝓓",
        "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐀̂𝐀̆𝐄̂𝐎̂𝐎̛𝐔̛𝐃",
        "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝑨̂𝑨̆𝑬̂𝑶̂𝑶̛𝑼̛𝑫",
        "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗔̂𝗔̆𝗘̂𝗢̂𝗢̛𝗨̛𝗗",
        "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝙰̂𝙰̆𝙴̂𝙾̂𝙾̛𝚄̛𝙳",
        "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝕬̂𝕬̆𝕰̂𝕺̂𝕺̛𝖀̛𝕯",
        "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺＡ̂Ａ̆Ｅ̂Ｏ̂Ｏ̛Ｕ̛Ｄ",
        "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀ̂ᴀ̆ᴇ̂ᴏ̂ᴏ̛ᴜ̛ᴅ",
        "A̷B̷C̷D̷E̷F̷G̷H̷I̷J̷K̷L̷M̷N̷O̷P̷Q̷R̷S̷T̷U̷V̷W̷X̷Y̷Z̷Â̷Ă̷Ê̷Ô̷Ơ̷Ư̷D̷",
        "𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒜̂𝒜̆ℰ̂𝒪̂𝒪̛𝒰̛𝒟",
        "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘈̂𝘈̆𝘌̂𝘖̂𝘖̛𝘜̛𝘋",
        "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝙰̂𝙰̆𝙴̂𝙾̂𝙾̛𝚄̛𝙳",
        "𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍𝐴̂𝐴̆𝐸̂𝑂̂𝑂̛𝑈̛𝐷",
        "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝑨̂𝑨̆𝑬̂𝑶̂𝑶̛𝑼̛𝑫",
        "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝒂̂𝒂̆𝒆̂𝒐̂𝒐̛𝒖̛𝒅",
        "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝔸̂𝔸̆𝔼̂𝕆̂𝕆̛𝕌̛𝔻",
        "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺＡ̂Ａ̆Ｅ̂Ｏ̂Ｏ̛Ｕ̛Ｄ",
        "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⒶ̂Ⓐ̆Ⓔ̂Ⓞ̂Ⓞ̛Ⓤ̛Ⓓ",
        "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺＡ̂Ａ̆Ｅ̂Ｏ̂Ｏ̛Ｕ̛Ｄ",
        "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🅰̂🅰̆🅴̂🅾̂🅾̛🆄̛🅳"
    ]


    icons = [
        "🔥", "💥", "⚡", "☠️", "💀", "🖤", "👾", "🎃", "🌩️", "🕸️",
        "🗡️", "🔪", "🩸", "💣", "🛡️", "⚔️", "🌋", "☣️", "☢️", "🦇",
        "👹", "👻", "🧟", "🕷️", "🦂", "🌪️", "🧨", "💤", "🍷", "🍾",
        "🎭", "🎮", "📛", "🔱", "🎲", "🎯", "🧩", "🎸", "🎬", "🔮",
        "🌟", "💫", "✨", "⭐", "🌙", "☀️", "🌈", "❄️", "🌊", "🍕",
        "🍔", "🍟", "🍉", "🍓", "🍒", "🍰", "🎁", "🎀", "🎉", "🎊"
    ]

    raid_links = [
        "https://guns.lol/nkhoa"
    ]


    def apply_font(name):
        font_map_base = {
            "A": "A", "B": "B", "C": "C", "D": "D", "E": "E", "F": "F", "G": "G", "H": "H",
            "I": "I", "J": "J", "K": "K", "L": "L", "M": "M", "N": "N", "O": "O", "P": "P",
            "Q": "Q", "R": "R", "S": "S", "T": "T", "U": "U", "V": "V", "W": "W", "X": "X",
            "Y": "Y", "Z": "Z", "Â": "Â", "Ă": "Ă", "Ê": "Ê", "Ô": "Ô", "Ơ": "Ơ", "Ư": "Ư", "Đ": "Đ"
        }
        words = name.upper().split()
        styled_name = ""
        
        for word in words:
            font_template = random.choice(font_styles)
            font_map = {
                "A": font_template[0], "B": font_template[1], "C": font_template[2], "D": font_template[3],
                "E": font_template[4], "F": font_template[5], "G": font_template[6], "H": font_template[7],
                "I": font_template[8], "J": font_template[9], "K": font_template[10], "L": font_template[11],
                "M": font_template[12], "N": font_template[13], "O": font_template[14], "P": font_template[15],
                "Q": font_template[16], "R": font_template[17], "S": font_template[18], "T": font_template[19],
                "U": font_template[20], "V": font_template[21], "W": font_template[22], "X": font_template[23],
                "Y": font_template[24], "Z": font_template[25], "Â": font_template[26], "Ă": font_template[27],
                "Ê": font_template[28], "Ô": font_template[29], "Ơ": font_template[30], "Ư": font_template[31],
                "Đ": font_template[32]
            }
            styled_word = ""
            for char in word:
                styled_word += font_map.get(char, char)
            styled_name += styled_word + " "
        
        return styled_name.strip()
    async def spam_webhook(channel):
        try:
            if avatar_data_list:
                webhook = await channel.create_webhook(
                    name=f"Raid-Đăng Khoa-{new_server_name}",
                    avatar=random.choice(avatar_data_list)
                )
                log_success(f"Đã tạo webhook trong kênh {channel.name} với avatar từ danh sách đã tải trước")
            else:
                webhook = await channel.create_webhook(name=f"Raid-Webhook-{new_server_name}")
                log_warning(f"Không có ảnh, tạo webhook không avatar trong kênh {channel.name}")
            for _ in range(100):
                random_link = random.choice(raid_links)
                await webhook.send(f"@everyone @here 💥 SERVER ĐÃ BỊ PHÁ HOẠI BỞI NGUYỄN ĐĂNG KHOA - {new_server_name} 💥 {random_link}")
                await asyncio.sleep(1.5) 
        except discord.Forbidden:
            log_error(f"Không có quyền tạo hoặc spam webhook trong kênh {channel.name}")
        except Exception as e:
            log_error(f"Lỗi khi spam webhook trong kênh {channel.name}: {e}")
    created_text_channels = []
    for _ in range(200):
        styled_name = apply_font(new_server_name)
        random_icons = "".join(random.choice(icons) for _ in range(5))
        channel_name = f"{styled_name}{random_icons}"
        try:
            new_channel = await guild.create_text_channel(channel_name)
            log_success(f"Đã tạo kênh chat {channel_name}")
            created_text_channels.append(new_channel)
            asyncio.create_task(spam_webhook(new_channel))  
            await asyncio.sleep(0.5) 
        except discord.Forbidden:
            log_error("Không có quyền tạo kênh chat!")
        except Exception as e:
            log_error(f"Lỗi khi tạo kênh chat {channel_name}: {e}")
    for _ in range(50):
        styled_name = apply_font(new_server_name)
        random_icons = "".join(random.choice(icons) for _ in range(5))
        channel_name = f"{styled_name}{random_icons}"
        try:
            await guild.create_voice_channel(channel_name)
            log_success(f"Đã tạo kênh voice {channel_name}")
            await asyncio.sleep(0.2)
        except discord.Forbidden:
            log_error("Không có quyền tạo kênh voice!")
        except Exception as e:
            log_error(f"Lỗi khi tạo kênh voice {channel_name}: {e}")
    try:
        await guild.edit(
            region="japan",
            default_notifications=discord.NotificationLevel.all_messages
        )
        log_success("Đã thay đổi cài đặt server!")
    except discord.Forbidden:
        log_error("Không có quyền thay đổi cài đặt server!")
    except Exception as e:
        log_error(f"Lỗi khi thay đổi cài đặt server: {e}")

    return (
        f"✅ Đã raid server {guild_id}: \n"
        f"- Đổi tên thành '{new_server_name}'\n"
        f"- Đổi avatar server ngẫu nhiên từ danh sách đã tải trước\n"
        f"- Xóa toàn bộ kênh và role\n"
        f"- Tạo 200 kênh chat (spam ngay sau khi tạo) + 50 kênh voice với font ngẫu nhiên mỗi từ và 5 icon\n"
        f"- Spam 100 lần qua webhook riêng mỗi kênh chat với avatar ngẫu nhiên, @everyone @here và link random\n"
        f"- Thay đổi vùng và cài đặt thông báo"
    )
def check_token_status(token):
    headers = {"Authorization": token}
    try:
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=5)
        if response.status_code == 200:
            return {"status": "active", "message": "Token hợp lệ"}
        return {"status": "invalid", "message": f"Mã lỗi: {response.status_code}"}
    except Exception as e:
        return {"status": "invalid", "message": str(e)}
async def tải_ảnh(url, temp_file="temp_avatar.jpg"):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    log_error(f"Không thể tải ảnh từ URL: {resp.status}")
                    return None, f"❌ Không thể tải ảnh từ URL: {resp.status}"
                image_data = await resp.read()
                if len(image_data) > 10 * 1024 * 1024:
                    log_error("Ảnh quá lớn (>10MB)")
                    return None, "❌ Ảnh quá lớn! Giới hạn là 10MB."
                with open(temp_file, "wb") as f:
                    f.write(image_data)
                log_info(f"Đã lưu ảnh vào {temp_file}")
                return image_data, "✅ Ảnh đã được tải thành công"
    except Exception as e:
        log_error(f"Lỗi khi tải ảnh: {e}")
        return None, f"❌ Lỗi tải ảnh: {str(e)}"
async def đổi_avatar_single(client, image_data):
    try:
        await client.user.edit(avatar=image_data)
        log_success(f"Đã đổi avatar cho bot hiện tại")
        return "✅ Đã thay đổi avatar thành công!"
    except discord.HTTPException as e:
        log_error(f"Lỗi HTTP khi đổi avatar: {e}")
        return f"❌ Lỗi HTTP: {str(e)}"
    except Exception as e:
        log_error(f"Lỗi khi đổi avatar: {e}")
        return f"❌ Lỗi: {str(e)}"
async def đổi_avatar_token(token, image_data):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    try:
        token_status = check_token_status(token)
        if token_status["status"] != "active":
            log_error(f"Token {token[:10]}... không hợp lệ: {token_status['message']}")
            return f"❌ Token không hợp lệ: {token_status['message']}"
        
        payload = {"avatar": f"data:image/jpeg;base64,{base64.b64encode(image_data).decode('utf-8')}"}
        response = requests.patch("https://discord.com/api/v9/users/@me", headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            log_success(f"Đã đổi avatar cho token {token[:10]}...")
            return "✅ Đã thay đổi avatar thành công!"
        elif response.status_code == 429:
            log_warning(f"Rate limit cho token {token[:10]}...")
            return "❌ Rate limit, thử lại sau!"
        else:
            log_error(f"Lỗi API cho token {token[:10]}...: {response.status_code} - {response.text}")
            return f"❌ Lỗi API: {response.status_code}"
    except Exception as e:
        log_error(f"Lỗi khi đổi avatar cho token {token[:10]}...: {e}")
        return f"❌ Lỗi: {str(e)}"
async def đổi_avatar_đa_token(tokens, image_url, client):
    temp_file = "temp_avatar.jpg"
    image_data, tải_result = await tải_ảnh(image_url, temp_file)
    if not image_data:
        return 0, len(tokens), [tải_result]
    
    success_count = 0
    total_tokens = len(tokens)
    results = []
    
    for token in tokens:
        if token == client.user.token: 
            result = await đổi_avatar_single(client, image_data)
        else:
            result = await đổi_avatar_token(token, image_data)
        results.append(f"Token {token[:10]}...: {result}")
        if "✅" in result:
            success_count += 1
        await asyncio.sleep(5)  
    
    if os.path.exists(temp_file):
        os.remove(temp_file)
        log_info(f"Đã xóa file tạm {temp_file}")
    
    log_success(f"Đã đổi avatar cho {success_count}/{total_tokens} token")
    return success_count, total_tokens, results


async def lấy_kênh_văn_bản(message):
    if isinstance(message.channel, discord.DMChannel):
        return message.channel
    elif isinstance(message.channel, discord.TextChannel):
        return message.channel
    guild = message.guild
    if guild:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                return channel
    log_error("Không tìm thấy kênh văn bản")
    return None

def thiết_lập():
    global USER_TOKEN, ALLOWED_USER_ID, PREFIX
    old_config = đọc_thông_tin_từ_file()
    if old_config:
        log_info("Tìm thấy thông tin cũ trong tt.txt")
        choice = input(f"{yellow}[INPUT] Dùng thông tin cũ? (y/n): {reset}").strip().lower()
        if choice == "y":
            USER_TOKEN = old_config["USER_TOKEN"]
            ALLOWED_USER_ID = int(old_config["ALLOWED_USER_ID"])
            PREFIX = old_config["PREFIX"]
            return USER_TOKEN
    
    user_token = input(f"{yellow}[INPUT] Nhập Token: {reset}").strip()
    if not user_token:
        log_error("Token trống")
        sys.exit(1)
    token_info = lấy_thông_tin_token(user_token)
    if "error" in token_info:
        log_error(f"Token không hợp lệ: {token_info['error']}")
        sys.exit(1)
    
    allowed_user_id = input(f"{yellow}[INPUT] Nhập User ID: {reset}").strip()
    if not allowed_user_id.isdigit():
        log_error("ID không hợp lệ")
        sys.exit(1)
    
    prefix = input(f"{yellow}[INPUT] Nhập Prefix (mặc định !): {reset}").strip() or "!"
    USER_TOKEN = user_token
    ALLOWED_USER_ID = int(allowed_user_id)
    PREFIX = prefix
    lưu_thông_tin_vào_file(user_token, allowed_user_id, prefix)
    return user_token

@client.event
async def on_ready():
    tải_cài_đặt()
    log_success(f"Được chạy bởi Hoàng Gia Kiệt - Đã đăng nhập với {client.user}")
    async def keep_alive():
        while True:
            await asyncio.sleep(300)
            if not client.is_closed():
                log_info("Bot vẫn hoạt động...")
    client.loop.create_task(keep_alive())

async def tạo_webhook(channel):
    try:
        webhook = await channel.create_webhook(name="Bot Webhook by Nguyễn Đăng Khoa")
        log_success(f"Đã tạo webhook trong kênh {channel.name} (ID: {channel.id})")
        return webhook.url
    except discord.Forbidden:
        log_error("Không có quyền tạo webhook!")
        return None
    except Exception as e:
        log_error(f"Lỗi khi tạo webhook: {e}")
        return None

async def tạo_nhiều_webhook(channel, amount):
    webhook_urls = []
    try:
        for i in range(min(amount, 10)):  
            webhook = await channel.create_webhook(name=f"Bot Webhook {i+1} by Hoang Gia Kiet")
            webhook_urls.append(webhook.url)
            log_success(f"Đã tạo webhook {i+1}/{amount} trong kênh {channel.name} (ID: {channel.id})")
            await asyncio.sleep(0.5)  
        return webhook_urls
    except discord.Forbidden:
        log_error("Không có quyền tạo webhook!")
        return None
    except discord.HTTPException as e:
        log_error(f"Lỗi HTTP khi tạo webhook: {e}")
        return webhook_urls if webhook_urls else None  
    except Exception as e:
        log_error(f"Lỗi khác khi tạo webhook: {e}")
        return None
    
@client.event
async def on_message(message):
    global PREFIX, spam_states, spam_threads, spam_files, spam_datoken_files, REPLY_ACTIVE, replied_users
    if message.guild and REPLY_ACTIVE and message.author.id != client.user.id:
        if client.user in message.mentions or "@here" in message.content or "@everyone" in message.content:
            nhay_messages = đọc_nhây_từ_file()
            reply_content = f"{random.choice(nhay_messages)} <@{message.author.id}>"
            await message.reply(reply_content)
            return
    if message.author.id != ALLOWED_USER_ID or not message.content.startswith(PREFIX):
        if message.guild and message.author.id in replied_users and message.author.id != client.user.id:
            nhay_messages = đọc_nhây_từ_file()
            reply_content = f"{random.choice(nhay_messages)} <@{message.author.id}>"
            await message.reply(reply_content)
            return
        return
    if message.author.id != ALLOWED_USER_ID or not message.content.startswith(PREFIX):
        return
    
    command = message.content[len(PREFIX):].strip().split()
    if not command:
        return
    
    cmd = command[0].lower()
    args = command[1:]
    text_channel = await lấy_kênh_văn_bản(message)
    if not text_channel:
        return
    channel_id = str(text_channel.id)
    
    if channel_id not in spam_states:
        spam_states[channel_id] = {"n": False, "s": False, "sp": False, "spwh": False, "ndt": False, "sdt": False, "spdt": False, "whdt": False, "fsm": False, "chui": False, "cfsm": False, "masswhspam": False}
    if channel_id not in spam_threads:
        spam_threads[channel_id] = {"n": None, "s": None, "sp": None, "spwh": None, "ndt": [], "sdt": [], "spdt": None, "whdt": None, "fsm": None, "chui": None, "cfsm": None, "masswhspam": None}
    client.loop.create_task(xóa_tin_nhắn_sau_khoảng_thời_gian(message, 1))

    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%d/%m/%Y")

    if cmd == "menu":
        token_info = lấy_thông_tin_token(USER_TOKEN, message.guild.id if message.guild else None)
        username = token_info.get("username", "Không rõ")
        display_name = message.guild.me.display_name if message.guild and message.guild.me else client.user.name
        user_id = token_info.get("user_id", "Không rõ")
        
        if message.guild:  
            menu_msg = await text_channel.send(
                "```css\n"
                f"    🌟 [ 𝑩𝒐𝒕 𝑫𝒊𝒔𝒄𝒐𝒓𝒅 𝑽𝒆𝒓𝒔𝒊𝒐𝒏 𝟑 ] 🌟\n"
                f"════════════════════════════════════\n"
                f"📌 𝑨𝒄𝒄𝒐𝒖𝒏𝒕 𝑷𝒓𝒐𝒇𝒊𝒍𝒆: {username} 📌\n"
                f"⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻\n"
                f"🎭 Tên hiển thị: {display_name}\n"
                f"🆔 ID: {user_id}\n"
                f"⏰ Uptime: {tính_thời_gian_hoạt_động()}\n"
                f"🔧 Prefix: `{PREFIX}`\n"
                f"════════════════════════════════════\n"
                f"         💬 𝑳𝒆̣̂𝒏𝒉 𝑫𝒊𝒔𝒄𝒐𝒓𝒅 💬\n" 
                f"⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻\n"
                f"📢 {PREFIX}n [@tag] » Nhây\n"
                f"🎶 {PREFIX}s [@tag] » Thả sớ\n"
                f"📜 {PREFIX}sp » Treo ngôn\n"
                f"🚀 {PREFIX}ndt [@tag] » Nhây đa token\n"
                f"🚀 {PREFIX}sdt [@tag] » Sớ đa token\n"
                f"🚀 {PREFIX}spdt » Treo ngôn đa token\n"
                f"🌐 {PREFIX}spwh <url> » Treo webhook\n"
                f"🌐 {PREFIX}whdt <url> » Treo Webhook đa token\n"
                f"🖼️ {PREFIX}fsm <link> » Spam ảnh\n"
                f"💭 {PREFIX}cfsm <@tag> <link> » Nhây kèm ảnh\n"
                f"🔄 {PREFIX}rl » Auto reply khi bị ccho rách nào tag\n"
                f"📩 {PREFIX}rep <@tag> » Auto reply user\n"
                f"📪 {PREFIX}urep <@tag> » Hủy auto reply\n"
                f"✍️ {PREFIX}c <nội dung> <lần> <trễ> » Spam gì kmm\n"
                f"⛔ {PREFIX}st <lệnh> » Dừng lệnh\n"
                f"════════════════════════════════════\n"
                f"          🎙️ 𝑳𝒆̣̂𝒏𝒉 𝑽𝒐𝒊𝒄𝒆 🎙️\n"
                f"⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻\n"
                f"🎤 {PREFIX}vc <kênh> » Treo voice token chính\n"
                f"🎛️ {PREFIX}vcdt <kênh> » Treo voice đa token\n"
                f"════════════════════════════════════\n"
                f"         🎮 𝑳𝒆̣̂𝒏𝒉 𝑮𝒊𝒂̉𝒊 𝑻𝒓𝒊́ 🎮\n"
                f"⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻\n"
                f"💌 {PREFIX}thinh » Thả thính\n"
                f"📖 {PREFIX}cadao » Ca dao\n"
                f"👊 {PREFIX}đấm » Đấm mẹ ruột\n"
                f"💋 {PREFIX}kiss » Hôn\n"
                f"❤️ {PREFIX}love » I love you :)\n"
                f"🖌️ {PREFIX}tti <văn bản> » Văn bản thành ảnh\n"
                f"❓ {PREFIX}hoingu » Hỏi ngu\n"
                f"🔗 {PREFIX}noitu <từ> » Trò chơi nối từ\n"
                f"🔮 {PREFIX}tarot » Bói Tarot\n"
                f"🦠 {PREFIX}covid <quốc gia> » Thống kê COVID-19\n"
                f"🔍 {PREFIX}sr » Tìm kiếm (pin, tt, cap, spot, scl, dl)\n"
                f"📧 {PREFIX}getemail » Lấy email tạm\n"
                f"📬 {PREFIX}showemail <email> » Xem email tạm\n"
                f"════════════════════════════════════\n"
                f"          ⚙️ 𝑳𝒆̣̂𝒏𝒉 𝑺𝒆𝒕𝒖𝒑 ⚙️\n"
                f"⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻\n"
                f"📝 {PREFIX}rn <id> <tên> » Đổi tên trong server\n"
                f"📝 {PREFIX}rndt <id> <tên> » Đổi tên đa token\n"
                f"🗑️ {PREFIX}rsn <id> » Xóa tên trong server\n"
                f"📎 {PREFIX}sf <file> » Chọn file spam\n"
                f"📎 {PREFIX}sfdt <file> » Chọn file đa token\n"
                f"✍️ {PREFIX}es <file> <nội dung> » Sửa file\n"
                f"📄 {PREFIX}ns <file> <nội dung> » Tạo file mới\n"
                f"🔑 {PREFIX}checktoken » Kiểm tra token\n"
                f"🌐 {PREFIX}taowh » Tạo webhook\n"
                f"🌐 {PREFIX}taowhsll <số> » Tạo nhiều webhook\n"
                f"════════════════════════════════════\n" 
                f"        📝 𝑳𝒆̣̂𝒏𝒉 𝑯𝒆̣̂ 𝑻𝒉𝒐̂́𝒏𝒈 📝\n"
                f"⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻\n"
                f"📩 {PREFIX}dmall <nội dung> <số lần> » Gửi DM all\n"
                f"💣 {PREFIX}raid <id> <tên> » Raid server\n"
                f"📋 {PREFIX}sv » Danh sách server\n"
                f"📋 {PREFIX}idkenh <id> » Danh sách kênh\n"
                f"📊 {PREFIX}checktt <id> » Check tương tác\n"
                f"📈 {PREFIX}checksv <id> » Check server\n"
                f"🆔 {PREFIX}id [@tag] » Lấy ID người dùng\n"
                f"ℹ️ {PREFIX}i » Thông tin bot\n"
                f"🔧 {PREFIX}spf <prefix> » Đổi prefix\n"
                f"📡 {PREFIX}ping » Kiểm tra độ trễ\n"
                f"🗑️ {PREFIX}cl <số> » Xóa tin nhắn\n"
                f"🚪 {PREFIX}ex » Thoát bot\n"
                f"❓ {PREFIX}help <lệnh> » Hướng dẫn chi tiết\n" 
                f"════════════════════════════════════\n"
                f"⏰ 𝑪𝒖𝒓𝒓𝒆𝒏𝒕 𝑻𝒊𝒎𝒆: {current_time}\n"
                f"📅 𝑪𝒖𝒓𝒓𝒆𝒏𝒕 𝑫𝒂𝒕𝒆: {current_date}\n"
                f"👤 𝑨𝒖𝒕𝒉𝒐𝒓: Nguyễn Đăng Khoa\n"
                f"🎱 𝑨𝒅𝒎𝒊𝒏𝑩𝒐𝒕: Nguyễn Đăng Khoa\n"
                f"🏝️ 𝑽𝒆𝒓𝒔𝒊𝒐𝒏: 𝟑"
                "```"
            )            
        else: 
            menu_msg = await text_channel.send(
                "```markdown\n"
                "🌟 Bot Discord V3 - DM Mode 🌟\n"
                "═══════════════════════════════════════\n"
                "📌 Thông Tin\n"
                "───────────────────────────────────────\n"
                f"👑 Tác giả: Nguyễn Đăng Khoa\n"
                f"👤 Username: {username}\n"
                f"🎭 Tên hiển thị: {display_name}\n"
                f"🆔 ID: {user_id}\n"
                f"⏰ Thời gian hoạt động: {tính_thời_gian_hoạt_động()}\n"
                f"🔧 Prefix: {PREFIX}\n"
                "═══════════════════════════════════════\n"
                "💬 Lệnh Discord (DM)\n"
                "───────────────────────────────────────\n"
                f"📢 {PREFIX}n - Spam nhây từ nhay.txt\n"
                f"🎶 {PREFIX}s - Thả sớ từ so.txt\n"
                f"📜 {PREFIX}sp - Spam file đã chọn\n"
                f"🚀 {PREFIX}ndt - Nhây đa token\n"
                f"🚀 {PREFIX}sdt - Sớ đa token\n"
                f"🚀 {PREFIX}spdt - Spam file đa token\n"
                f"🌐 {PREFIX}spwh <url> - Spam qua webhook\n"
                f"🌐 {PREFIX}whdt <url> - Webhook đa token\n"
                f"🖼️ {PREFIX}fsm <link> - Spam ảnh\n"
                f"📝 {PREFIX}c <nội dung> <lần> <trễ> - Spam tùy chỉnh\n"
                f"⛔ {PREFIX}st <lệnh> - Dừng lệnh đang chạy\n"
                "═══════════════════════════════════════\n"
                "🎮 Lệnh Giải Trí\n"
                "───────────────────────────────────────\n"
                f"💌 {PREFIX}thinh - Thả thính\n"
                f"📜 {PREFIX}cadao - Ca dao\n"
                f"🖼️ {PREFIX}tti <văn bản> - Văn bản thành ảnh\n"
                f"❓ {PREFIX}hoingu - Hỏi ngu\n"
                f"🔗 {PREFIX}noitu <từ> - Trò chơi nối từ\n"
                f"🔮 {PREFIX}tarot - Bói Tarot\n"
                f"🦠 {PREFIX}covid <quốc gia> - Thống kê COVID-19\n"
                f"🔍 {PREFIX}sr - Tìm kiếm (pin, tt, cap, spot, scl, dl)\n"
                f"📧 {PREFIX}getemail - Lấy email tạm thời\n"
                f"📬 {PREFIX}showemail <email> - Xem hộp thư của email tạm\n"
                "═══════════════════════════════════════\n"
                "✏️ Lệnh Đổi Tên & File\n"
                "───────────────────────────────────────\n"
                f"📎 {PREFIX}sf <file> - Chọn file spam\n"
                f"📎 {PREFIX}sfdt <file> - Chọn file đa token\n"
                f"✍️ {PREFIX}es <file> <nội dung> - Sửa file\n"
                f"📄 {PREFIX}ns <file> <nội dung> - Tạo file mới\n"
                f"🌐 {PREFIX}taowh - Tạo webhook\n"
                f"🌐 {PREFIX}taowhsll <số> - Tạo nhiều webhook\n"
                "═══════════════════════════════════════\n"
                "🌐 Lệnh Khác\n"
                "───────────────────────────────────────\n"
                f"📋 {PREFIX}sv - Danh sách server\n"
                f"🆔 {PREFIX}id - Lấy ID bản thân\n"
                f"ℹ️ {PREFIX}i - Thông tin bot chi tiết\n"
                f"🔧 {PREFIX}spf <prefix> - Đổi prefix\n"
                f"📡 {PREFIX}ping - Kiểm tra độ trễ\n"
                f"🗑️ {PREFIX}cl <số> - Xóa tin nhắn\n"
                f"🚪 {PREFIX}ex - Thoát bot\n"
                f"❓ {PREFIX}help <lệnh> - Hướng dẫn chi tiết\n"
                "═══════════════════════════════════════\n"
                f"⏰ Thời gian: {current_time}\n"
                f"📅 Ngày: {current_date}\n"
                "```"
            )
        random_gif = random.choice(GIF_LINKS)
        await text_channel.send(random_gif)        
    elif cmd == "help":
        if not args:
            help_msg = await text_channel.send(
                "```css\n"
                "🌟 [HƯỚNG DẪN SỬ DỤNG BOT] 🌟\n"
                "════════════════════\n"
                f"📜 Sử dụng `{PREFIX}help <lệnh>` để xem chi tiết cách dùng.\n"
                f"📌 Ví dụ: `{PREFIX}help n` để xem cách dùng lệnh spam nhây.\n"
                "--------------------\n"
                "💡 Mẹo: Gõ lệnh chính xác để nhận hỗ trợ nhanh chóng!\n"
                "════════════════════\n"
                f"⏰ Thời gian: {current_time}\n"
                f"📅 Ngày: {current_date}\n"
                "```"
            )
        else:
            help_cmd = args[0].lower()
            help_text = {
                "n": f"📢 `{PREFIX}n [@tag]`\nGửi tin nhắn nhây từ `nhay.txt`, thêm tag người dùng nếu muốn.",
                "s": f"🎶 `{PREFIX}s [@tag]`\nThả sớ từ `so.txt`, thêm tag nếu muốn.",
                "sp": f"📜 `{PREFIX}sp`\nSpam nội dung từ file đã chọn bằng `{PREFIX}sf`.",
                "spwh": f"🌐 `{PREFIX}spwh <url>`\nSpam qua webhook từ file đã chọn.",
                "ndt": f"🚀 `{PREFIX}ndt [@tag]`\nSpam nhây đa token từ `nhay.txt`.",
                "sdt": f"🚀 `{PREFIX}sdt [@tag]`\nThả sớ đa token từ `so.txt`.",
                "spdt": f"🚀 `{PREFIX}spdt`\nSpam đa token từ file đã chọn bằng `{PREFIX}sfdt`.",
                "whdt": f"🌐 `{PREFIX}whdt <url>`\nWebhook đa token từ file đã chọn.",
                "fsm": f"🖼️ `{PREFIX}fsm <link ảnh>`\nSpam ảnh từ link cung cấp.",
                "cfsm": f"💭 `{PREFIX}cfsm <@tag> <link ảnh>`\nSpam chửi kèm ảnh, dừng bằng `{PREFIX}st cfsm`.",
                "rl": f"💭 `{PREFIX}rl`\nBật/tắt auto reply khi bị tag, @here, @everyone từ `nhay.txt`.",
                "rep": f"📩 `{PREFIX}rep <@tag>`\nBật auto reply cho một người dùng cụ thể từ `nhay.txt`.",
                "urep": f"📪 `{PREFIX}urep <@tag>`\nTắt auto reply cho một người dùng cụ thể.",
                "c": f"📝 `{PREFIX}c <nội dung> <số lần> <độ trễ>`\nSpam nội dung tùy chỉnh với số lần và độ trễ (giây). Ví dụ: `{PREFIX}c Hello 5 1`.",
                "raid": f"💣 `{PREFIX}raid <server_id> <tên mới>`\nRaid server: đổi tên, xóa kênh/role, tạo kênh mới.",
                "sv": f"📋 `{PREFIX}sv`\nLiệt kê server bot tham gia.",
                "idkenh": f"📋 `{PREFIX}idkenh <server_id>`\nLiệt kê kênh trong server.",
                "checktt": f"📊 `{PREFIX}checktt <server_id>`\nKiểm tra tương tác server.",
                "checksv": f"📈 `{PREFIX}checksv <server_id>`\nKiểm tra chi tiết server.",
                "vc": f"🎤 `{PREFIX}vc <channel_id>`\nTreo voice với token chính.",
                "vcdt": f"🎛️ `{PREFIX}vcdt <channel_id>`\nTreo voice đa token.",
                "rn": f"📝 `{PREFIX}rn <server_id> <tên>`\nĐổi tên trong server.",
                "rndt": f"📝 `{PREFIX}rndt <server_id> <tên>`\nĐổi tên đa token.",
                "rsn": f"🗑️ `{PREFIX}rsn <server_id>`\nXóa tên trong server.",
                "sf": f"📎 `{PREFIX}sf <file>`\nChọn file để spam.",
                "sfdt": f"📎 `{PREFIX}sfdt <file>`\nChọn file để spam đa token.",
                "es": f"✍️ `{PREFIX}es <file> <nội dung>`\nSửa nội dung file.",
                "ns": f"📄 `{PREFIX}ns <file> <nội dung>`\nTạo file mới.",
                "thinh": f"💌 `{PREFIX}thinh`\nLấy câu thính ngẫu nhiên.",
                "tti": f"🖼️ `{PREFIX}tti <văn bản>`\nChuyển văn bản thành hình ảnh.",
                "hoingu": f"❓ `{PREFIX}hoingu`\nĐặt câu hỏi ngu ngẫu nhiên.",
                "noitu": f"🔗 `{PREFIX}noitu <từ>`\nChơi nối từ với từ đầu vào.",
                "covid": f"🦠 `{PREFIX}covid <quốc gia>`\nXem thống kê COVID-19 của quốc gia.",
                "dmall": f"📩 `{PREFIX}dmall <nội dung> <số lần>`\nGửi DM tới tất cả thành viên trong server.",
                "id": f"🆔 `{PREFIX}id [@tag]`\nLấy ID người dùng.",
                "i": f"ℹ️ `{PREFIX}i`\nXem thông tin chi tiết bot.",
                "spf": f"🔧 `{PREFIX}spf <prefix>`\nĐổi prefix bot.",
                "ping": f"📡 `{PREFIX}ping`\nKiểm tra độ trễ bot.",
                "cl": f"🗑️ `{PREFIX}cl <số lượng>`\nXóa số lượng tin nhắn.",
                "ex": f"🚪 `{PREFIX}ex`\nThoát bot.",
                "st": f"⛔ `{PREFIX}st <lệnh>`\nDừng lệnh đang chạy."
            }
            if help_cmd in help_text:
                help_msg = await text_channel.send(
                    f"```css\n"
                    f"❓ [HƯỚNG DẪN LỆNH `{help_cmd}`] ❓\n"
                    f"════════════════════\n"
                    f"{help_text[help_cmd]}\n"
                    f"--------------------\n"
                    f"💡 Gõ `{PREFIX}menu` để xem tất cả lệnh!\n"
                    f"════════════════════\n"
                    f"⏰ Thời gian: {current_time}\n"
                    f"📅 Ngày: {current_date}\n"
                    f"```"
                )
            else:
                help_msg = await text_channel.send(f"❌ Lệnh `{help_cmd}` không tồn tại! Dùng `{PREFIX}menu` để xem danh sách lệnh.", delete_after=0.01)

    elif cmd == "id":
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%d/%m/%Y")

        if not args:  
            created_at = message.author.created_at.strftime("%d/%m/%Y %H:%M:%S")
            response = (
                "```css\n"
                "✨ Thông Tin ID - Bản Thân ✨\n"
                "═════════════════════════════\n"
                f"👤 Tên: {message.author.name}\n"
                f"🆔 ID: {message.author.id}\n"
                f"📅 Tạo: {created_at}\n"
                "═════════════════════════════\n"
                f"⏰ {current_time} | 📅 {current_date}\n"
                "```"
            )
            msg = await text_channel.send(response)
            await asyncio.sleep(60)
            await msg.delete()

        elif args[0].startswith("<@"):  
            user_id = args[0].strip("<@!>").strip()
            response = (
                "```css\n"
                "✨ ID Người Dùng ✨\n"
                "═════════════════════════════\n"
                f"🆔 ID: {user_id}\n"
                "═════════════════════════════\n"
                f"⏰ {current_time} | 📅 {current_date}\n"
                "```"
            )
            msg = await text_channel.send(response)
            await asyncio.sleep(60)
            await msg.delete()

        elif args[0].startswith("<#") and message.guild:  
            channel_id = args[0].strip("<#>")
            channel = message.guild.get_channel(int(channel_id))
            if channel:
                response = (
                    "```css\n"
                    "✨ Thông Tin ID - Kênh ✨\n"
                    "═════════════════════════════\n"
                    f"📢 Tên: {channel.name}\n"
                    f"🆔 ID: {channel.id}\n"
                    f"🔧 Loại: {str(channel.type).capitalize()}\n"
                    f"🏰 Server: {message.guild.name} ({message.guild.id})\n"
                    "═════════════════════════════\n"
                    f"⏰ {current_time} | 📅 {current_date}\n"
                    "```"
                )
            else:
                response = (
                    "```css\n"
                    "🚫 Lỗi Thông Tin ID 🚫\n"
                    "═════════════════════════════\n"
                    "❌ Trạng thái: Không tìm thấy kênh\n"
                    f"💡 Gợi ý: {PREFIX}id #channel\n"
                    "═════════════════════════════\n"
                    f"⏰ {current_time} | 📅 {current_date}\n"
                    "```"
                )
            msg = await text_channel.send(response)
            await asyncio.sleep(60)
            await msg.delete()

        elif args[0].lower() == "server" and message.guild:  
            response = (
                "```css\n"
                "✨ Thông Tin ID - Server ✨\n"
                "═════════════════════════════\n"
                f"🏰 Tên: {message.guild.name}\n"
                f"🆔 ID: {message.guild.id}\n"
                f"👥 Thành viên: {message.guild.member_count}\n"
                "═════════════════════════════\n"
                f"⏰ {current_time} | 📅 {current_date}\n"
                "```"
            )
            msg = await text_channel.send(response)
            await asyncio.sleep(60)
            await msg.delete()

        else:  
            response = (
                "```css\n"
                "🚫 Lỗi Thông Tin ID 🚫\n"
                "═════════════════════════════\n"
                "❌ Trạng thái: Cú pháp không hợp lệ\n"
                f"💡 Gợi ý: {PREFIX}id, @user, #channel, server\n"
                "═════════════════════════════\n"
                f"⏰ {current_time} | 📅 {current_date}\n"
                "```"
            )
            msg = await text_channel.send(response, delete_after=0.01)

    elif cmd == "i":
        info = lấy_thông_tin_token(USER_TOKEN, message.guild.id if message.guild else None)
        if "error" in info:
            await text_channel.send(f"❌ Lỗi khi lấy thông tin: {info['error']}", delete_after=0.01)
            return

        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%d/%m/%Y")

        headers = {"Authorization": USER_TOKEN, "Content-Type": "application/json"}
        try:
            user_response = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=5)
            user_data = user_response.json() if user_response.status_code == 200 else {}
            email = user_data.get("email", "Không công khai")
            phone = user_data.get("phone", "Không công khai")
            verified = "Có" if user_data.get("verified", False) else "Không"
            mfa_enabled = "Có" if user_data.get("mfa_enabled", False) else "Không"
            premium_type = {0: "Không có Nitro", 1: "Nitro Classic", 2: "Nitro", 3: "Nitro Basic"}.get(user_data.get("premium_type", 0), "Không rõ")
            avatar_url = f"https://cdn.discordapp.com/avatars/{info['user_id']}/{user_data.get('avatar')}.png" if user_data.get("avatar") else "https://cdn.discordapp.com/embed/avatars/0.png"
        except Exception as e:
            email = phone = verified = mfa_enabled = premium_type = "Không thể lấy"
            avatar_url = "https://cdn.discordapp.com/embed/avatars/0.png"

        system_info = f"{platform.system()} {platform.release()} ({platform.machine()})"
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_cores = psutil.cpu_count(logical=True)
        cpu_physical_cores = psutil.cpu_count(logical=False)
        cpu_freq = psutil.cpu_freq()
        cpu_freq_info = f"{cpu_freq.current:.2f} MHz (Min: {cpu_freq.min:.2f}, Max: {cpu_freq.max:.2f})" if cpu_freq else "Không rõ"
        memory = psutil.virtual_memory()
        memory_usage = f"{memory.used / 1024 / 1024:.2f}/{memory.total / 1024 / 1024:.2f} MB ({memory.percent}%)"
        disk = psutil.disk_usage('/')
        disk_usage = f"{disk.used / 1024 / 1024 / 1024:.2f}/{disk.total / 1024 / 1024 / 1024:.2f} GB ({disk.percent}%)"
        uptime = tính_thời_gian_hoạt_động()
        latency = round(client.latency * 1000) if client.latency else "N/A"
        process = psutil.Process()
        memory_bot = process.memory_info().rss / 1024 / 1024
        threads_bot = process.num_threads()

        server_count = len(client.guilds)
        total_members = sum(guild.member_count for guild in client.guilds) if client.guilds else 0
        guild_name = message.guild.name if message.guild else "Không trong server"
        guild_id = message.guild.id if message.guild else "N/A"
        channel_count = len(message.guild.channels) if message.guild else 0
        voice_channels = len([vc for vc in client.voice_clients])
        active_spam = sum(1 for state in spam_states.values() for value in state.values() if value)

        detailed_info = (
            "```css\n"
            "🌟 [THÔNG TIN CHI TIẾT BOT] 🌟\n"
            "════════════════════\n"
            "📌 Tài Khoản\n"
            "--------------------\n"
            f"👤 Tên: {info['username']}\n"
            f"🎭 Tên hiển thị: {info['nick']}\n"
            f"🆔 ID: {info['user_id']}\n"
            f"📅 Ngày tạo: {info['created_at']}\n"
            f"📧 Email: {email}\n"
            f"📱 Số điện thoại: {phone}\n"
            f"✅ Xác minh: {verified}\n"
            f"🔒 MFA: {mfa_enabled}\n"
            f"💎 Nitro: {premium_type}\n"
            f"🖼️ Avatar: {avatar_url}\n"
            "════════════════════\n"
            "💻 Hệ Thống\n"
            "--------------------\n"
            f"🖥️ OS: {system_info}\n"
            f"📈 CPU: {cpu_usage}% ({cpu_physical_cores} nhân vật lý, {cpu_cores} luồng)\n"
            f"⏱️ Tần số CPU: {cpu_freq_info}\n"
            f"💾 RAM: {memory_usage}\n"
            f"💿 Ổ đĩa (/): {disk_usage}\n"
            f"🤖 RAM bot sử dụng: {memory_bot:.2f} MB\n"
            f"🧵 Luồng bot: {threads_bot}\n"
            f"⏰ Thời gian hoạt động: {uptime}\n"
            f"📡 Độ trễ: {latency}ms\n"
            "════════════════════\n"
            "🌐 Discord\n"
            "--------------------\n"
            f"🏰 Server: {server_count} (Tổng thành viên: {total_members})\n"
            f"📢 Server hiện tại: {guild_name} (ID: {guild_id})\n"
            f"🔊 Số kênh: {channel_count}\n"
            f"🎙️ Kênh voice đang treo: {voice_channels}\n"
            "════════════════════\n"
            "📊 Hoạt Động\n"
            "--------------------\n"
            f"🔧 Prefix: {PREFIX}\n"
            f"📩 Lệnh spam đang chạy: {active_spam}\n"
            f"📅 Ngày: {current_date}\n"
            f"⏰ Thời gian: {current_time}\n"
            "════════════════════\n"
            f"💡 Gõ `{PREFIX}menu` để xem tất cả lệnh!\n"
            "```"
            f"🔗 Link Avatar: {avatar_url}"
        )

        await text_channel.send(detailed_info)
        log_success(f"Đã hiển thị thông tin cho {message.author.id}")

    elif cmd == "vc" and len(args) >= 1:
        if message.guild is None:
            await text_channel.send("❌ Lệnh này chỉ hoạt động trong server!", delete_after=0.01)
            return
        try:
            channel_id = int(args[0])
            guild = message.guild
            channel = guild.get_channel(channel_id)
            if not channel or not isinstance(channel, discord.VoiceChannel):
                await text_channel.send("❌ Kênh voice không hợp lệ!", delete_after=0.01)
                return
            voice_client = await channel.connect()
            await voice_client.guild.change_voice_state(channel=channel, self_mute=True, self_deaf=True)
            log_success(f"Đã treo voice tại kênh `{channel.name}` (ID: {channel_id}) trong server `{guild.name}`")
            await text_channel.send(f"🎤 Đã treo voice tại kênh `{channel.name}` (ID: {channel_id})")
        except Exception as e:
            await text_channel.send(f"❌ Lỗi khi treo voice: {e}", delete_after=0.01)

    elif cmd == "vcdt" and len(args) >= 1:
        if message.guild is None:
            await text_channel.send("❌ Lệnh này chỉ hoạt động trong server!", delete_after=0.01)
            return
        try:
            channel_id = int(args[0])
            guild = message.guild
            channel = guild.get_channel(channel_id)
            if not channel or not isinstance(channel, discord.VoiceChannel):
                await text_channel.send("❌ Kênh voice không hợp lệ!", delete_after=0.01)
                return
            tokens = đọc_tokens_từ_file()
            if not tokens:
                await text_channel.send("❌ Không có token trong tokens.txt!", delete_after=0.01)
                return
            
            async def treo_voice_pynacl(token, guild_id, channel_id):
                intents = discord.Intents.default()
                intents.voice_states = True
                temp_client = discord.Client(intents=intents)
                success = False
                
                @temp_client.event
                async def on_ready():
                    nonlocal success
                    guild = temp_client.get_guild(guild_id)
                    if not guild:
                        await temp_client.close()
                        return
                    channel = guild.get_channel(channel_id)
                    if not channel or not isinstance(channel, discord.VoiceChannel):
                        await temp_client.close()
                        return
                    try:
                        voice_client = await channel.connect()
                        await voice_client.guild.change_voice_state(channel=channel, self_mute=True, self_deaf=True)
                        success = True
                        while not temp_client.is_closed():
                            await asyncio.sleep(10)
                        if voice_client.is_connected():
                            await voice_client.disconnect()
                        await temp_client.close()
                    except Exception:
                        await temp_client.close()
                
                try:
                    await temp_client.start(token, bot=False)
                except Exception:
                    pass
                return success
            
            tasks = {}
            for token in tokens:
                tasks[token] = client.loop.create_task(treo_voice_pynacl(token, guild.id, channel_id))
            
            await asyncio.sleep(10)
            success_count = 0
            for token, task in tasks.items():
                try:
                    if await task:
                        success_count += 1
                except Exception:
                    pass
            log_success(f"Đã treo voice đa token: {success_count}/{len(tokens)} token thành công trong server `{guild.name}`")
            await text_channel.send(f"🎛️ Đã treo voice đa token tại kênh `{channel.name}` (ID: {channel_id}): {success_count}/{len(tokens)} token thành công")
        except ValueError:
            await text_channel.send("❌ ID kênh phải là số!", delete_after=0.01)

    elif cmd == "vcx" and len(args) >= 1:
        if not message.guild:
            await text_channel.send("❌ Lệnh này chỉ hoạt động trong server!", delete_after=0.01)
            return

        voice_channel_id = args[0] 
        mp3_urls = [
            "https://files.catbox.moe/vd0nx3.mp3",
            "https://files.catbox.moe/vfmcqz.mp3"
        ]
        voice_channel = discord.utils.get(message.guild.voice_channels, id=int(voice_channel_id))
        if not voice_channel:
            await text_channel.send(f"❌ Không tìm thấy kênh voice với ID `{voice_channel_id}`!", delete_after=0.01)
            return
        permissions = voice_channel.permissions_for(message.guild.me)
        if not permissions.connect or not permissions.speak:
            await text_channel.send("❌ Bot không có quyền tham gia hoặc phát âm thanh trong kênh voice!", delete_after=0.01)
            return
        voice_client = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()

        try:
            vc = await voice_channel.connect()
            log_success(f"Đã tham gia kênh voice {voice_channel.name} (ID: {voice_channel.id})")
            channel_id = text_channel.id
            if channel_id not in spam_states:
                spam_states[channel_id] = {}
            spam_states[channel_id]["vcx"] = True

            await text_channel.send(
                f"🎵 Bắt đầu xả âm thanh (đơn token) trong kênh `{voice_channel.name}`! Dùng `{PREFIX}stop vcx` để dừng.",
                delete_after=60
            )
            index = 0
            while spam_states.get(channel_id, {}).get("vcx", False):
                try:
                    mp3_url = mp3_urls[index % len(mp3_urls)]
                    audio_source = discord.FFmpegPCMAudio(
                        mp3_url,
                        executable="ffmpeg", 
                        options="-vn"
                    )
                    audio_source = discord.PCMVolumeTransformer(audio_source, volume=2.0)  

                    if not vc.is_playing():
                        log_info(f"Chuẩn bị phát: {mp3_url}")
                        vc.play(audio_source, after=lambda e: log_info(f"Đã phát xong {mp3_url}: {e if e else 'Không có lỗi'}"))
                        log_success(f"Đang phát {mp3_url} với âm lượng tối đa (PyNaCl)")
                    while vc.is_playing() and spam_states.get(channel_id, {}).get("vcx", False):
                        await asyncio.sleep(1)

                    if not vc.is_connected():
                        log_error("Bot đã bị ngắt kết nối khỏi kênh voice!")
                        break

                    index += 1
                    await asyncio.sleep(0.5)  

                except Exception as e:
                    log_error(f"Lỗi khi phát âm thanh (vcx): {str(e)}")
                    await text_channel.send(f"⚠️ Lỗi phát âm thanh: {str(e)}. Thử lại...", delete_after=0.01)
                    if vc.is_connected():
                        vc.stop()  
                    await asyncio.sleep(5)  
            if vc.is_connected():
                vc.stop()
                await vc.disconnect()
                log_info(f"Đã rời kênh voice {voice_channel.name} do lệnh dừng vcx")
                await text_channel.send(f"⛔ Đã dừng xả âm thanh (vcx) và rời kênh `{voice_channel.name}`!", delete_after=0.01)

        except Exception as e:
            log_error(f"Lỗi khi tham gia/phát âm thanh (vcx): {str(e)}")
            await text_channel.send(f"❌ Lỗi: {str(e)}", delete_after=0.01)
            if voice_client and voice_client.is_connected():
                await voice_client.disconnect()
            

    elif cmd == "rndt" and len(args) >= 2:
        guild_id, new_nickname = args[0], " ".join(args[1:])
        tokens = đọc_tokens_từ_file()
        if not tokens:
            await text_channel.send("❌ Không có token trong tokens.txt!", delete_after=0.01)
            return
        result = đổi_tên_hiển_thị_đa_token(tokens, guild_id, new_nickname)
        await text_channel.send(result, delete_after=0.01)

    elif cmd == "rsn" and len(args) >= 1:
        guild_id = args[0]
        result = đổi_tên_hiển_thị(USER_TOKEN, guild_id, None)
        if "✅" in result:
            await text_channel.send(result, delete_after=0.01)
        else:
            await text_channel.send(result, delete_after=0.01)

    elif cmd == "n":
        if not spam_states[channel_id]["n"]:
            spam_states[channel_id]["n"] = True
            tags = [arg for arg in args if arg.startswith("<@")] if message.guild else None
            spam_threads[channel_id]["n"] = threading.Thread(target=spam_message, args=(text_channel, channel_id, tags), daemon=True)
            spam_threads[channel_id]["n"].start()
            await text_channel.send("✅ Bắt đầu spam nhây!", delete_after=0.01)
            log_success("Bắt đầu spam nhây!")

    elif cmd == "s":
        if not spam_states[channel_id]["s"]:
            spam_states[channel_id]["s"] = True
            tags = [arg for arg in args if arg.startswith("<@")] if message.guild else None
            spam_threads[channel_id]["s"] = threading.Thread(target=so_spam_message, args=(text_channel, channel_id, tags), daemon=True)
            spam_threads[channel_id]["s"].start()
            await text_channel.send("✅ Bắt đầu thả sớ!", delete_after=0.01)
            log_success("Bắt đầu thả sớ!")

    elif cmd == "sp":
        spam_file = spam_files.get(channel_id)
        if spam_file and os.path.exists(spam_file):
            content = đọc_spam_từ_file(spam_file)
            if content:
                spam_states[channel_id]["sp"] = True
                async def spam_forever():
                    while spam_states[channel_id].get("sp", False):
                        await text_channel.send(content)
                        await asyncio.sleep(5)
                client.loop.create_task(spam_forever())
                await text_channel.send("✅ Bắt đầu spam file!", delete_after=0.01)
                log_success("Bắt đầu spam file!")
            else:
                await text_channel.send("❌ File trống!", delete_after=0.01)
        else:
            await text_channel.send(f"❌ Chưa chọn file! Dùng `{PREFIX}sf <file>` để chọn.", delete_after=0.01)

    elif cmd == "spwh" and len(args) >= 1:
        if not spam_states[channel_id]["spwh"]:
            webhook_url = args[0]
            spam_file = spam_files.get(channel_id)
            if spam_file and os.path.exists(spam_file):
                content = đọc_spam_từ_file(spam_file)
                if content:
                    spam_states[channel_id]["spwh"] = True
                    spam_threads[channel_id]["spwh"] = threading.Thread(target=spam_webhook, args=(webhook_url, channel_id), daemon=True)
                    spam_threads[channel_id]["spwh"].start()
                    await text_channel.send("✅ Bắt đầu spam qua webhook!", delete_after=0.01)
                    log_success("Bắt đầu spam webhook!")
                else:
                    await text_channel.send("❌ File trống!", delete_after=0.01)
            else:
                await text_channel.send(f"❌ Chưa chọn file! Dùng `{PREFIX}sf <file>` để chọn.", delete_after=0.01)

    elif cmd == "ndt":
        if not spam_states[channel_id]["ndt"]:
            spam_states[channel_id]["ndt"] = True
            tags = [arg for arg in args if arg.startswith("<@")] if message.guild else None
            nhay_datoken(text_channel, channel_id, tags)
            await text_channel.send("✅ Bắt đầu nhây đa token!", delete_after=0.01)
            log_success("Bắt đầu nhây đa token!")

    elif cmd == "sdt":
        if not spam_states[channel_id]["sdt"]:
            spam_states[channel_id]["sdt"] = True
            tags = [arg for arg in args if arg.startswith("<@")] if message.guild else None
            so_datoken(text_channel, channel_id, tags)
            await text_channel.send("✅ Bắt đầu sớ đa token!", delete_after=0.01)
            log_success("Bắt đầu sớ đa token!")

    elif cmd == "spdt":
        spam_datoken_file = spam_datoken_files.get(channel_id)
        if spam_datoken_file and os.path.exists(spam_datoken_file):
            content = đọc_spam_từ_file(spam_datoken_file)
            if content:
                spam_states[channel_id]["spdt"] = True
                spam_datoken(text_channel, channel_id)
                await text_channel.send("✅ Bắt đầu spam đa token!", delete_after=0.01)
                log_success("Bắt đầu spam đa token!")
            else:
                await text_channel.send("❌ File trống!", delete_after=0.01)
        else:
            await text_channel.send(f"❌ Chưa chọn file! Dùng `{PREFIX}sfdt <file>` để chọn.", delete_after=0.01)

    elif cmd == "whdt" and len(args) >= 1:
        if not spam_states[channel_id]["whdt"]:
            webhook_url = args[0]
            tokens = đọc_tokens_từ_file()
            if tokens:
                spam_datoken_file = spam_datoken_files.get(channel_id)
                if spam_datoken_file and os.path.exists(spam_datoken_file):
                    content = đọc_spam_từ_file(spam_datoken_file)
                    if content:
                        spam_states[channel_id]["whdt"] = True
                        webhook_datoken(webhook_url, channel_id)
                        await text_channel.send("✅ Bắt đầu webhook đa token!", delete_after=0.01)
                        log_success("Bắt đầu webhook đa token!")
                    else:
                        await text_channel.send("❌ File trống!", delete_after=0.01)
                else:
                    await text_channel.send(f"❌ Chưa chọn file! Dùng `{PREFIX}sfdt <file>` để chọn.", delete_after=0.01)
            else:
                await text_channel.send("❌ Không có token trong tokens.txt!", delete_after=0.01)

    elif cmd == "fsm" and len(args) >= 1:
        if not spam_states[channel_id]["fsm"]:
            image_url = args[0]
            spam_states[channel_id]["fsm"] = True
            spam_threads[channel_id]["fsm"] = threading.Thread(target=spam_image, args=(text_channel, channel_id, image_url), daemon=True)
            spam_threads[channel_id]["fsm"].start()
            await text_channel.send("✅ Bắt đầu spam ảnh!", delete_after=0.01)
            log_success("Bắt đầu spam ảnh!")

    elif cmd == "chui" and len(args) >= 1:
        if not spam_states[channel_id]["chui"]:
            image_url = args[0]
            spam_states[channel_id]["chui"] = True
            spam_threads[channel_id]["chui"] = threading.Thread(target=spam_chui, args=(text_channel, channel_id, image_url), daemon=True)
            spam_threads[channel_id]["chui"].start()
            await text_channel.send("✅ Bắt đầu spam chửi!", delete_after=0.01)
            log_success("Bắt đầu spam chửi!")

    elif cmd == "cfsm" and len(args) >= 2:
        if not message.guild:
            await text_channel.send("❌ Lệnh này chỉ hoạt động trong server!", delete_after=0.01)
            return
        if not spam_states[channel_id]["cfsm"]:
            if args[0].startswith("<@") and "http" in args[1]:
                user_tag = args[0]
                image_url = args[1]
                spam_states[channel_id]["cfsm"] = True
                spam_threads[channel_id]["cfsm"] = threading.Thread(
                    target=spam_cfsm, 
                    args=(text_channel, channel_id, user_tag, image_url), 
                    daemon=True
                )
                spam_threads[channel_id]["cfsm"].start()
                await text_channel.send(f"✅ Bắt đầu spam chửi kèm ảnh cho {user_tag}!", delete_after=0.01)
                log_success(f"Bắt đầu spam chửi kèm ảnh cho {user_tag}!")
            else:
                await text_channel.send(f"❌ Cú pháp: `{PREFIX}cfsm <@tag> <link ảnh>`", delete_after=0.01)

    elif cmd == "sf" and len(args) >= 1:
        filename = args[0] + (".txt" if not args[0].endswith(".txt") else "")
        if os.path.exists(filename):
            content = đọc_spam_từ_file(filename)
            if content:
                spam_files[channel_id] = filename
                await text_channel.send(f"✅ Đã chọn file `{filename}` để spam!", delete_after=0.01)
                log_success(f"Đã chọn file `{filename}` để spam!")
            else:
                await text_channel.send("❌ File trống!", delete_after=0.01)
        else:
            await text_channel.send(f"❌ File `{filename}` không tồn tại!", delete_after=0.01)

    elif cmd == "sfdt" and len(args) >= 1:
        filename = args[0] + (".txt" if not args[0].endswith(".txt") else "")
        if os.path.exists(filename):
            content = đọc_spam_từ_file(filename)
            if content:
                spam_datoken_files[channel_id] = filename
                await text_channel.send(f"✅ Đã chọn file `{filename}` để spam đa token!", delete_after=0.01)
                log_success(f"Đã chọn file `{filename}` để spam đa token!")
            else:
                await text_channel.send("❌ File trống!", delete_after=0.01)
        else:
            await text_channel.send(f"❌ File `{filename}` không tồn tại!", delete_after=0.01)

    elif cmd == "es" and len(args) >= 2:
        filename = args[0] + (".txt" if not args[0].endswith(".txt") else "")
        if os.path.exists(filename):
            content = " ".join(args[1:])
            if ghi_spam_vào_file(filename, content):
                await text_channel.send(f"✅ Đã sửa file `{filename}`!", delete_after=0.01)
                log_success(f"Đã sửa file `{filename}`!")
            else:
                await text_channel.send(f"❌ Lỗi khi sửa file `{filename}`!", delete_after=0.01)
        else:
            await text_channel.send(f"❌ File `{filename}` không tồn tại!", delete_after=0.01)

    elif cmd == "ns" and len(args) >= 2:
        filename = args[0] + (".txt" if not args[0].endswith(".txt") else "")
        if not os.path.exists(filename):
            content = " ".join(args[1:])
            if ghi_spam_vào_file(filename, content):
                await text_channel.send(f"✅ Đã tạo file `{filename}`!", delete_after=0.01)
                log_success(f"Đã tạo file `{filename}`!")
            else:
                await text_channel.send(f"❌ Lỗi khi tạo file `{filename}`!", delete_after=0.01)
        else:
            await text_channel.send(f"❌ File `{filename}` đã tồn tại!", delete_after=0.01)

    elif cmd == "st" and len(args) >= 1:
        sub_cmd = args[0].lower()
        if sub_cmd in spam_states[channel_id]:
            spam_states[channel_id][sub_cmd] = False
            await text_channel.send(f"⛔ Đã dừng lệnh `{sub_cmd}`!", delete_after=0.01)
            log_success(f"Đã dừng lệnh `{sub_cmd}`!")
        else:
            await text_channel.send(f"❌ Lệnh `{sub_cmd}` không hợp lệ hoặc không chạy!", delete_after=0.01)

    elif cmd == "c" and len(args) >= 3:
        try:
            content = " ".join(args[:-2])
            times = int(args[-2])
            delay = float(args[-1])
            if times <= 0 or delay < 0:
                await text_channel.send("❌ Số lần và độ trễ phải lớn hơn 0!", delete_after=0.01)
                return
            await text_channel.send(f"✅ Bắt đầu spam `{content}` {times} lần, độ trễ {delay}s!", delete_after=0.01)
            log_success(f"Bắt đầu spam `{content}` {times} lần, độ trễ {delay}s!")
            for _ in range(times):
                await text_channel.send(content)
                await asyncio.sleep(delay)
        except ValueError:
            await text_channel.send(f"❌ Cú pháp: `{PREFIX}c <nội dung> <số lần> <độ trễ>`", delete_after=0.01)

    elif cmd == "raid" and len(args) >= 2:
        if not message.guild:
            await text_channel.send("❌ Lệnh này chỉ hoạt động trong server!", delete_after=0.01)
            return
        guild_id = args[0]
        new_server_name = " ".join(args[1:])
        result = await raid_server(guild_id, new_server_name)
        await text_channel.send(result, delete_after=0.01)

    elif cmd == "sv":
        servers = "\n".join([f"🏰 {guild.name} (ID: {guild.id}) - 👥 {guild.member_count} thành viên" for guild in client.guilds])
        await text_channel.send(
            f"```css\n"
            f"📋 [DANH SÁCH SERVER]\n"
            f"════════════════════\n"
            f"{servers if servers else 'Bot chưa tham gia server nào!'}\n"
            f"════════════════════\n"
            f"⏰ Thời gian: {current_time}\n"
            f"📅 Ngày: {current_date}\n"
            f"```"
        )

    elif cmd == "idkenh" and len(args) >= 1:
        guild_id = args[0]
        guild = client.get_guild(int(guild_id))
        if guild:
            channels = "\n".join([f"📢 {channel.name} (ID: {channel.id}) - {channel.type}" for channel in guild.channels])
            await text_channel.send(
                f"```css\n"
                f"📋 [DANH SÁCH KÊNH - {guild.name}]\n"
                f"════════════════════\n"
                f"{channels if channels else 'Không có kênh nào!'}\n"
                f"════════════════════\n"
                f"⏰ Thời gian: {current_time}\n"
                f"📅 Ngày: {current_date}\n"
                f"```"
            )
        else:
            await text_channel.send(f"❌ Không tìm thấy server với ID `{guild_id}`!", delete_after=0.01)

    elif cmd == "kiss":
        if message.guild is None:
            return
        
        kiss_gif = "https://files.catbox.moe/gry2gi.gif"
        members = [m for m in message.guild.members if not m.bot]
        
        if not members:
            return
        
        if len(args) == 0: 
            target = random.choice(members)
            message_content = f"{message.author.mention} nhẹ nhàng đặt một nụ hôn lên má {target.mention}, ngọt ngào như cách hôn mẹ ruột! 💋"
            await text_channel.send(message_content)
            await text_channel.send(kiss_gif)
            log_info(f"{message.author} đã hôn ngẫu nhiên {target} trong {message.guild.name}")
        
        elif len(message.mentions) > 0: 
            target = message.mentions[0]
            if target == message.author:
                return
            if target.bot:
                return
            message_content = f"{message.author.mention} nhẹ nhàng đặt một nụ hôn lên má {target.mention}, ngọt ngào như cách hôn mẹ ruột! 💋"
            await text_channel.send(message_content)
            await text_channel.send(kiss_gif)
            log_info(f"{message.author} đã hôn {target} trong {message.guild.name}")
        
        else:
            await text_channel.send(f"❌ Cú pháp: `{PREFIX}kiss` hoặc `{PREFIX}kiss @tag`!", delete_after=0.01)

    elif cmd == "love":
        if message.guild is None:
            return
        
        love_gif = "https://files.catbox.moe/0impan.gif"
        members = [m for m in message.guild.members if not m.bot]
        
        if not members:
            return
        
        if len(args) == 0:  
            target = random.choice(members)
            message_content = f"{message.author.mention} nắm tay {target.mention}, thì thầm rằng cả thế giới này không đẹp bằng nụ cười của em! 💞"
            await text_channel.send(message_content)
            await text_channel.send(love_gif)
            log_info(f"{message.author} đã gửi yêu thương ngẫu nhiên đến {target} trong {message.guild.name}")
        
        elif len(message.mentions) > 0:  
            target = message.mentions[0]
            if target == message.author:
                return
            if target.bot:
                return
            message_content = f"{message.author.mention} nắm tay {target.mention}, thì thầm rằng cả thế giới này không đẹp bằng nụ cười của em! 💞"
            await text_channel.send(message_content)
            await text_channel.send(love_gif)
            log_info(f"{message.author} đã gửi yêu thương đến {target} trong {message.guild.name}")
        
        else:
            await text_channel.send(f"❌ Cú pháp: `{PREFIX}love` hoặc `{PREFIX}love @tag`!", delete_after=0.01)

    elif cmd == "đấm":
        if message.guild is None:
            return
        
        punch_gif = "https://i.pinimg.com/originals/b3/b9/bf/b3b9bfce58ebd841a38f90069ab67f0b.gif"
        members = [m for m in message.guild.members if not m.bot]
        
        if not members:
            return
        
        if len(args) == 0:  
            target = random.choice(members)
            message_content = f"Con lồn {target.mention} ơi bố {message.author.mention} đấm chết cụ mày này con đĩ🏳️‍🌈!"
            await text_channel.send(message_content)  
            await text_channel.send(punch_gif)  
            log_info(f"{message.author} đã đấm ngẫu nhiên {target} trong {message.guild.name}")
        
        elif len(message.mentions) > 0:  
            target = message.mentions[0]
            if target == message.author:
                return
            if target.bot:
                return
            message_content = f"Con lồn {target.mention} ơi bố {message.author.mention} đấm chết cụ mày này con đĩ🏳️‍🌈!"
            await text_channel.send(message_content)  
            await text_channel.send(punch_gif)  
            log_info(f"{message.author} đã đấm {target} trong {message.guild.name}")
        
        else:
            await text_channel.send(f"❌ Cú pháp: `{PREFIX}đấm` hoặc `{PREFIX}đấm @tag`!", delete_after=0.01)

    elif cmd == "checktt" and len(args) >= 1:
        guild_id = args[0]
        guild = client.get_guild(int(guild_id))   
        if not guild:
            await text_channel.send(f"❌ Không tìm thấy server với ID `{guild_id}`!", delete_after=0.01)
            return
        async def count_messages(channel):
            message_count = 0
            async for _ in channel.history(limit=1000):
                message_count += 1
            return message_count
        channel_counts = {}
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).read_message_history:
                channel_counts[channel.name] = await count_messages(channel)
        result = "\n".join([f"📢 {name}: {count} tin nhắn" for name, count in channel_counts.items()])
        await text_channel.send(
            f"```css\n"
            f"📊 [KIỂM TRA TƯƠNG TÁC - {guild.name}]\n"
            f"════════════════════\n"
            f"{result if result else 'Không có dữ liệu!'}\n"
            f"════════════════════\n"
            f"⏰ Thời gian: {current_time}\n"
            f"📅 Ngày: {current_date}\n"
            f"```"
        )

    elif cmd == "checksv" and len(args) >= 1:
        guild_id = args[0]
        guild = client.get_guild(int(guild_id))
        if guild:
            member_count = guild.member_count
            channel_count = len(guild.channels)
            role_count = len(guild.roles) - 1
            owner = guild.owner.name if guild.owner else "Không rõ"
            created_at = guild.created_at.strftime("%d/%m/%Y %H:%M:%S")
            await text_channel.send(
                f"```css\n"
                f"📈 [KIỂM TRA SERVER - {guild.name}]\n"
                f"════════════════════\n"
                f"🏰 Tên: {guild.name} (ID: {guild.id})\n"
                f"👥 Thành viên: {member_count}\n"
                f"📢 Số kênh: {channel_count}\n"
                f"👑 Roles: {role_count}\n"
                f"👤 Chủ sở hữu: {owner}\n"
                f"📅 Tạo ngày: {created_at}\n"
                f"════════════════════\n"
                f"⏰ Thời gian: {current_time}\n"
                f"📅 Ngày: {current_date}\n"
                f"```"
            )
        else:
            await text_channel.send(f"❌ Không tìm thấy server với ID `{guild_id}`!", delete_after=0.01)

    elif cmd == "thinh":
        api_url = "https://hungdev.id.vn/randoms/thinh?apikey=3986ca"
        try:
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "data" in data:
                    thinh_text = data["data"]
                    # Định dạng giao diện đẹp hơn
                    formatted_message = (
                        "```css\n"
                        "💘 [CÂU THÍNH NGẪU NHIÊN] 💘\n"
                        "════════════════════\n"
                        f"💬 {thinh_text}\n"
                        "════════════════════\n"
                        f"⏰ Gửi lúc: {current_time}\n"
                        f"📅 Ngày: {current_date}\n"
                        "```"
                        "\n🌸 **Powered by Nguyễn Đăng Khoa** 🌸"
                    )
                    await text_channel.send(formatted_message, delete_after=60)
                    log_success("Đã lấy và gửi câu thính ngẫu nhiên từ API")
                else:
                    await text_channel.send(
                        "```css\n"
                        "❌ [LỖI]\n"
                        "Không lấy được câu thính từ API!\n"
                        "```",
                        delete_after=0.01
                    )
            else:
                await text_channel.send(
                    "```css\n"
                    "❌ [LỖI API]\n"
                    f"Mã lỗi: {response.status_code}\n"
                    "```",
                    delete_after=0.01
                )
        except Exception as e:
            await text_channel.send(
                "```css\n"
                "❌ [LỖI HỆ THỐNG]\n"
                f"Chi tiết: {str(e)}\n"
                "```",
                delete_after=0.01
            )
            log_error(f"Lỗi khi lấy câu thính: {str(e)}")

    elif cmd == "cadao":
        api_url = "https://hungdev.id.vn/randoms/cadao?apikey=3986ca"
        try:
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "data" in data:
                    cadao = data["data"]
                    result_message = (
                        "```css\n"
                        "📜 [CA DAO VIỆT NAM]\n"
                        "═══════\n"
                        f"💬 {cadao}\n"
                        "═══════\n"
                        f"⏰ {current_time} | 📅 {current_date}\n"
                        "```"
                    )
                    await text_channel.send(result_message, delete_after=60)
                    log_success("Đã lấy câu ca dao thành công")
                else:
                    await text_channel.send(
                        "```css\n"
                        "❌ Lỗi: Không lấy được ca dao!\n"
                        f"⏰ {current_time} | 📅 {current_date}\n"
                        "```",
                        delete_after=60
                    )
                    log_error("API ca dao trả về dữ liệu không hợp lệ")
            else:
                await text_channel.send(
                    "```css\n"
                    f"❌ Lỗi API: {response.status_code}\n"
                    f"⏰ {current_time} | 📅 {current_date}\n"
                    "```",
                    delete_after=60
                )
                log_error(f"Lỗi API ca dao: {response.status_code}")
        except Exception as e:
            await text_channel.send(
                "```css\n"
                f"❌ Lỗi kết nối: {str(e)}\n"
                f"⏰ {current_time} | 📅 {current_date}\n"
                "```",
                delete_after=60
            )
            log_error(f"Lỗi khi lấy ca dao: {str(e)}")

    elif cmd == "tarot":
        api_url = "https://subhatde.id.vn/tarot"
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    card = random.choice(data)
                    name = card["name"]
                    suite = card["suite"]
                    image_url = card["image"]
                    vi_desc = card["vi"]["description"]
                    vi_interp = card["vi"]["interpretation"]
                    vi_reversed = card["vi"]["reversed"]
                    is_reversed = random.choice([True, False])
                    state = "Ngược" if is_reversed else "Xuôi"
                    interpretation = vi_reversed if is_reversed else vi_interp
                    result_message = (
                        f"```css\n"
                        f"🔮 [BÓI TAROT - {state.upper()}]\n"
                        f"════════════════════\n"
                        f"🃏 Lá bài: {name} ({suite})\n"
                        f"📜 Mô tả: {vi_desc}\n"
                        f"💡 Ý nghĩa ({state}): {interpretation}\n"
                        f"════════════════════\n"
                        f"⏰ Thời gian: {current_time}\n"
                        f"📅 Ngày: {current_date}\n"
                        f"```"
                    )
                    image_response = requests.get(image_url, timeout=10)
                    if image_response.status_code == 200:
                        image_data = io.BytesIO(image_response.content)
                        picture = discord.File(image_data, filename=f"tarot_{name.replace(' ', '_')}.png")
                        await text_channel.send(result_message, file=picture, delete_after=120)
                        log_success(f"Đã bói Tarot: {name} ({state}) ")
                    else:
                        await text_channel.send(result_message, delete_after=120)
                        log_warning(f"Không tải được ảnh cho {name}: {image_response.status_code}")
                else:
                    await text_channel.send(
                        f"```css\n"
                        f"❌ [LỖI]\n"
                        f"Không lấy được lá bài Tarot từ API!\n"
                        f"```",
                        delete_after=0.01
                    )
                    log_error("API Tarot trả về dữ liệu không hợp lệ")
            else:
                await text_channel.send(
                    f"```css\n"
                    f"❌ [LỖI API]\n"
                    f"Mã lỗi: {response.status_code}\n"
                    f"```",
                    delete_after=0.01
                )
                log_error(f"Lỗi API Tarot: {response.status_code}")
        except Exception as e:
            await text_channel.send(
                f"```css\n"
                f"❌ [LỖI HỆ THỐNG]\n"
                f"Chi tiết: {str(e)}\n"
                f"```",
                delete_after=0.01
            )
            log_error(f"Lỗi khi bói Tarot: {str(e)}")

    elif cmd == "getemail":
        api_url = "https://hungdev.id.vn/temp-mails/get-email?apikey=3986ca"
        try:
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "data" in data:
                    email = data["data"]["email"]
                    token = data["data"]["token"]
                    result_message = (
                        "```css\n"
                        "📧 [EMAIL TẠM THỜI]\n"
                        "═══════\n"
                        f"✉️ Email: {email}\n"
                        f"🔑 Token: {token}\n"
                        f"💡 Dùng lệnh {PREFIX}showemail <email> để xem thư\n"
                        "═══════\n"
                        f"⏰ {current_time} | 📅 {current_date}\n"
                        "```"
                    )
                    await text_channel.send(result_message, delete_after=60)
                    log_success(f"Đã lấy email tạm thời: {email}")
                else:
                    await text_channel.send(
                        "```css\n"
                        "❌ Lỗi: Không lấy được email!\n"
                        f"⏰ {current_time} | 📅 {current_date}\n"
                        "```",
                        delete_after=60
                    )
                    log_error("API email trả về dữ liệu không hợp lệ")
            else:
                await text_channel.send(
                    "```css\n"
                    f"❌ Lỗi API: {response.status_code}\n"
                    f"⏰ {current_time} | 📅 {current_date}\n"
                    "```",
                    delete_after=60
                )
                log_error(f"Lỗi API get-email: {response.status_code}")
        except Exception as e:
            await text_channel.send(
                "```css\n"
                f"❌ Lỗi kết nối: {str(e)}\n"
                f"⏰ {current_time} | 📅 {current_date}\n"
                "```",
                delete_after=60
            )
            log_error(f"Lỗi khi lấy email tạm: {str(e)}")

    elif cmd == "showemail" and len(args) >= 1:
        email = args[0]
        api_url = f"https://hungdev.id.vn/temp-mails/show-email?email={email}&apikey=3986ca"
        try:
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "data" in data:
                    emails = data["data"]
                    if emails:
                        result_message = (
                            "```css\n"
                            f"📬 [HỘP THƯ - {email}]\n"
                            "═══════\n"
                        )
                        for i, mail in enumerate(emails, 1):
                            result_message += (
                                f"📧 Thư {i}:\n"
                                f"👤 Từ: {mail.get('from', 'Không rõ')}\n"
                                f"📜 Tiêu đề: {mail.get('subject', 'Không có')}\n"
                                f"💬 Nội dung: {mail.get('body', 'Trống')[:50]}...\n"
                                "─────\n"
                            )
                        result_message += (
                            f"⏰ {current_time} | 📅 {current_date}\n"
                            "```"
                        )
                    else:
                        result_message = (
                            "```css\n"
                            f"📬 [HỘP THƯ - {email}]\n"
                            "═══════\n"
                            "📭 Hộp thư trống!\n"
                            "═══════\n"
                            f"⏰ {current_time} | 📅 {current_date}\n"
                            "```"
                        )
                    await text_channel.send(result_message, delete_after=60)
                    log_success(f"Đã xem hộp thư của {email}")
                else:
                    await text_channel.send(
                        "```css\n"
                        "❌ Lỗi: Không xem được email!\n"
                        f"⏰ {current_time} | 📅 {current_date}\n"
                        "```",
                        delete_after=60
                    )
                    log_error("API show-email trả về dữ liệu không hợp lệ")
            else:
                await text_channel.send(
                    "```css\n"
                    f"❌ Lỗi API: {response.status_code}\n"
                    f"⏰ {current_time} | 📅 {current_date}\n"
                    "```",
                    delete_after=60
                )
                log_error(f"Lỗi API show-email: {response.status_code}")
        except Exception as e:
            await text_channel.send(
                "```css\n"
                f"❌ Lỗi kết nối: {str(e)}\n"
                f"⏰ {current_time} | 📅 {current_date}\n"
                "```",
                delete_after=60
            )
            log_error(f"Lỗi khi xem email {email}: {str(e)}")


    elif cmd == "taowh":
        if not message.guild:
            await text_channel.send(
                "```css\n"
                "❌ [LỖI]\n"
                "Lệnh này chỉ hoạt động trong server!\n"
                "```",
                delete_after=0.01
            )
            return
        if not text_channel.permissions_for(message.guild.me).manage_webhooks:
            await text_channel.send(
                "```css\n"
                "❌ [LỖI QUYỀN]\n"
                "Bot không có quyền 'Manage Webhooks'!\n"
                "```",
                delete_after=0.01
            )
            return
        webhook_url = await tạo_webhook(text_channel)
        if webhook_url:
            formatted_message = (
                "```css\n"
                "🌐 [TẠO WEBHOOK THÀNH CÔNG] 🌐\n"
                "════════════════════\n"
                f"📍 Kênh: {text_channel.name} (ID: {text_channel.id})\n"
                f"🔗 URL: {webhook_url}\n"
                "════════════════════\n"
                f"⏰ Thời gian: {current_time}\n"
                f"📅 Ngày: {current_date}\n"
                "```"
                "\n⚠️ **Lưu ý: Giữ URL này an toàn!**"
            )
            await text_channel.send(formatted_message, delete_after=60)
        else:
            await text_channel.send(
                "```css\n"
                "❌ [LỖI]\n"
                "Không thể tạo webhook!\n"
                "```",
                delete_after=0.01
            )

    elif cmd == "taowhsll" and len(args) >= 1:
        if not message.guild:
            await text_channel.send(
                "```css\n"
                "❌ [LỖI]\n"
                "Lệnh này chỉ hoạt động trong server!\n"
                "```",
                delete_after=0.01
            )
            return
        if not text_channel.permissions_for(message.guild.me).manage_webhooks:
            await text_channel.send(
                "```css\n"
                "❌ [LỖI QUYỀN]\n"
                "Bot không có quyền 'Manage Webhooks'!\n"
                "```",
                delete_after=0.01
            )
            return
        try:
            amount = int(args[0])
            if amount <= 0:
                await text_channel.send(
                    "```css\n"
                    "❌ [LỖI]\n"
                    "Số lượng phải lớn hơn 0!\n"
                    "```",
                    delete_after=0.01
                )
                return
            if amount > 10:
                amount = 10 
                log_warning("Số lượng yêu cầu vượt quá 10, giới hạn ở 10 webhook.")
            webhook_urls = await tạo_nhiều_webhook(text_channel, amount)
            if webhook_urls:
                webhook_list = "\n".join([f"🔗 Webhook {i+1}: {url}" for i, url in enumerate(webhook_urls)])
                formatted_message = (
                    "```css\n"
                    "🌐 [TẠO NHIỀU WEBHOOK THÀNH CÔNG] 🌐\n"
                    "════════════════════\n"
                    f"📍 Kênh: {text_channel.name} (ID: {text_channel.id})\n"
                    f"📊 Số lượng: {len(webhook_urls)}/{amount}\n"
                    f"{webhook_list}\n"
                    "════════════════════\n"
                    f"⏰ Thời gian: {current_time}\n"
                    f"📅 Ngày: {current_date}\n"
                    "```"
                    "\n⚠️ **Lưu ý: Giữ các URL này an toàn!**"
                )
                await text_channel.send(formatted_message, delete_after=60)
            else:
                await text_channel.send(
                    "```css\n"
                    "❌ [LỖI]\n"
                    "Không thể tạo webhook nào!\n"
                    "```",
                    delete_after=0.01
                )
        except ValueError:
            await text_channel.send(
                "```css\n"
                "❌ [LỖI]\n"
                "Vui lòng nhập số lượng hợp lệ! Cú pháp: {PREFIX}taowhsll <số lượng>\n"
                "```",
                delete_after=0.01
            )
    elif cmd == "checktoken":
        tokens = đọc_tokens_từ_file()
        if not tokens:
            await text_channel.send(
                "```css\n"
                "❌ [LỖI]\n"
                "Không có token nào trong tokens.txt!\n"
                "════════════════════\n"
                f"⏰ Thời gian: {current_time}\n"
                f"📅 Ngày: {current_date}\n"
                "```",
                delete_after=60
            )
            log_error("Không có token trong tokens.txt để kiểm tra")
            return
        token_counts = {}
        for token in tokens:
            token_counts[token] = token_counts.get(token, 0) + 1
        unique_tokens = set(tokens)
        duplicate_count = len(tokens) - len(unique_tokens)
        duplicates = {token: count for token, count in token_counts.items() if count > 1}

        if duplicate_count > 0:
            duplicate_list = "\n".join([f"- {token[:10]}...: {count} lần" for token, count in duplicates.items()])
            log_warning(f"Phát hiện {duplicate_count} token trùng lặp:\n{duplicate_list}")

        stats = {
            "total": len(tokens),
            "unique": len(unique_tokens),
            "duplicates": duplicate_count,
            "active": 0,
            "inactive": 0,
            "error": 0,
            "nitro": 0,
            "old_accounts": 0  
        }

        active_tokens = []
        inactive_tokens = []
        detailed_report = []
        for token in unique_tokens:
            headers = {
                "Authorization": token,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            try:
                response = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    stats["active"] += 1
                    active_tokens.append(token)
                    username = data.get("username", "Không rõ")
                    user_id = data.get("id", "0")
                    creation_time = datetime.fromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%Y-%m-%d')
                    account_age = (datetime.now() - datetime.strptime(creation_time, '%Y-%m-%d')).days
                    has_nitro = data.get("premium_type", 0) > 0
                    if has_nitro:
                        stats["nitro"] += 1
                    if account_age > 365:
                        stats["old_accounts"] += 1

                    token_short = token[:10] + "..."
                    detailed_report.append(
                        f"✅ Token: {token_short}\n"
                        f"   - Tên: {username}\n"
                        f"   - ID: {user_id}\n"
                        f"   - Ngày tạo: {creation_time}\n"
                        f"   - Nitro: {'Có' if has_nitro else 'Không'}\n"
                        f"   - Tuổi: {account_age} ngày"
                    )
                    log_success(f"Token {token_short} hoạt động - {username}")
                elif response.status_code == 401:
                    stats["inactive"] += 1
                    inactive_tokens.append(token)
                    detailed_report.append(f"❌ Token: {token[:10]}...\n   - Trạng thái: Không hợp lệ")
                    log_warning(f"Token {token[:10]}... không hợp lệ")
                else:
                    stats["error"] += 1
                    inactive_tokens.append(token)
                    detailed_report.append(f"⚠️ Token: {token[:10]}...\n   - Trạng thái: Lỗi {response.status_code}")
                    log_error(f"Token {token[:10]}... lỗi {response.status_code}")
            except Exception as e:
                stats["error"] += 1
                inactive_tokens.append(token)
                detailed_report.append(f"⚠️ Token: {token[:10]}...\n   - Trạng thái: Lỗi kết nối ({str(e)})")
                log_error(f"Token {token[:10]}... lỗi kết nối: {str(e)}")
            
            await asyncio.sleep(0.5) 
        active_file = "active_tokens.txt"
        inactive_file = "inactive_tokens.txt"
        report_file = "token_report.txt"
        try:
            if not os.path.exists(active_file):
                with open(active_file, "w", encoding="utf-8") as f:
                    f.write("")
                log_info(f"Đã tạo file mới: {active_file}")
            with open(active_file, "w", encoding="utf-8") as active_file_handle:
                active_file_handle.write("\n".join(active_tokens) + "\n")
            log_success(f"Đã lưu {len(active_tokens)} token hoạt động vào {active_file}")
        except Exception as e:
            log_error(f"Lỗi khi lưu {active_file}: {e}")
        try:
            if not os.path.exists(inactive_file):
                with open(inactive_file, "w", encoding="utf-8") as f:
                    f.write("")
                log_info(f"Đã tạo file mới: {inactive_file}")
            with open(inactive_file, "w", encoding="utf-8") as inactive_file_handle:
                inactive_file_handle.write("\n".join(inactive_tokens) + "\n")
            log_success(f"Đã lưu {len(inactive_tokens)} token không hợp lệ vào {inactive_file}")
        except Exception as e:
            log_error(f"Lỗi khi lưu {inactive_file}: {e}")
        try:
            if not os.path.exists(report_file):
                with open(report_file, "w", encoding="utf-8") as f:
                    f.write("")
                log_info(f"Đã tạo file mới: {report_file}")
            with open(report_file, "w", encoding="utf-8") as report_file_handle:
                report_file_handle.write(f"CHECK TOKEN REPORT - {current_date} {current_time}\n")
                report_file_handle.write("=" * 50 + "\n")
                report_file_handle.write(f"Tổng số token: {stats['total']}\n")
                report_file_handle.write(f"Token duy nhất: {stats['unique']}\n")
                report_file_handle.write(f"Token trùng lặp: {stats['duplicates']}\n")
                if duplicates:
                    report_file_handle.write("Danh sách token trùng lặp:\n")
                    for token, count in duplicates.items():
                        report_file_handle.write(f"- {token[:10]}...: {count} lần\n")
                report_file_handle.write("=" * 50 + "\n")
                report_file_handle.write("CHI TIẾT TOKEN:\n")
                report_file_handle.write("\n".join(detailed_report) + "\n")
            log_success(f"Đã lưu báo cáo chi tiết vào {report_file}")
        except Exception as e:
            log_error(f"Lỗi khi lưu {report_file}: {e}")
        duplicate_summary = f"Danh sách trùng lặp:\n{duplicate_list}\n" if duplicates else "Không có token trùng lặp.\n"
        result_message = (
            "```css\n"
            "🔍 [CHECK TOKEN - TỔNG QUAN]\n"
            "════════════════════════════\n"
            f"📊 Tổng số token: {stats['total']}\n"
            f"🔄 Token duy nhất: {stats['unique']} ({stats['duplicates']} trùng lặp)\n"
            f"{duplicate_summary}"
            f"✅ Hoạt động: {stats['active']} ({stats['active']/stats['total']*100:.1f}%)\n"
            f"❌ Không hợp lệ: {stats['inactive']} ({stats['inactive']/stats['total']*100:.1f}%)\n"
            f"⚠️ Lỗi: {stats['error']} ({stats['error']/stats['total']*100:.1f}%)\n"
            f"⭐ Có Nitro: {stats['nitro']} ({stats['nitro']/stats['total']*100:.1f}%)\n"
            f"🕰️ Tài khoản > 1 năm: {stats['old_accounts']} ({stats['old_accounts']/stats['total']*100:.1f}%)\n"
            "════════════════════════════\n"
            f"💾 Token hoạt động: {active_file}\n"
            f"💾 Token không hợp lệ: {inactive_file}\n"
            f"📄 Báo cáo chi tiết: {report_file}\n"
            f"⏰ Thời gian: {current_time}\n"
            f"📅 Ngày: {current_date}\n"
            "```"
        )
        
        await text_channel.send(result_message, delete_after=60)
        log_success(f"Đã kiểm tra {stats['total']} token: {stats['active']} hoạt động, {stats['inactive']} không hợp lệ, {stats['error']} lỗi, {stats['duplicates']} trùng lặp")
    elif cmd == "tti" and len(args) >= 1:
        text = " ".join(args)
        api_url = f"https://hungdev.id.vn/ai/text-to-image?query={text}&apikey=3986ca"
        try:
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "data" in data and len(data["data"]) > 0:
                    image_url = data["data"][0]
                    await text_channel.send(image_url, delete_after=60)
                    log_success(f"Đã tạo ảnh từ văn bản: {text}")
                else:
                    await text_channel.send("❌ Không tạo được ảnh từ văn bản!", delete_after=0.01)
            else:
                await text_channel.send(f"❌ Lỗi API: {response.status_code}", delete_after=0.01)
        except Exception as e:
            await text_channel.send(f"❌ Lỗi khi tạo ảnh: {str(e)}", delete_after=0.01)
            log_error(f"Lỗi khi tạo ảnh từ văn bản '{text}': {str(e)}")
    elif cmd == "hoingu":
        questions = [
            "Trái chuối màu gì?",
            "1+1 bằng bao nhiêu?",
            "Trái đất có hình gì?"
        ]
        await text_channel.send(random.choice(questions), delete_after=60)

    elif cmd == "noitu" and len(args) >= 1:
        word = args[0].lower()
        suggestions = {
            "mèo": "con",
            "con": "gái",
            "gái": "xinh",
            "xinh": "đẹp"
        }
        next_word = suggestions.get(word, "Không biết nối từ gì!")
        await text_channel.send(f"{word} -> {next_word}", delete_after=60)

    elif cmd == "covid" and len(args) >= 1:
        country = " ".join(args)
        url = f"https://disease.sh/v3/covid-19/countries/{country}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                result = (
                    f"```css\n"
                    f"🦠 [THỐNG KÊ COVID-19 - {data['country']}]\n"
                    f"════════════════════\n"
                    f"👥 Dân số: {data['population']:,}\n"
                    f"😷 Ca nhiễm: {data['cases']:,}\n"
                    f"💀 Tử vong: {data['deaths']:,}\n"
                    f"💊 Hồi phục: {data['recovered']:,}\n"
                    f"🏥 Đang điều trị: {data['active']:,}\n"
                    f"⏰ Cập nhật: {datetime.fromtimestamp(data['updated']/1000).strftime('%d/%m/%Y %H:%M:%S')}\n"
                    f"════════════════════\n"
                    f"⏰ Thời gian: {current_time}\n"
                    f"📅 Ngày: {current_date}\n"
                    f"```"
                )
                await text_channel.send(result, delete_after=60)
            else:
                await text_channel.send(f"❌ Không tìm thấy dữ liệu cho `{country}`!", delete_after=0.01)
        except Exception as e:
            await text_channel.send(f"❌ Lỗi khi lấy dữ liệu: {e}", delete_after=0.01)

    elif cmd == "dmall" and len(args) >= 2:
        if not message.guild:
            await text_channel.send("❌ Lệnh này chỉ hoạt động trong server!", delete_after=0.01)
            return
        content = " ".join(args[:-1])
        times = int(args[-1])
        if times <= 0:
            await text_channel.send("❌ Số lần phải lớn hơn 0!", delete_after=0.01)
            return
        success_count = 0
        for member in message.guild.members:
            if member != client.user and not member.bot:
                try:
                    for _ in range(times):
                        await member.send(content)
                        await asyncio.sleep(1)
                    success_count += 1
                except discord.Forbidden:
                    log_error(f"Không thể gửi DM tới {member.name}")
                except Exception as e:
                    log_error(f"Lỗi khi gửi DM tới {member.name}: {e}")
        await text_channel.send(f"✅ Đã gửi DM tới {success_count}/{message.guild.member_count} thành viên!", delete_after=0.01)

    elif cmd == "spf" and len(args) >= 1:
        new_prefix = args[0]
        PREFIX = new_prefix
        lưu_thông_tin_vào_file(USER_TOKEN, ALLOWED_USER_ID, PREFIX)
        await text_channel.send(f"✅ Đã đổi prefix thành `{new_prefix}`!", delete_after=0.01)
        log_success(f"Đã đổi prefix thành `{new_prefix}`!")

    elif cmd == "ping":
        latency = round(client.latency * 1000)
        await text_channel.send(f"📡 Độ trễ: {latency}ms", delete_after=60)

    elif cmd == "cl" and len(args) >= 1:
        if not message.guild:
            await text_channel.send("❌ Lệnh này chỉ hoạt động trong server!", delete_after=0.01)
            return
        try:
            amount = int(args[0])
            if amount <= 0 or amount > 100:
                await text_channel.send("❌ Số lượng phải từ 1 đến 100!", delete_after=0.01)
                return
            async for msg in text_channel.history(limit=amount + 1):
                await msg.delete()
            await text_channel.send(f"🗑️ Đã xóa {amount} tin nhắn!", delete_after=0.01)
            log_success(f"Đã xóa {amount} tin nhắn!")
        except ValueError:
            await text_channel.send(f"❌ Cú pháp: `{PREFIX}cl <số lượng>`", delete_after=0.01)

    elif cmd == "ex":
        await text_channel.send("🚪 Đang thoát bot...", delete_after=0.01)
        log_success("Bot đã thoát!")
        await client.close()
        sys.exit(0)

    elif cmd == "rl":
        REPLY_ACTIVE = not REPLY_ACTIVE
        status = "bật" if REPLY_ACTIVE else "tắt"
        await text_channel.send(f"💭 Auto reply đã được {status}!", delete_after=0.01)
        log_success(f"Auto reply đã được {status}!")

    elif cmd == "stop" and len(args) >= 1:
        stop_cmd = args[0].lower()
        if stop_cmd == "rl":
            REPLY_ACTIVE = not REPLY_ACTIVE
            if REPLY_ACTIVE:
                REPLY_ACTIVE = False
                await text_channel.send(f"⛔ Đã dừng auto reply (`rl`)!", delete_after=0.01)
                log_success("Đã dừng auto reply (rl)")
            else:
                await text_channel.send(f"❌ Auto reply (`rl`) hiện không chạy!", delete_after=0.01)
        elif stop_cmd in spam_states and spam_states[stop_cmd]:
            spam_states[stop_cmd] = False
            if stop_cmd in spam_threads:
                spam_threads[stop_cmd].cancel()
            await text_channel.send(f"⛔ Đã dừng lệnh `{stop_cmd}`!", delete_after=0.01)
            log_success(f"Đã dừng lệnh {stop_cmd}")
        else:
            await text_channel.send(f"❌ Lệnh `{stop_cmd}` hiện không chạy!", delete_after=0.01)
    elif cmd == "rep" and len(args) >= 1:
        if not message.guild:
            await text_channel.send("❌ Lệnh này chỉ hoạt động trong server!", delete_after=0.01)
            return
        if not message.mentions:
            await text_channel.send(f"❌ Cú pháp: `{PREFIX}rep <@tag>` - Vui lòng tag một người dùng!", delete_after=0.01)
            return
        user = message.mentions[0]  
        user_id = user.id
        try:
            replied_users.add(user_id)  
            lưu_cài_đặt()
            await text_channel.send(f"📩 Đã bật auto reply cho {user.name}!", delete_after=0.01)
            log_success(f"Đã bật auto reply cho {user.name}!")
        except Exception as e:
            await text_channel.send(f"❌ Lỗi khi bật auto reply: {str(e)}", delete_after=0.01)
            log_error(f"Lỗi khi bật auto reply cho {user.name}: {str(e)}")

    elif cmd == "urep" and len(args) >= 1:
        if not message.guild:
            await text_channel.send("❌ Lệnh này chỉ hoạt động trong server!", delete_after=0.01)
            return
        if not message.mentions:
            await text_channel.send(f"❌ Cú pháp: `{PREFIX}urep <@tag>` - Vui lòng tag một người dùng!", delete_after=0.01)
            return
        user = message.mentions[0]
        user_id = user.id
        try:
            if user_id in replied_users:
                replied_users.remove(user_id)
                lưu_cài_đặt()
                await text_channel.send(f"📪 Đã tắt auto reply cho {user.name}!", delete_after=0.01)
                log_success(f"Đã tắt auto reply cho {user.name}!")
            else:
                await text_channel.send(f"❌ Auto reply chưa được bật cho {user.name}!", delete_after=0.01)
        except Exception as e:
            await text_channel.send(f"❌ Lỗi khi tắt auto reply: {str(e)}", delete_after=0.01)
            log_error(f"Lỗi khi tắt auto reply cho {user.name}: {str(e)}")    
    elif cmd == "sr":
            if not args:
                response =(
                    f"```css\n"
                    f"🔍 [BẢNG LỆNH TÌM KIẾM - SR]\n"
                    f"════════════════════\n"
                    f"📌 Sử dụng: {PREFIX}sr <lệnh con> <nội dung tìm kiếm>\n"
                    f"--------------------\n"
                    f"🖼️ pin <từ khóa> » Tìm kiếm ảnh Pinterest\n"
                    f"🎥 tt <từ khóa> » Tìm kiếm video TikTok\n"
                    f"🎬 cap <từ khóa> » Tìm kiếm mẫu CapCut\n"
                    f"🎵 spot <tên bài> » Tìm kiếm nhạc Spotify\n"
                    f"🎧 scl <tên bài> » Tìm kiếm nhạc SoundCloud\n"
                    f"📥 dl <URL> » Download video/nhạc all nền tảng\n"
                    f"--------------------\n"
                    f"💡 Gõ `{PREFIX}sr tt jack bỏ con` để thử!\n"
                    f"════════════════════\n"
                    f"⏰ Thời gian: {current_time}\n"
                    f"📅 Ngày: {current_date}\n"
                    f"```"
                )
                await text_channel.send(response, delete_after=120)
                return

            sub_cmd = args[0].lower()
            query = " ".join(args[1:]) if len(args) > 1 else None
            if not query:
                await text_channel.send(f"❌ Vui lòng nhập nội dung tìm kiếm! Cú pháp: `{PREFIX}sr {sub_cmd} <nội dung>`", delete_after=3)
                return
            if sub_cmd == "pin":
                api_url = f"https://subhatde.id.vn/pinterest?search={query}"
                try:
                    response = requests.get(api_url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if "data" in data and len(data["data"]) > 0:
                            results = "\n".join([f"🖼️ <{url}>" for url in data["data"][:10]]) 
                            response_text = (
                                f"```css\n"
                                f"🖼️ [TÌM KIẾM PINTEREST - {query}]\n"
                                f"════════════════════\n"
                                f"Tổng: {data['count']} ảnh\n"
                                f"{results if results else 'Không tìm thấy ảnh!'}\n"
                                f"════════════════════\n"
                                f"⏰ Thời gian: {current_time}\n"
                                f"📅 Ngày: {current_date}\n"
                                f"```"
                            )
                            await text_channel.send(response_text, delete_after=120)
                            log_success(f"Đã tìm kiếm Pinterest: {query}")
                        else:
                            await text_channel.send(f"❌ Không tìm thấy ảnh nào trên Pinterest cho '{query}'!", delete_after=0.001)
                    else:
                        await text_channel.send(f"❌ Lỗi API Pinterest: {response.status_code}", delete_after=0.001)
                except Exception as e:
                    await text_channel.send(f"❌ Lỗi khi tìm kiếm Pinterest: {str(e)}", delete_after=0.001)
            elif sub_cmd == "tt":
                api_url = f"https://subhatde.id.vn/tiktok/searchvideo?keywords={query}"
                try:
                    response = requests.get(api_url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if data["code"] == 0 and "videos" in data["data"] and len(data["data"]["videos"]) > 0:
                            results = "\n".join([
                                f"{i}. {video['title']}\n   🖼️ Bìa: <{video['cover']}>\n   ▶️ Video: <{video['play']}>\n   👤 Tác giả: {video['author']['nickname']} | ⏱️ {video['duration']}s"
                                for i, video in enumerate(data["data"]["videos"][:3], 1) 
                            ])
                            response_text = (
                                f"```css\n"
                                f"🎥 [TÌM KIẾM TIKTOK - {query}]\n"
                                f"════════════════════\n"
                                f"{results if results else 'Không tìm thấy video!'}\n"
                                f"════════════════════\n"
                                f"⏰ Thời gian: {current_time}\n"
                                f"📅 Ngày: {current_date}\n"
                                f"```"
                            )
                            await text_channel.send(response_text, delete_after=120)
                            log_success(f"Đã tìm kiếm TikTok: {query}")
                        else:
                            await text_channel.send(f"❌ Không tìm thấy video TikTok nào cho '{query}'!", delete_after=0.001)
                    else:
                        await text_channel.send(f"❌ Lỗi API TikTok: {response.status_code}", delete_after=0.001)
                except Exception as e:
                    await text_channel.send(f"❌ Lỗi khi tìm kiếm TikTok: {str(e)}", delete_after=0.001)
            elif sub_cmd == "cap":
                api_url = f"https://subhatde.id.vn/capcut/search?keyword={query}"
                try:
                    response = requests.get(api_url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if isinstance(data, list) and len(data) > 0:
                            template = data[0]  
                            duration_sec = template['duration'] // 1000
                            video_url = template['video_url']
                            video_response = requests.get(video_url, timeout=15)
                            if video_response.status_code == 200:
                                video_data = io.BytesIO(video_response.content)
                                video_file = discord.File(video_data, filename="capcut_video.mp4")
                                response_text = (
                                    f"```css\n"
                                    f"🎬 [CAPCUT VIDEO - {query}]\n"
                                    f"════════════════════\n"
                                    f"📜 Tiêu đề: {template['title']}\n"
                                    f"👤 Tác giả: {template['author']['name']} (ID: {template['author']['unique_id']})\n"
                                    f"⏱️ Thời lượng: {duration_sec}s\n"
                                    f"❤️ Lượt thích: {template['like_count']} | 📺 Lượt xem: {template['play_amount']}\n"
                                    f"📌 Lượt dùng: {template['usage_amount']}\n"
                                    f"════════════════════\n"
                                    f"⏰ Thời gian: {current_time}\n"
                                    f"📅 Ngày: {current_date}\n"
                                    f"```"
                                )
                                await text_channel.send(response_text, file=video_file, delete_after=120)
                                log_success(f"Đã gửi video CapCut: {template['title']}")
                            else:
                                await text_channel.send(
                                    f"❌ Lỗi tải video CapCut: {video_response.status_code}",
                                    delete_after=0.001
                                )
                                log_warning(f"Không tải được video CapCut: {video_response.status_code}")
                        else:
                            await text_channel.send(f"❌ Không tìm thấy mẫu CapCut nào cho '{query}'!", delete_after=0.001)
                    else:
                        await text_channel.send(f"❌ Lỗi API CapCut: {response.status_code}", delete_after=0.001)
                except Exception as e:
                    await text_channel.send(f"❌ Lỗi khi tìm kiếm CapCut: {str(e)}", delete_after=0.001)
            elif sub_cmd == "spot":
                api_url = f"https://subhatde.id.vn/spotify?q={query}"
                try:
                    response = requests.get(api_url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if isinstance(data, list) and len(data) > 0:
                            results = "\n".join([
                                f"{i}. {song['title']} - {song['duration']}\n   🔗 {song['url']}"
                                for i, song in enumerate(data[:5], 1)  
                            ])
                            response_text = (
                                f"```css\n"
                                f"🎵 [TÌM KIẾM SPOTIFY - {query}]\n"
                                f"════════════════════\n"
                                f"{results if results else 'Không tìm thấy bài hát!'}\n"
                                f"════════════════════\n"
                                f"⏰ Thời gian: {current_time}\n"
                                f"📅 Ngày: {current_date}\n"
                                f"```"
                            )
                            await text_channel.send(response_text, delete_after=120)
                            log_success(f"Đã tìm kiếm Spotify: {query}")
                        else:
                            await text_channel.send(f"❌ Không tìm thấy bài hát nào trên Spotify cho '{query}'!", delete_after=0.001)
                    else:
                        await text_channel.send(f"❌ Lỗi API Spotify: {response.status_code}", delete_after=0.001)
                except Exception as e:
                    await text_channel.send(f"❌ Lỗi khi tìm kiếm Spotify: {str(e)}", delete_after=0.001)
            elif sub_cmd == "scl":
                api_url = f"https://hungdev.id.vn/soundcloud/search?query={query}&apikey=3986ca"
                try:
                    response = requests.get(api_url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("success") and "data" in data and len(data["data"]) > 0:
                            track = data["data"][0]  
                            author_name = track["user"].get("full_name", "Không rõ") if "user" in track else "Không rõ"
                            duration_min = track["duration"] // 60000
                            duration_sec = (track["duration"] % 60000) // 1000
                            download_link = track.get("link_download", None)
                            if download_link:
                                file_response = requests.get(download_link, timeout=15)
                                if file_response.status_code == 200:
                                    audio_data = io.BytesIO(file_response.content)
                                    audio_file = discord.File(audio_data, filename="soundcloud_track.mp3")
                                    response_text = (
                                        f"```css\n"
                                        f"🎧 [SOUNDCLOUD TRACK - {query}]\n"
                                        f"════════════════════\n"
                                        f"📜 Tiêu đề: {track['title']}\n"
                                        f"👤 Tác giả: {author_name}\n"
                                        f"⏱️ Thời lượng: {duration_min}:{duration_sec:02d}\n"
                                        f"❤️ Lượt thích: {track['likes_count']} | 📺 Lượt nghe: {track['playback_count']}\n"
                                        f"════════════════════\n"
                                        f"⏰ Thời gian: {current_time}\n"
                                        f"📅 Ngày: {current_date}\n"
                                        f"```"
                                    )
                                    await text_channel.send(response_text, file=audio_file, delete_after=120)
                                    log_success(f"Đã gửi nhạc SoundCloud: {track['title']}")
                                else:
                                    await text_channel.send(
                                        f"❌ Lỗi tải nhạc SoundCloud: {file_response.status_code}",
                                        delete_after=0.001
                                    )
                                    log_warning(f"Không tải được nhạc SoundCloud: {file_response.status_code}")
                            else:
                                await text_channel.send(
                                    f"❌ Không có link tải cho bài hát: {track['title']}!",
                                    delete_after=0.001
                                )
                        else:
                            await text_channel.send(f"❌ Không tìm thấy bài hát nào trên SoundCloud cho '{query}'!", delete_after=0.001)
                    else:
                        await text_channel.send(f"❌ Lỗi API SoundCloud: {response.status_code}", delete_after=0.001)
                except Exception as e:
                    await text_channel.send(f"❌ Lỗi khi tìm kiếm SoundCloud: {str(e)}", delete_after=0.001)
            elif sub_cmd == "dl":
                api_url = f"https://hungdev.id.vn/medias/down-aio?url={query}&apikey=3986ca"
                try:
                    response = requests.get(api_url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("success") and "data" in data:
                            media_data = data["data"]
                            author = media_data.get("author", "Không rõ")
                            best_media = None
                            for media in media_data["medias"]:
                                if media["quality"] in ["HD No Watermark", "No Watermark"]:
                                    best_media = media
                                    break
                            if not best_media:
                                best_media = media_data["medias"][0]

                            file_url = best_media["url"]
                            file_response = requests.get(file_url, timeout=20)
                            if file_response.status_code == 200:
                                file_content = file_response.content
                                file_extension = best_media["extension"]
                                file_name = f"download_{query.split('/')[-1]}.{file_extension}"

                                if len(file_content) < MAX_FILE_SIZE:
                                    file_data = io.BytesIO(file_content)
                                    await text_channel.send(
                                        f"📥 **Đã tải xuống từ {media_data['source'].capitalize()}**\n"
                                        f"📜 Tiêu đề: {media_data['title']}\n"
                                        f"👤 Tác giả: {author}\n"
                                        f"⏰ Thời gian: {current_time} | 📅 Ngày: {current_date}",
                                        file=discord.File(file_data, filename=file_name),
                                        delete_after=300
                                    )
                                    log_success(f"Đã tải và gửi file từ URL: {query}")
                                else:
                                    max_size_mb = MAX_FILE_SIZE // (1024 * 1024)
                                    await text_channel.send(
                                        f"❌ File quá lớn (>{max_size_mb}MB)! Đây là link nhúng:\n<{file_url}>",
                                        delete_after=120
                                    )
                            else:
                                await text_channel.send(f"❌ Lỗi khi tải file: {file_response.status_code}", delete_after=0.1)
                        else:
                            await text_channel.send(f"❌ Không thể tải xuống từ URL '{query}'!", delete_after=0.1)
                    else:
                        await text_channel.send(f"❌ Lỗi API Download: {response.status_code}", delete_after=0.1)
                except Exception as e:
                    await text_channel.send(f"❌ Lỗi khi tải xuống: {str(e)}", delete_after=0.1)

            else:
                await text_channel.send(f"❌ Lệnh con không hợp lệ! Các lệnh: pin, tt, cap, spot, scl, dl", delete_after=0.1)
async def xóa_tin_nhắn_sau_khoảng_thời_gian(message, delay):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except discord.NotFound:
        pass
    except discord.Forbidden:
        log_warning(f"Không có quyền xóa tin nhắn của {message.author.id}")
def kiểm_tra_key(user_key):
    payload = {"action": "verify", "key": user_key}
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        if response.status_code != 200:
            log_error(f"API trả về mã lỗi {response.status_code}")
            return False
        data = response.json()
        return data.get("status") == "success" and data.get("message") == "Key is valid"
    except Exception as e:
        log_error(f"Không thể kết nối tới API: {e}")
        return False

def kiểm_tra_api_key():
    for line in ASCII_ART:
        print(line)
    print(f"{yellow}[START] Bot Discord V3 by Nguyễn Đăng Khoa {reset}")
    
    log_info("Xin chào, Nguyễn Đăng Khoa")
    log_info("Chào mừng đến với Bot Discord v3 © Nguyễn Đăng Khoa")
    while True:
        user_key = input(f"{yellow}[INPUT] Vui lòng nhập key: {reset}").strip()
        if not user_key:
            log_error("Key không được để trống!")
            continue
        if kiểm_tra_key(user_key):
            log_success("Key hợp lệ! Bot đang khởi động...")
            for line in BANNER:
                print(f"{cyan}{line}{reset}")
            return user_key
        else:
            log_error("Key không hợp lệ hoặc đã bị thay đổi!")
            retry = input(f"{yellow}[INPUT] Thử lại? (y/n): {reset}").strip().lower()
            if retry != "y":
                log_error("Thoát bot do key không hợp lệ.")
                sys.exit(1)

if __name__ == "__main__":
    user_key = "DANGKHOA"
    if user_key:
        token = thiết_lập()
        try:
            client.run(token, bot=False)
        except Exception as e:
            log_error(f"Lỗi khi chạy bot: {e}")
            sys.exit(1)