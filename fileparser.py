import json, os

settingsc = {
    "file_ver": "2.0.1-beta",
    "default": {
        "engine": "engine",
        "engine_exe": "engine/PsychEngine.exe",
        "engine_mods": "engine/mods",
        "icon": "Default",
        "theme": "Dark",
        "mods": "mods",
        "lang": "EN",
        "time": "%d-%m-%Y"
    },
    "current": {
        "engine": "engine",
        "engine_exe": "engine/PsychEngine.exe",
        "engine_mods": "engine/mods",
        "icon": "Default",
        "theme": "Dark",
        "mods": "mods",
        "lang": "EN",
        "time": "%d-%m-%Y"
    },
    "themes": {
        "Dark": [
            "#2b2b2b",
            "#3c3c3c",
            "white"
        ],
        "Light": [
            "#dbdbdb",
            "#f5f5f5",
            "black"
        ]
    },
    "icons": {
        "Default": "assets/icon.ico",
        "Legacy": "assets/legacy_icon.ico"
    },
    "ver": "Ver 2.0-beta"
}

langc = {
    "file_ver": "2.0.1-beta",
    "EN": {
        "mod": {
            "run": "Run",
            "mdl": "Mod folder localization",
            "exe": "Executable?",
            "icon": "Mod icon",
            "new": "Recently added?",
            "nml": "No mod link",
            "edit": "Edit values",
            "name": "Mod name",
            "link": "Gamebanana/Gamejolt link",
            "save": "Save changes",
            "newb": "Uncheck recently added",
            "fav": [
                "Add to favourites",
                "Remove from favourites"
                ],
            "sf": {
                "war": [
                    "No mod name",
                    "There is no name for mod.\nMod has to have a name",
                    "Engine error",
                    "Engine folder does not exist!\nMake sure you downloaded PsychEngine and put it in the 'engine' folder",
                    "Engine exe file does not exist!\nCheck if you correctly placed the engine and it is PsychEngine"
                ],
                "inf": [
                    "Saved",
                    "Mod informations saved!"
                ]
            },
            "launch": [
                "Launched",
                "Times"
            ],
            "played": "Last played"
        },
        "settings": {
            "app": "Appearance",
            "icon": "Icon",
            "icop": [
                "Default",
                "Legacy"
            ],
            "theme": "Theme",
            "thop": [
                "Dark",
                "Light"
            ],
            "lang": "Language",
            "upt": [
                "Settings",
                "Settings saved \nTo see the result restart the program"
            ],
            "rst": [
                "Settings",
                "Settings successfuly reseted to default \nTo see the result restart the program"
            ],
            "time": "Date format",
            "reset": "Reset to default"
        },
        "main": {
            "btn": [
                "Info",
                "Settings",
                "Mod list",
                "Reload mods",
                "Mod browser"
            ],
            "lomd": "Loading mods...",
            "info": [
                "Info",
                "Friday Night Funkin Mod Loader",
                "Made by: NevrenDev"
            ]
        }
    },
    "PL": {
        "mod": {
            "run": "Uruchom",
            "mdl": "Lokalizacja foldera modu",
            "exe": "Wykonywalny?",
            "icon": "Ikona moda",
            "new": "Ostatnio dodany?",
            "nml": "Brak linku do moda",
            "edit": "Zmień wartości",
            "name": "Nazwa moda",
            "link": "Link do Gamebanana/Gamejolt",
            "save": "Zapisz zmiany",
            "newb": "Odznacz ostatnio dodany",
            "fav": [
                "Dodaj do ulubionych",
                "Usuń z ulubionych"
                ],
            "sf": {
                "war": [
                    "Brak nazwy moda",
                    "Nie ma wprowadzonej nazwy moda\nMod musi mieć nazwę",
                    "Błąd silnika",
                    "Folder z silnikiem nie istnieje\nUpewnij się, że pobrałeś PsychEngine i umieściłeś go w folderze 'engine'",
                    "Plik exe silnika nie istnieje!\nSprawdź czy dobrze umieściłeś silnik i jest to PsychEngine"
                ],
                "inf": [
                    "Zapisano",
                    "Informacje na temat moda zostały zapisane!"
                ]
            },
            "launch": [
                "Uruchomiono",
                "Razy"
            ],
            "played": "Ostatnio zagrano"
        },
        "settings": {
            "app": "Wygląd",
            "icon": "Ikona",
            "icop": [
                "Domyślna",
                "Stara"
            ],
            "theme": "Motyw",
            "thop": [
                "Ciemny",
                "Jasny"
            ],
            "lang": "Język",
            "upt": [
                "Ustawienia",
                "Ustawienia zostały zapisane\nAby zobaczyć zmiany, zrestartuj program"
            ],
            "rst": [
                "Ustawienia",
                "Pomyślnie zresetowano ustawienia do domyślnych \nAby zobaczyć zmiany, zrestartuj program"
            ],
            "time": "Format daty",
            "reset": "Zresetuj do domyślnych"
        },
        "main": {
            "btn": [
                "Informacje",
                "Ustawienia",
                "Lista modów",
                "Załaduj mody",
                "Przeglądarka modów"
            ],
            "lomd": "Wczytywanie modów...",
            "info": [
                "Informacje",
                "Mod Loader do Friday Night Funkin",
                "Stworzone przez: NevrenDev"
            ]
        }
    }
}

current_version = '2.0.1-beta'

def settings(file):
    if os.path.exists(file):
        update('s')
        return False
    else:
        with open("settings.json", "w", encoding="utf-8") as file:
            
            json.dump(settingsc, file, ensure_ascii=False, indent=4)
        return True
    
def language(file):
    if os.path.exists(file):
        update('l')
        return False
    else:
        with open("lang.json", "w", encoding="utf-8") as file:
            json.dump(langc, file, ensure_ascii=False, indent=4)
        return True
        
def update(type):
    if type == 's':
        with open("settings.json", 'r', encoding='utf-8') as file:
            st = json.load(file)
            
        if st["file_ver"] != current_version:
            with open("settings.json", 'w', encoding='utf-8') as file:
                json.dump(settingsc, file, ensure_ascii=False, indent=4)
    elif type == 'l':
        with open("lang.json", 'r', encoding='utf-8') as file:
            l = json.load(file)
            
        if l["file_ver"] != current_version:
            with open("lang.json", 'w', encoding='utf-8') as file:
                json.dump(langc, file, ensure_ascii=False, indent=4)