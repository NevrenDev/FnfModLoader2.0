# |-------------------------------------------------------------------------------------------|
# |                               Fnf Mod Loader 2.0 and up                                   |
# |                    Made with determination (not love, I hate myself)                      |
# |                           No changing code without permission!!!                          |
# |                 (you can change it but cannot distribute it without permission)           |
# | If you downloaded it from somewhere else than https://github.com/NevrenDev/FnFModLoader2.0|
# | check the code to see if there's no virus injected (original isn't a virus no matter what |
# |                               the antivirus tells you)                                    |
# |                          Have fun with using the Mod Loader!                              |
# |                                  Credits to NevrenDev                                     |
# |-------------------------------------------------------------------------------------------|

import sys
import os, subprocess, shutil, json, configparser, time
from PyQt6.QtWidgets import QSizePolicy, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QListWidget, QListWidgetItem, QLineEdit, QMessageBox, QComboBox, QStackedWidget, QSpacerItem
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, QThread, pyqtSignal, QUrl
from configparser import NoOptionError
import fileparser as fp

# load mods
class ModLoaderThread(QThread):
    mod_loaded = pyqtSignal(dict)  # Emituje listę modów

    def run(self):
        mods_path = settings["current"]["mods"]

        # make 'mods' folder if it doesn't exist
        if not os.path.exists(mods_path):
            os.mkdir(mods_path)
            return

        mods_list = []  # Lista do przechowywania danych modów

        for folder_name in os.listdir(mods_path):
            folder_path = os.path.join(mods_path, folder_name)
            
            correct_folder = False

            if os.path.isdir(folder_path) and os.listdir(folder_path):
                while not correct_folder:
                    folder_path, correct_folder = self.check_folders(folder_path)
                
                mod_ini_path = os.path.join(folder_path, ".mod.ini")

                # create '.mod.ini' file if it doesn't exist
                if not os.path.exists(mod_ini_path):
                    config = configparser.ConfigParser()
                    config['ModData'] = {
                        'mod_name': folder_name,
                        'exe_file': self.find_file_in_folder(folder_path, '.exe'),
                        'icon': self.find_file_in_folder(folder_path, '.ico'),
                        'folder': folder_name,
                        'path': folder_path,
                        'mod_link': "None",
                        'new': 'True',
                        'launched': '0',
                        'last_played': "None",
                        'fav': 'False'
                    }
                    with open(mod_ini_path, 'w') as configfile:
                        config.write(configfile)

                config = configparser.ConfigParser()
                config.read(mod_ini_path)
                
                try:
                    fav = config.getboolean("ModData", 'fav')
                except NoOptionError:
                    config.set("ModData", "fav", 'False')
                    with open(mod_ini_path, 'w') as file:
                        config.write(file)
                    fav = False

                # mod data, important to properly show mod
                mod_data = {
                    'mod_name': config.get('ModData', 'mod_name', fallback=folder_name),
                    'icon_file': config.get('ModData', 'icon', fallback='None'),
                    'folder_path': folder_path,
                    'new': config.getboolean('ModData', 'new', fallback=True),
                    'fav': fav
                }
                mods_list.append(mod_data)

        mods_list.sort(key=lambda x: x['fav'], reverse=True)

        for md in mods_list:
            self.mod_loaded.emit(md)

    # finds .exe and .ico files in the mod folder
    def find_file_in_folder(self, folder_path, extension):
        for file_name in os.listdir(folder_path):
            if file_name.endswith(extension):
                return file_name
        return 'None'
    
    # checks if the mod isn't stacked inside folders (didn't test that yet)
    def check_folders(self, folder_path):
        folders = 0
        for item in os.listdir(folder_path):
            path = os.path.join(folder_path, item)
            if os.path.isdir(path):
                folders += 1
            if folders > 1:
                break
                
        if folders == 1:
            folder_path = path
            return folder_path, False
            
        return folder_path, True
    
# mod informations, edit mod info and run mod
class ModWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.lang = transl[lng]["mod"]
        self.config = configparser.ConfigParser()
        self.init_ui()

    # important to load correct mod data
    def set_data(self, mod_data):
        self.config.read(os.path.join(mod_data["folder_path"], ".mod.ini"))
        self.update_ui()
        
    # this makes UI  
    def init_ui(self):
        main = QWidget()
        layout = QVBoxLayout(main)
        
        self.setStyleSheet(f"background: {color1}; border-radius: 5px; padding: 10px;")
        
        layout.setSpacing(1)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.mod_name = QLabel()
        self.mod_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mod_name.setStyleSheet("font-size: 25px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.mod_name)
        
        icon_layout = QHBoxLayout()
        self.exe_icon = QLabel()
        self.exe_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_icon = QLabel()
        self.icon_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.new_icon = QLabel()
        self.new_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(self.exe_icon)
        icon_layout.addWidget(self.icon_icon)
        icon_layout.addWidget(self.new_icon)
        layout.addLayout(icon_layout)
        
        self.folder_label = QLabel()
        layout.addWidget(self.folder_label)
        
        self.link_label = QLabel()
        self.link_label.setOpenExternalLinks(True)
        layout.addWidget(self.link_label)
        
        stats_layout = QHBoxLayout()
        self.launched = QLabel()
        self.launched.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.launched.setMaximumWidth(100)
        self.launched.setFixedHeight(100)
        stats_layout.addWidget(self.launched)
        
        self.last_played = QLabel()
        self.last_played.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.last_played.setFixedHeight(100)
        self.last_played.setMaximumWidth(150)
        stats_layout.addWidget(self.last_played)
        
        layout.addLayout(stats_layout)
        
        editable_label = QLabel(self.lang["edit"])
        editable_label.setStyleSheet("font-size: 15px; font-weight: bold; margin-top: 10px;")
        editable_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(editable_label)
        
        name_layout = QHBoxLayout()
        name_label = QLabel(self.lang["name"])
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        html_layout = QHBoxLayout()
        html_label = QLabel(self.lang["link"])
        self.html_input = QLineEdit()
        html_layout.addWidget(html_label)
        html_layout.addWidget(self.html_input)
        layout.addLayout(html_layout)
        
        self.button_layout = QHBoxLayout()
        save_btn = MainWindow.create_button(self, "assets/save.svg", self.lang["save"], self.save)
        self.new_btn = MainWindow.create_button(self, "assets/new.svg", self.lang["newb"], self.uncheck)
        self.run_btn = MainWindow.create_button(self, "assets/run.svg", self.lang["run"], self.run)
        self.fav_btn = MainWindow.create_button(self, "assets/nfav.svg", self.lang["fav"][0], self.fav_toggle)
        self.button_layout.addWidget(save_btn)
        self.button_layout.addWidget(self.new_btn)
        self.button_layout.addWidget(self.run_btn)
        self.button_layout.addWidget(self.fav_btn)
        layout.addLayout(self.button_layout)
        
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
                
        self.setLayout(layout)
      
    # this updates UI  
    def update_ui(self):
        self.folder = self.config.get("ModData", "path")
        self.name = self.config.get("ModData", "mod_name")
        self.link = self.config.get('ModData', 'mod_link')
        self.new = self.config.getboolean("ModData", "new")
        exe = self.config.get("ModData", "exe_file")
        icon = self.config.get("ModData", "icon")
        launched = self.config.getint("ModData", "launched")
        last = self.config.get("ModData", "last_played")
        fav = self.config.getboolean("ModData", "fav")
        
        if fav:
            self.fav_btn.setIcon(QIcon("assets/fav.svg"))
            self.fav_btn.setToolTip(self.lang["fav"][1])
        else:
            self.fav_btn.setIcon(QIcon("assets/nfav.svg"))
            self.fav_btn.setToolTip(self.lang["fav"][0])
        
        self.mod_name.setText(self.name)
        self.run_btn.setToolTip(f"{self.lang["run"]} {self.name}")
        self.name_input.setText(self.name)
        
        self.launched.setText(f"{self.lang["launch"][0]}: <br><br> {launched} <br><br> {self.lang["launch"][1]}")
        
        if last == "None":
            self.last_played.setText(f"{self.lang["played"]}: <br><br> Never")
        else:
            self.last_played.setText(f"{self.lang["played"]}: <br><br> {last}")

        if self.new is True:
            self.new_icon.setText(f"{self.lang['new']} <br><br><br><img src='assets/yexe.svg' width=128 height=128")
            self.new_btn.show()
        else:
            self.new_icon.setText(f"{self.lang['new']} <br><br><br><img src='assets/nexe.svg' width=128 height=128")
            self.new_btn.hide()
        
        if self.link != "None":
            self.html_input.setText(self.link)
        
        path = os.path.abspath(self.folder)
        self.folder_label.setText(f"{self.lang["mdl"]}: <strong>{path}</strong>")
        
        if exe != "None":
            self.exe_icon.setText(f"{self.lang["exe"]} <br><br><br><img src='assets/yexe.svg' width=128 height=128>")
        else:
            self.exe_icon.setText(f"{self.lang["exe"]} <br><br><br><img src='assets/nexe.svg' width=128 height=128>")
            
        if icon:
            path = os.path.join(self.folder, icon)
            self.icon_icon.setText(f'{self.lang["icon"]} <br><br><br><img src="{path}" width=128 height=128>')
        else:
            self.icon_icon.setText(f'{self.lang["icon"]} <br>><br><br><img src="assets/default_icon.png" width=128 height=128>')
            
        if "gamebanana.com" in self.link:
            self.link_label.setText(f"Gamebanana: <strong><a href='{self.link}'>{self.link}</a></strong>")
        elif "gamejolt.com" in self.link:
            self.link_label.setText(f"Gamejolt: <strong><a href='{self.link}'>{self.link}</a></strong>")
        else:
            self.link_label.setText(self.lang["nml"])
           
    # this saves mod information 
    def save(self):
        path = os.path.join(self.folder, ".mod.ini")
        name = self.name_input.text()
        link = self.html_input.text()
        if name != self.name or link != self.link:
            if name == "":
                QMessageBox.warning(self, self.lang["sf"]["war"][0], self.lang["sf"]["war"][1])
                return
            self.config.set("ModData", "mod_name", name)
            self.config.set("ModData", "mod_link", self.html_input.text() if not "" else "None")
        
            with open(path, "w") as file:
                self.config.write(file)
            
                QMessageBox.information(self, self.lang["sf"]["inf"][0], self.lang["sf"]["inf"][1])
            
            self.update_ui(self.config.get("ModData", "path"))
           
    # this runs the mod         
    def run(self):
        exe = self.config.get("ModData", "exe_file", fallback=None)
        self.config.set("ModData", "launched", str(self.config.getint("ModData", "launched")+1))
        date = time.strftime("%d %B %Y %H:%M", time.localtime())
        self.config.set("ModData", "last_played", f'{date}')
        
        with open(os.path.join(self.folder, ".mod.ini"), 'w') as file:
            self.config.write(file)
          
        # uncheck the recently added tag, cuz if you played it then it isn't recently added  
        self.uncheck()
        self.update_ui()

        if exe != "None":
            # run .exe file
            exe_path = os.path.join(self.folder, exe)
            subprocess.Popen(exe_path, cwd=self.folder)
        else:
            # copy mod to engine and run the engine (using PsychEngine. Maybe will add more engines later)
            engine_mods = settings["current"]["engine_mods"]
            if not os.path.exists(settings["current"]["engine"]):
                QMessageBox.critical(self, self.lang["sf"]["war"][2], self.lang["sf"]["war"][3])
                return
                
            for file in os.listdir(engine_mods):
                file_path = os.path.join(engine_mods, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    
            shutil.copytree(self.folder, engine_mods, dirs_exist_ok=True)
            try:
                subprocess.Popen(settings["current"]["engine_exe"], cwd=settings["current"]["engine"])
            except:
                QMessageBox.critical(self, self.lang["sf"]["war"][2], self.lang["sf"]["war"][4])

    # unchecks the recently added tag if it annoys you
    def uncheck(self):
        path = os.path.join(self.folder, ".mod.ini")
        if self.new is True:
            self.config.set("ModData", "new", "False")
            
            with open(path, "w") as file:
                self.config.write(file)
                
            self.update_ui()
            
    def fav_toggle(self):
        fav = self.config.getboolean("ModData", "fav")
        if fav:
            self.config.set("ModData", 'fav', 'False')
        else:
            self.config.set("ModData", "fav", "True")
            
        with open(os.path.join(self.folder, ".mod.ini"), 'w') as file:
            self.config.write(file)
            
        self.update_ui()
        
# settings!
class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.lang = transl[lng]["settings"]
        self.init_ui()

    # makes UI
    def init_ui(self):
        main = QWidget()
        layout = QVBoxLayout(main)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet(f"""
            QWidget {{
                background: {color1};
            }}
            QLabel {{
                background: {color1};
                color: {font};
                padding: 15px;
            }}
            QComboBox {{
                background: {color2};
                padding: 15px;
                color: {font};
            }}
        """)

        appearance_label = QLabel(self.lang["app"])
        appearance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(appearance_label)

        icon_label = QLabel(self.lang["icon"])
        self.icon_dropdown = QComboBox()
        self.icon_dropdown.addItems(self.lang["icop"])

        icon_layout = QHBoxLayout()
        icon_layout.setSpacing(0)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.addWidget(icon_label)
        icon_layout.addWidget(self.icon_dropdown)

        theme_layout = QHBoxLayout()
        theme_layout.setSpacing(0)
        theme_layout.setContentsMargins(0, 0, 0, 0)
        theme_label = QLabel(self.lang["theme"])
        self.theme_dropdown = QComboBox()
        self.theme_dropdown.addItems(self.lang["thop"])
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_dropdown)
        
        lang_layout = QHBoxLayout()
        lang_layout.setSpacing(0)
        lang_layout.setContentsMargins(0, 0, 0, 0)
        lang_label = QLabel(self.lang["lang"])
        self.lang_dropdown = QComboBox()
        self.lang_dropdown.addItems(['EN', 'PL'])
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_dropdown)
        
        reset_btn = QPushButton()
        reset_btn.setText(self.lang["reset"])
        button_style = f"""
            QPushButton {{
                background: {color1};
                border: none;
                padding: 5px;
                border-radius: 10px;
                margin-top: 20px;
            }}
            QPushButton:hover {{
                background-color: {color2};
            }}
        """
        reset_btn.setStyleSheet(button_style)
        reset_btn.clicked.connect(self.reset_default)

        layout.addLayout(icon_layout)
        layout.addLayout(theme_layout)
        layout.addLayout(lang_layout)
        layout.addWidget(reset_btn)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(layout)
        
        self.update_ui()

        self.icon_dropdown.currentTextChanged.connect(self.update_icon_setting)
        self.theme_dropdown.currentTextChanged.connect(self.update_theme)
        self.lang_dropdown.currentTextChanged.connect(self.update_lang)
        
    # resets settings to default
    def reset_default(self):
        settings["current"] = settings["default"]
        
        with open("settings.json", 'w') as file:
            json.dump(settings, file, indent=4)
        
        QMessageBox.information(self, self.lang["rst"][0], self.lang["rst"][1])
        self.update_ui()
        
    # updates chosen options (only used in reset)
    def update_ui(self):
        current_icon = settings["current"]["icon"]
        if current_icon == "Default":
            self.icon_dropdown.setCurrentText(self.lang["icop"][0])
        else:
            self.icon_dropdown.setCurrentText(self.lang["icop"][1])
            
        current_theme = settings["current"]["theme"]
        if current_theme == "Dark":
            self.theme_dropdown.setCurrentText(self.lang["thop"][0])
        else:
            self.theme_dropdown.setCurrentText(self.lang["thop"][1])
            
        self.lang_dropdown.setCurrentText(settings["current"]["lang"])

    # saves icon change (who needs the legacy icon?)
    def update_icon_setting(self, value):
        if fp.settings("settings.json"):
            QMessageBox.warning(None, "Settings", "Settings file has been deleted, but do not worry\nNew settings file has been created!")
        if value != settings["current"]["icon"]:
            QMessageBox.information(self, self.lang["upt"][0], self.lang["upt"][1])
        
        if value in ["Default", "Domyślna"]:
            settings["current"]["icon"] = "Default"
        else:
            settings["current"]["icon"] = "Legacy"

        with open("settings.json", "w") as file:
            json.dump(settings, file, indent=4)
        
    # update theme (only 2 themes available, will add more in the future)    
    def update_theme(self, value):
        if fp.settings("settings.json"):
            QMessageBox.warning(None, "Settings", "Settings file has been deleted, but do not worry\nNew settings file has been created!")
        if value != settings["current"]['theme']:
            QMessageBox.information(self, self.lang["upt"][0], self.lang["upt"][1])
            if value in ["Dark", "Ciemny"]:
                settings["current"]["theme"] = "Dark"
            else:
                settings["current"]["theme"] = "Light"
                
            with open("settings.json", "w") as file:
                json.dump(settings, file, indent=4)
       
    # update language (who needs it when you can speak English?)         
    def update_lang(self, value):
        if fp.settings("settings.json"):
            QMessageBox.warning(None, "Settings", "Settings file has been deleted, but do not worry\nNew settings file has been created!")
        if value != settings["current"]["lang"]:
            QMessageBox.information(self, self.lang["upt"][0], self.lang["upt"][1])
            settings["current"]["lang"] = value
            
            with open("settings.json", "w") as file:
                json.dump(settings, file, indent=4)

# main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = transl[lng]["main"]
        btn = self.lang["btn"]

        self.setWindowTitle("FNF Mod Loader")
        self.setGeometry(100, 100, 800, 600)

        self.setWindowIcon(QIcon(settings["icons"][settings["current"]["icon"]]))

        # no way, no init_ui() it's cuz this was made first with help of ChatGPT (I'm dumb and can't code without help :<)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_widget.setStyleSheet(f"""
        background: url(assets/background.png) no-repeat center center;
        color: {font};
        """)

        main_layout = QHBoxLayout(main_widget)

        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sidebar_layout.setContentsMargins(5, 5, 5, 5)

        sidebar_style = f"""
            QWidget {{
                background: {color1};
                border-radius: 15px;
            }}
        """
        sidebar_widget.setStyleSheet(sidebar_style)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        self.mod_list_view = QWidget()
        self.mod_list_layout = QVBoxLayout(self.mod_list_view)
        
        # yeah this is how it changes tabs
        self.mod_view = ModWidget()
        self.settings_view = SettingsWidget()
        self.stacked_widget.addWidget(self.mod_list_view)
        self.stacked_widget.addWidget(self.settings_view)
        self.stacked_widget.addWidget(self.mod_view)
        self.stacked_widget.setStyleSheet("background: None;")
        
        # buttons!!!
        btn_info = self.create_button("assets/info.svg", btn[0], self.show_info)
        btn_settings = self.create_button("assets/settings.svg", btn[1], self.show_settings)
        btn_modlist = self.create_button("assets/modlist.svg", btn[2], self.show_mod_list)
        btn_reload = self.create_button("assets/reload.svg", btn[3], self.load_mods)
        btn_web = self.create_button("assets/web.svg", btn[4], self.show_web)

        sidebar_layout.addWidget(btn_info)
        sidebar_layout.addWidget(btn_settings)
        sidebar_layout.addWidget(btn_modlist)
        sidebar_layout.addWidget(btn_reload)
        sidebar_layout.addWidget(btn_web)

        self.loading_label = QLabel(self.lang["lomd"])
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet(f"color: {font}; font-weight: bold;")
        self.loading_label.setVisible(False)

        self.mod_list_container = QListWidget()
        self.mod_list_container.setStyleSheet(f"""
            QListWidget {{
                background: {color1};
                border-radius: 15px;
            }}
            QListWidget::item {{
                background: {color1};
                border-radius: 10px;
                padding: 2px;
            }}
            QListWidget::item:selected {{
                background: {color2};
            }}
        """)
        self.mod_list_container.itemDoubleClicked.connect(self.show_mod_view)

        self.mod_list_layout.addWidget(self.mod_list_container)
        self.mod_list_layout.addWidget(self.loading_label)

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.stacked_widget)

        self.load_mods()

    # that makes the buttons with icons
    def create_button(self, icon_path, tooltip_text, func=None):
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(32, 32))
        button.setToolTip(tooltip_text)
        button.setFixedSize(50, 50)

        button_style = f"""
            QPushButton {{
                background: {color1};
                border: none;
                padding: 5px;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {color2};
            }}
        """
        button.setStyleSheet(button_style)

        if func:
            button.clicked.connect(func)

        return button

    # load mods!!!
    def load_mods(self):
        self.loading_label.setVisible(True)
        self.mod_list_container.clear()

        self.loader_thread = ModLoaderThread()
        self.loader_thread.mod_loaded.connect(self.add_mod_to_list)
        self.loader_thread.finished.connect(self.loading_complete)
        self.loader_thread.start()

    # adds mods to the list
    def add_mod_to_list(self, mod_data):
        mod_item_widget = QWidget()
        mod_item_layout = QHBoxLayout(mod_item_widget)

        icon_label = QLabel()
        icon_path = os.path.join(mod_data['folder_path'], mod_data['icon_file']) if mod_data['icon_file'] != 'None' else "assets/default_icon.png"
        icon_label.setPixmap(QPixmap(icon_path).scaled(24, 24))
        icon_label.setMaximumWidth(32)
        mod_item_layout.addWidget(icon_label)
        
        spacer = QLabel("")
        spacer.setMaximumWidth(1)
        spacer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spacer.setStyleSheet("border: 2px solid black")
        mod_item_layout.addWidget(spacer)

        name_label = QLabel(mod_data['mod_name'])
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mod_item_layout.addWidget(name_label)
        
        spacer1 = QLabel("")
        spacer1.setMaximumWidth(7)
        spacer1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spacer1.setStyleSheet("border: 2px solid black; margin-right: 7px;")
        mod_item_layout.addWidget(spacer1)
        
        new_label = QLabel()
        new_label.setPixmap(QPixmap("assets/new.svg").scaled(12, 12))
        new_label.setMaximumWidth(32)
        mod_item_layout.addWidget(new_label)
        if mod_data['new']: new_label.show()
        else: new_label.hide()
        
        fav_label = QLabel()
        fav_label.setPixmap(QPixmap("assets/fav.svg").scaled(24, 24))
        fav_label.setMaximumWidth(32)
        mod_item_layout.addWidget(fav_label)
        if mod_data['fav']: fav_label.show()
        else: fav_label.hide()
        

        mod_list_item = QListWidgetItem()
        mod_list_item.setSizeHint(mod_item_widget.sizeHint())
        mod_list_item.setData(Qt.ItemDataRole.UserRole, mod_data)

        self.mod_list_container.addItem(mod_list_item)
        self.mod_list_container.setItemWidget(mod_list_item, mod_item_widget)

    # this shows settings
    def show_settings(self):
        self.stacked_widget.setCurrentWidget(self.settings_view)

    # this shows the mod list
    def show_mod_list(self):
        self.stacked_widget.setCurrentWidget(self.mod_list_view)
        
    # this shows mod info
    def show_mod_view(self, item):
        mod_data = item.data(Qt.ItemDataRole.UserRole)
        self.mod_view.set_data(mod_data)
        self.stacked_widget.setCurrentWidget(self.mod_view)
      
    #this should show Mod browser, but it's in developement (don't hate)  
    def show_web(self):
        QMessageBox.information(self, "Web", "This function is work in progress. \nPlease wait until it's complete")

    # another function connected with loading mods
    def loading_complete(self):
        
        
        self.loading_label.setVisible(False)
            
    # shows information    
    def show_info(self):
        QMessageBox.information(self, self.lang["info"][0], self.lang["info"][1]+"\n"+settings["ver"]+"\n"+self.lang["info"][2])

# this makes the program go vrrrr (makes it work)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # no deleting files it makes so settings come back once deleted :>
    fp.settings("settings.json")

    with open("settings.json", "r") as file:
        settings = json.load(file)

    # same thing here but for language
    fp.language("lang.json")
        
    with open("lang.json", "r", encoding="utf-8") as file:
        transl = json.load(file)
        
    lng = settings["current"]["lang"]
        
    # theme loading :D
    color1 = settings["themes"][settings["current"]["theme"]][0]
    color2 = settings["themes"][settings["current"]["theme"]][1]
    font = settings["themes"][settings["current"]["theme"]][2]
    # actually makes the program work
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
