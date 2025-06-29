import requests
import csv
import os

api_key = '998B0F36D38C3D986B678FC5308AA631'

steam_ids = [
    '76561198831548361',
    '76561198397940810',
    '76561198970717047',
    '76561198364217015',
    '76561198333162897',
    '76561198241448688',
    '76561198304919971',
    '76561198171910965',
    '76561198403351463',
    '76561198103671808',
    '76561198047499266',
    '76561199174946691',
    '76561198073877451',
    '76561198151383580',
    '76561199464554662',
    '76561198215999856',
    '76561198209861043',
    '76561197993787110',
    '76561198203601508',
    '76561199150978792',
    '76561198382716016',
    '76561198077790740',
    '76561198062568918',
    '76561198021535330',
    '76561198022246174',
    '76561198174171821',
    '76561198146290252',
    '76561198869905597',
    '76561198134698473',
    '76561198379252632',
    '76561198285864361'


]

csv_file = r'C:\Users\crist\OneDrive\Documents\GitHub\Analisi-de-dades-mitjansant-Business-Intelligence-Un-estudi-de-casos-practics\codi\Steam\steam_games.csv'

existing = []

if os.path.exists(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as f:
        r = csv.reader(f)
        next(r)  
        existing = [row for row in r]

existing = [row for row in existing if row[0] not in steam_ids]

nous = []

for sid in steam_ids:
    url = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={api_key}&steamid={sid}&include_appinfo=true'
    r = requests.get(url)

    if r.status_code == 200:
        j = r.json()
        jocs = j['response'].get('games', [])
        for joc in jocs:
            appid = joc['appid']
            nom = joc.get('name', 'Desconegut')
            temps = joc.get('playtime_forever', 0)
            nous.append([sid, appid, nom, temps])
    else:
        print(f"Error amb {sid}: {r.status_code}")

with open(csv_file, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['SteamID', 'AppID', 'Game Name', 'Playtime (Minutes)'])
    w.writerows(existing + nous)

