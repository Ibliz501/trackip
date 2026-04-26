#!/usr/bin/env python3
import requests
import json
import sys
import time
from datetime import datetime
from colorama import init, Fore, Style
import socket
import dns.resolver
import pycountry

init(autoreset=True)

BANNER = f"""
{Fore.RED}{Style.BRIGHT}
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⢁⣼⣿⡿⠿⠛⢋⣡⢤⣶⣶⣶⣶⣶⣤⣤⣬⣭⣿⣿⣿⣿⣿⣿⡿⢋⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣴⢃⡾⠟⠋⢀⣠⢾⣿⣿⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣍⣀⠾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⢱⣿⠏⠌⣠⣤⠨⠵⠾⣿⡿⠿⢷⣯⣥⣐⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⡏⠀⠞⠁⠀⠀⠀⣀⣀⣀⣀⡀⠀⠉⠩⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⣮⡛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠿⠿⠇⠀⡇⠀⠀⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣤⣤⣍⣛⣛⣛⣛⡛⠛⣫⣾⣿⣿⣿⣿⣿⣿⣍⡻⠦⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⡿⢋⠵⠶⠷⠙⠀⠀⠀⠀⠰⠿⠿⢿⣿⠿⢿⣿⣿⣋⣴⣶⣮⣍⣋⣙⠫⣥⣐⠶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣬⣛⣻⡿⠿⠿⡟⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⢀⣴⣾⣿⣿⡿⠆⠀⡀⠀⠀⡤⢠⡄⡈⠙⠀⠛⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣙⠳⣌⡙⠿⣿⣿⣍⠻⣿⣿⣿⣿⣿⣿⣿⣿⠿⢋⡴⢃⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⡙⠿⠿⠿⠿⠟⣁⠀⣴⡟⠀⠀⣆⢱⣿⣿⣿⣿⡀⣄⡀⠉⠻⣿⣏⠻⣿⣿⣿⢿⣿⣷⣦⡉⠂⠈⠻⣿⣿⣮⡳⣭⣙⠛⠋⣭⣔⠂⢁⣴⣿⡟⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣷⣄⡑⠾⢋⣼⠃⢚⣿⠁⢰⠀⣿⡄⠛⣿⣿⢛⣡⣿⣿⣶⣄⠀⠙⠿⣮⡻⢿⣿⣿⣿⣿⣿⣷⣦⣄⣈⠻⠿⣿⣎⠻⣿⣶⣶⣤⣬⣍⡉⠉⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣶⣤⡄⢰⣾⣿⠀⢿⡄⠹⣿⣆⠸⣿⠸⡟⢿⣿⣿⣿⣟⠦⣀⠈⠻⢦⣝⠻⣿⣿⣿⣛⠻⠿⠿⣿⣷⣶⣾⣤⣬⠭⠉⣉⣋⣁⠲⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⡿⢋⣤⣾⣿⠿⢠⣿⣧⢰⡘⣿⡄⠱⣀⣴⣦⡝⠿⠻⣿⣧⡙⢷⣦⣀⠙⢷⣜⢿⣿⣿⣿⡷⢦⡀⠠⠈⣁⣀⠀⢠⣶⣿⡿⣿⣿⣦⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⡿⠿⠋⠀⣊⢸⢿⣿⠀⣿⡿⢸⠀⢯⣿⣿⣆⠘⢍⠻⣟⢧⡀⠈⠻⣿⣆⠙⢿⢿⣶⡤⠄⣀⢀⠤⠴⠋⣁⠀⠀⠸⡿⠸⣸⣿⡍⢿⠿⠶⠀⣉⡀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣶⣶⣶⣿⣿⠘⢸⣿⠀⣿⣇⢸⡆⠈⢻⣿⣿⣷⣄⠳⣌⢀⠣⠐⣀⠉⣭⡄⢬⣐⣈⠟⠷⠶⠤⠄⠙⠚⣛⣆⠀⢐⡁⠀⠘⠻⠿⠀⣶⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡟⠀⣾⣿⢸⢹⣿⠘⣷⠀⡄⠿⢿⣿⣿⣷⣬⡙⠧⠀⠻⣧⡙⣿⠸⠟⠛⠉⠉⠉⠃⡘⢸⣿⣿⠈⠀⣂⠁⠀⠀⠀⠘⢧⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠀⢿⣿⠸⠘⣧⢃⠻⡆⢶⡀⠻⣿⣿⣿⡿⣿⣳⡄⢀⠀⣁⠈⠀⠀⠀⠀⠀⠀⠀⣷⠘⢫⡏⠀⠀⠟⠀⡠⠀⠀⢘⠂⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⢰⣾⡏⠀⣷⡸⡄⢂⠀⠘⠛⠀⠈⠀⠙⠷⣮⡛⠃⠸⠷⠆⢠⣘⢀⠰⢶⠆⠀⣰⣿⠈⢸⡇⢠⣤⡶⠟⠁⠀⢠⣈⠻⢿⣶⣶⣬⣍⣛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⢃⡿⢋⠀⠇⢻⣷⡈⠀⠂⠀⠀⣄⠀⠀⠀⠀⢀⣩⣵⣶⣤⣾⣿⣿⣯⣤⣤⣤⣼⣿⠏⣴⠘⠀⠈⠉⠀⢠⠀⢠⣤⣤⣶⣿⣿⣿⣿⣿⣿⣿⣷⣦⣭⣛⡻⠿⣿⣿⣿⣿
⣿⣿⠿⢃⣨⣴⣿⠀⠅⠘⢻⠳⡄⠀⠀⠀⠘⠦⠈⠷⠀⣿⡟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣾⣯⠄⣴⢸⡄⠀⠈⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣭⣛⠿
⣿⣿⣿⣿⣿⣿⡟⢀⣼⣧⠀⠁⠙⢦⡀⠀⢶⣶⣤⣶⣿⣿⠇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣸⣿⣶⡿⠀⣃⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣷⣄⡂⠄⡀⠀⠀⠻⠿⣿⣿⣿⣧⣹⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⠏⢰⣿⣿⣏⢱⡆⢻⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢃⣠⣾⣿⡆⠘⢿⣿⣿⣿⣿⠛⢋⠭⠝⣂⣴⣾⣿⣿⡿⠁⢠⣿⣿⣿⣿⡘⡇⢸⡟⢸⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣴⣿⣿⣿⣿⣿⣷⣌⡻⢿⣿⣿⣶⣶⣾⣿⣿⣿⣿⡿⠋⡴⢃⣾⣿⣿⣿⣿⡇⡇⢸⠃⣿⡿⢣⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡶⢂⡍⢛⠿⢿⣿⣿⡿⠋⢠⣶⣦⣍⣛⠻⢿⣿⣿⣧⠇⠈⣸⢋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢡⣾⣿⡘⣿⣶⣮⡉⠐⠷⠘⣿⣿⣿⣿⣿⣦⣿⣿⠿⠀⠜⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣠⣿⣿⣿⣷⡘⣿⣿⣷⡀⡀⠀⢙⡛⠿⠿⠟⣛⣩⠄⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣰⣿⣿⣿⣿⣿⣷⡜⢿⣿⣷⡌⣄⠈⠿⠿⠥⠦⢙⡱⠂⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡙⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣰⣿⣿⣿⣿⣿⣿⣿⣷⣌⢶⣿⣿⣿⣆⠀⠲⣶⡾⠛⠁⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⢿⣷⠸⣿⣿⢡⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠻⣿⣿⣿⣷⡄⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⡌⢻⣿⣿⣿⣿⣆⠻⣧⣿⠇⣾⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡜⢿⣿⣿⣧⠀⠀⣾⡿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠻⣿⣿⣿⣿⣷⡼⠟⣸⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣻⣿⣿⣧⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡜⢿⣿⣿⣿⠁⢰⣿⡿⠿⠿⠛⠛⠛⠛⡛
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡁⢶⡆⠀⠉⠁⡀⠄⠀⠀⠀⠘⠿⠿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⠁⠠⠞⠋⠁⣀⣥⣴⣶⣶⠶⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣌⠻⠿⠿⢿⣿⡿⠛⠻⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⡠⣤⠙⠿⣿⡿⠁⠀⠀
                 {Fore.Blue} [ {Fore.Yellow} Trackl Ip By AnsXploit  {Fore.Blue}]{Style.RESET_ALL}
 {Fore.Green} TOOLS INI DI GUNAKAN UNTUK MELACAK LOKASI IP ADDRESS SESEORANG GUNNAKAN
   DENGAN BIJAK, JANGAN DI SALAG GUNAKAN
{Style.RESET_ALL}
"""

def print_table(title, data, columns):
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{title}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-'*80}{Style.RESET_ALL}")
    
    for key, value in data.items():
        print(f"{Fore.GREEN}│ {key:<25}{Style.RESET_ALL} {Fore.WHITE}: {value}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

def get_ip_info(ip_address):
    print(f"{Fore.YELLOW}[*] Melacak IP: {ip_address}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Mengambil data dari berbagai sumber...{Style.RESET_ALL}")
    
    results = {}
    
    # IP API (ip-api.com)
    try:
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('status') == 'success':
            results['ip_api'] = {
                'IP': data.get('query', ip_address),
                'Country': data.get('country', 'N/A'),
                'Country Code': data.get('countryCode', 'N/A'),
                'Region': data.get('regionName', 'N/A'),
                'City': data.get('city', 'N/A'),
                'Zip Code': data.get('zip', 'N/A'),
                'Latitude': data.get('lat', 'N/A'),
                'Longitude': data.get('lon', 'N/A'),
                'Timezone': data.get('timezone', 'N/A'),
                'ISP': data.get('isp', 'N/A'),
                'Organization': data.get('org', 'N/A'),
                'AS': data.get('as', 'N/A'),
                'Mobile': 'Yes' if data.get('mobile') else 'No',
                'Proxy': 'Yes' if data.get('proxy') else 'No',
                'Hosting': 'Yes' if data.get('hosting') else 'No'
            }
    except:
        results['ip_api'] = {'Error': 'Tidak dapat mengambil data dari ip-api.com'}

    # ipinfo.io
    try:
        url = f"https://ipinfo.io/{ip_address}/json"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'error' not in data:
            results['ipinfo'] = {
                'IP': data.get('ip', ip_address),
                'Hostname': data.get('hostname', 'N/A'),
                'City': data.get('city', 'N/A'),
                'Region': data.get('region', 'N/A'),
                'Country': data.get('country', 'N/A'),
                'Location': data.get('loc', 'N/A'),
                'Organization': data.get('org', 'N/A'),
                'Postal': data.get('postal', 'N/A'),
                'Timezone': data.get('timezone', 'N/A')
            }
    except:
        results['ipinfo'] = {'Error': 'Tidak dapat mengambil data dari ipinfo.io'}

    # IP WHOIS
    try:
        url = f"https://ipwhois.app/json/{ip_address}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('success', True):
            results['ipwhois'] = {
                'IP': data.get('ip', ip_address),
                'Success': data.get('success', True),
                'Type': data.get('type', 'N/A'),
                'Country': data.get('country', 'N/A'),
                'Country Code': data.get('country_code', 'N/A'),
                'Region': data.get('region', 'N/A'),
                'City': data.get('city', 'N/A'),
                'Latitude': data.get('latitude', 'N/A'),
                'Longitude': data.get('longitude', 'N/A'),
                'ISP': data.get('isp', 'N/A'),
                'Organization': data.get('org', 'N/A'),
                'ASN': data.get('asn', 'N/A'),
                'ASN Name': data.get('asn_name', 'N/A'),
                'Timezone': data.get('timezone', 'N/A'),
                'Timezone Name': data.get('timezone_name', 'N/A'),
                'Currency': data.get('currency', 'N/A'),
                'Currency Symbol': data.get('currency_symbol', 'N/A')
            }
    except:
        results['ipwhois'] = {'Error': 'Tidak dapat mengambil data dari ipwhois.app'}

    return results

def get_geolocation_map(lat, lon):
    if lat != 'N/A' and lon != 'N/A':
        return f"https://www.google.com/maps?q={lat},{lon}"
    return "Tidak tersedia"

def main():
    print(BANNER)
    
    print(f"{Fore.YELLOW}┌─[ MASUKKAN IP ADDRESS ]{Style.RESET_ALL}")
    ip_input = input(f"{Fore.GREEN}└──► {Style.RESET_ALL}").strip()
    
    if not ip_input:
        print(f"{Fore.RED}[!] IP Address tidak boleh kosong!{Style.RESET_ALL}")
        sys.exit(1)
    
    # Validasi IP sederhana
    parts = ip_input.split('.')
    if len(parts) != 4:
        print(f"{Fore.RED}[!] Format IP tidak valid! Contoh: 8.8.8.8{Style.RESET_ALL}")
        sys.exit(1)
    
    print("")
    start_time = time.time()
    
    # Track IP
    results = get_ip_info(ip_input)
    
    end_time = time.time()
    
    # Tampilkan hasil
    print(f"\n{Fore.CYAN}{'╔'}{'═'*78}{'╗'}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'║'}{' '*25}{Fore.RED}{Style.BRIGHT}HASIL PELACAKAN IP ADDRESS{Style.RESET_ALL}{Fore.CYAN}{' '*26}{'║'}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'╠'}{'═'*78}{'╣'}{Style.RESET_ALL}")
    
    # Ringkasan dari ip_api
    if 'ip_api' in results and 'Error' not in results['ip_api']:
        ip_data = results['ip_api']
        print(f"\n{Fore.CYAN}│{Fore.YELLOW} INFORMASI DASAR{Fore.CYAN}                                                                              │{Style.RESET_ALL}")
        print(f"{Fore.CYAN}├{Fore.CYAN}{'─'*78}{Fore.CYAN}┤{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ IP Address       {Fore.CYAN}: {Fore.WHITE}{ip_data.get('IP', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ Country         {Fore.CYAN}: {Fore.WHITE}{ip_data.get('Country', 'N/A')} ({ip_data.get('Country Code', 'N/A')}){Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ Region/State    {Fore.CYAN}: {Fore.WHITE}{ip_data.get('Region', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ City            {Fore.CYAN}: {Fore.WHITE}{ip_data.get('City', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ Zip Code        {Fore.CYAN}: {Fore.WHITE}{ip_data.get('Zip Code', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ Timezone        {Fore.CYAN}: {Fore.WHITE}{ip_data.get('Timezone', 'N/A')}{Style.RESET_ALL}")
        
        # Map link
        lat = ip_data.get('Latitude', 'N/A')
        lon = ip_data.get('Longitude', 'N/A')
        if lat != 'N/A' and lon != 'N/A':
            map_url = get_geolocation_map(lat, lon)
            print(f"{Fore.GREEN}│ Google Maps     {Fore.CYAN}: {Fore.BLUE}{map_url}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}├{Fore.CYAN}{'─'*78}{Fore.CYAN}┤{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.YELLOW} INFORMASI ISP & JARINGAN{Fore.CYAN}                                                                     │{Style.RESET_ALL}")
        print(f"{Fore.CYAN}├{Fore.CYAN}{'─'*78}{Fore.CYAN}┤{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ ISP             {Fore.CYAN}: {Fore.WHITE}{ip_data.get('ISP', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ Organization    {Fore.CYAN}: {Fore.WHITE}{ip_data.get('Organization', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ AS (Autonomous){Fore.CYAN}: {Fore.WHITE}{ip_data.get('AS', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ Mobile Network  {Fore.CYAN}: {Fore.WHITE}{ip_data.get('Mobile', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ Proxy/VPN       {Fore.CYAN}: {Fore.WHITE}{ip_data.get('Proxy', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ Hosting Provider{Fore.CYAN}: {Fore.WHITE}{ip_data.get('Hosting', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}├{Fore.CYAN}{'─'*78}{Fore.CYAN}┤{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.YELLOW} KOORDINAT GEOGRAFIS{Fore.CYAN}                                                                        │{Style.RESET_ALL}")
        print(f"{Fore.CYAN}├{Fore.CYAN}{'─'*78}{Fore.CYAN}┤{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ Latitude        {Fore.CYAN}: {Fore.WHITE}{ip_data.get('Latitude', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ Longitude       {Fore.CYAN}: {Fore.WHITE}{ip_data.get('Longitude', 'N/A')}{Style.RESET_ALL}")
    
    # Informasi tambahan dari ipwhois
    if 'ipwhois' in results and 'Error' not in results['ipwhois']:
        whois_data = results['ipwhois']
        print(f"{Fore.CYAN}├{Fore.CYAN}{'─'*78}{Fore.CYAN}┤{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.YELLOW} INFORMASI WHOIS & ASN{Fore.CYAN}                                                                      │{Style.RESET_ALL}")
        print(f"{Fore.CYAN}├{Fore.CYAN}{'─'*78}{Fore.CYAN}┤{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ ASN Number      {Fore.CYAN}: {Fore.WHITE}{whois_data.get('ASN', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ ASN Name        {Fore.CYAN}: {Fore.WHITE}{whois_data.get('ASN Name', 'N/A')}{Style.RESET_ALL}")
        if whois_data.get('Currency', 'N/A') != 'N/A':
            print(f"{Fore.GREEN}│ Currency        {Fore.CYAN}: {Fore.WHITE}{whois_data.get('Currency', 'N/A')} ({whois_data.get('Currency Symbol', 'N/A')}){Style.RESET_ALL}")
    
    # Informasi dari ipinfo
    if 'ipinfo' in results and 'Error' not in results['ipinfo']:
        info_data = results['ipinfo']
        print(f"{Fore.CYAN}├{Fore.CYAN}{'─'*78}{Fore.CYAN}┤{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.YELLOW} INFORMASI TAMBAHAN{Fore.CYAN}                                                                         │{Style.RESET_ALL}")
        print(f"{Fore.CYAN}├{Fore.CYAN}{'─'*78}{Fore.CYAN}┤{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ Hostname        {Fore.CYAN}: {Fore.WHITE}{info_data.get('Hostname', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│ Postal Code     {Fore.CYAN}: {Fore.WHITE}{info_data.get('Postal', 'N/A')}{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}├{Fore.CYAN}{'─'*78}{Fore.CYAN}┤{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│{Fore.YELLOW} WAKTU PELACAKAN{Fore.CYAN}                                                                           │{Style.RESET_ALL}")
    print(f"{Fore.CYAN}├{Fore.CYAN}{'─'*78}{Fore.CYAN}┤{Style.RESET_ALL}")
    print(f"{Fore.GREEN}│ Waktu Eksekusi   {Fore.CYAN}: {Fore.WHITE}{end_time - start_time:.2f} detik{Style.RESET_ALL}")
    print(f"{Fore.GREEN}│ Tanggal & Waktu  {Fore.CYAN}: {Fore.WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}{'╚'}{'═'*78}{'╝'}{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}[✓] Pelacakan selesai!{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Dibatalkan oleh pengguna{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")