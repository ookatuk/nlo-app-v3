import base64
import hashlib
import json
import os
import platform
import subprocess
import sys
import traceback
from logging import config, getLogger

import i18n
import psutil  # 追記
import requests
from cryptography.fernet import Fernet
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
                               QMainWindow, QMessageBox, QPushButton,
                               QStackedWidget, QVBoxLayout)

# constant

VERSION = "v3.0.0-closed-test-alpha"


# Erorr list


class PageNotFound(BaseException):
    pass


# setting
i18n.set("skip_locale_root_data", True)
i18n.set("file_format", "json")
i18n.set("filename_format", "{locale}.{format}")

EXE_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))

IS_PY = sys.argv[0].split(".")[-1] == "py"

MODPACK_PATH = os.path.join(EXE_PATH, "mod")


with open(os.path.join(EXE_PATH,
                       "data",
                       "config",
                       "logger.json"),
          encoding="utf-8") as f:
    config.dictConfig(json.load(f))

logger = getLogger("main")

logger.info(f"""
path: {EXE_PATH}
is_py: {IS_PY}
modpack_path: {MODPACK_PATH}
""")

# Function


def check_setting_file(dir):
    if not os.path.isdir(os.path.join(dir, "data")):
        return False
    if not os.path.isdir(os.path.join(dir, "data", "setting")):
        return False

    setting_dir = os.path.join(dir, "data", "setting")

    if not os.path.isfile(os.path.join(setting_dir, "Language.json")):
        return False
    return True


def restart():
    args = [sys.executable] + sys.argv
    subprocess.Popen(args)
    sys.exit()


def get_device_fingerprint():
    """
    jen encrypt code
    """
    device_info = {
        "os_name": platform.system(),
        "cpu_cores": psutil.cpu_count(logical=False),
        "total_memory": psutil.virtual_memory().total,
        "disk_device": psutil.disk_partitions()[0].device,
        "disk_fstype": psutil.disk_partitions()[0].fstype,
    }
    device_string = (
        json.dumps(
            device_info,
            sort_keys=True
            )
        ).encode('utf-8')
    hash_hex = hashlib.blake2b(device_string, digest_size=32).hexdigest()

    hash_bytes = bytes.fromhex(hash_hex)

    urlsafe_base64 = base64.urlsafe_b64encode(hash_bytes)

    return urlsafe_base64

# class


class nlo_acc:
    class name:
        def set(name):
            fer = Fernet(get_device_fingerprint())
            encoded = fer.encrypt(name.encode("utf-8")).decode("utf-8")

            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "acc.json"),
                      "r",
                      encoding="utf-8") as f:
                tex = base64.b85decode(f.read())
                tex = json.loads(tex)

            tex["name"] = encoded

            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "acc.json"),
                      "w",
                      encoding="utf-8") as f:
                tex = base64.b85encode(json.dumps(tex).encode("utf-8")
                                       ).decode("utf-8")
                f.write(tex)

        def get():
            fer = Fernet(get_device_fingerprint())
            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "acc.json"),
                      "r",
                      encoding="utf-8") as f:

                tex = base64.b85decode(f.read())
                tex = json.loads(tex)
            name = tex["name"]
            return fer.decrypt(name.encode("utf-8")).decode("utf-8")

    class password:
        def set(password):
            fer = Fernet(get_device_fingerprint())
            encoded = fer.encrypt(password.encode("utf-8")).decode("utf-8")

            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "acc.json"),
                      "r",
                      encoding="utf-8") as f:
                tex = base64.b85decode(f.read())
                tex = json.loads(tex)

            tex["password"] = encoded

            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "acc.json"),
                      "w",
                      encoding="utf-8") as f:
                tex = base64.b85encode(json.dumps(tex).encode("utf-8")
                                       ).decode("utf-8")
                f.write(tex)

        def get():
            fer = Fernet(get_device_fingerprint())
            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "acc.json"),
                      "r",
                      encoding="utf-8") as f:

                tex = base64.b85decode(f.read())
                tex = json.loads(tex)
            password = tex["password"]
            return fer.decrypt(password.encode("utf-8")).decode("utf-8")


class nlo_api:
    class url:
        def set(url):
            fer = Fernet(get_device_fingerprint())
            encoded = fer.encrypt(url.encode("utf-8")).decode("utf-8")

            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "api.json"),
                      "r",
                      encoding="utf-8") as f:
                tex = base64.b85decode(f.read())
                tex = json.loads(tex)

            tex["url"] = encoded

            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "api.json"),
                      "w",
                      encoding="utf-8") as f:
                tex = base64.b85encode(json.dumps(tex).encode("utf-8")
                                       ).decode("utf-8")
                f.write(tex)

        def get():
            fer = Fernet(get_device_fingerprint())
            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "api.json"),
                      "r",
                      encoding="utf-8") as f:

                tex = base64.b85decode(f.read())
                tex = json.loads(tex)
            key = tex["url"]
            return fer.decrypt(key.encode("utf-8")).decode("utf-8")

    class key:
        def set(key):
            fer = Fernet(get_device_fingerprint())
            encoded = fer.encrypt(key.encode("utf-8")).decode("utf-8")

            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "api.json"),
                      "r",
                      encoding="utf-8") as f:
                tex = base64.b85decode(f.read())
                tex = json.loads(tex)

            tex["key"] = encoded

            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "api.json"),
                      "w",
                      encoding="utf-8") as f:
                tex = base64.b85encode(json.dumps(tex).encode("utf-8")
                                       ).decode("utf-8")
                f.write(tex)

        def get():
            fer = Fernet(get_device_fingerprint())
            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "api.json"),
                      "r",
                      encoding="utf-8") as f:

                tex = base64.b85decode(f.read())
                tex = json.loads(tex)
            key = tex["key"]
            return fer.decrypt(key.encode("utf-8")).decode("utf-8")


class api:
    pass


class request:
    def post(self, _url: str | api, data: dict):
        if _url == api:
            url = nlo_api.url.get()
            data["apikey"] = nlo_api.key.get()
            data["accunt"] = {
                "name": nlo_acc.name.get(),
                "passowrd": nlo_acc.password.get()
            }
        else:
            url = _url

        req = requests.post(url, json.dumps(data))
        return req.content.decode()

    def get(self, url: str):
        req = requests.get(url)
        return req.content.decode()


class LanguagePack:
    def __init__(self, path: str):
        """
        Language pack class.

        Parameters
        ----------
        path: str
            language pack dir
        """
        self.path = path
        self.pack_data = {  # pack data
            "name": None,
            "locale": None,
            "display_locale": None,
            "compatibleAppVersion": None,
            "packVersion": 0
        }

    @staticmethod
    def get_list(path=os.path.join(MODPACK_PATH, "language-pack")):
        """
        get language pack list.

        Paramenters
        -----------
        path: str
            language pack dir
        Returns
        -------
        language_pack_list: list
            language pack
        """
        dirs = []
        for dir2 in os.listdir(path):
            languages = LanguagePack(os.path.join(path, dir2))
            if languages.check():
                dirs.append(languages)
        return dirs

    def load(self) -> None:
        """
        load language pack
        """
        i18n.load_path.append(os.path.join(self.path, "data"))

    def set(self, _language=None):
        language = _language or self.pack_data["locale"][0]
        i18n.set('locale', language)

    def _check_path(self, path):
        if not os.path.isfile(path):
            return False
        if not os.path.isdir(os.path.join(self.path, "data")):
            return False
        return True

    def _check_type(self, decoded_json):
        if type(decoded_json) is not dict:
            return False

        if type(decoded_json["name"]) is not str:  # type check
            return False

        if type(decoded_json["locale"]) is not list:
            return False

        if type(decoded_json["display_locale"]) is not list:
            return False

        if type(decoded_json["compatibleAppVersion"]) is not str:
            return False

        if type(decoded_json["packVersion"]) is not int:
            return False

        if len(decoded_json["locale"]) < 1:
            return False

        if len(decoded_json["display_locale"]) < 1:
            return False

        return True

    def _check_key(self, decoded_json):
        if "name" not in decoded_json:  # key check
            return False
        if "locale" not in decoded_json:
            return False
        if "display_locale" not in decoded_json:
            return False
        if "compatibleAppVersion" not in decoded_json:
            return False
        if "packVersion" not in decoded_json:
            return False
        return True

    def check(self) -> bool:
        """
        Check the language pack.

        Returns
        -------
        check_result : bool
            check result
        """
        main_path = os.path.join(self.path, "pack.json")
        a = self._check_path(main_path)
        if not a:
            return False
        with open(main_path, 'r', encoding='utf-8') as f:
            text = f.read()
        try:
            decoded_json = json.loads(text)
        except json.JSONDecodeError:
            return False
        except BaseException:
            return False

        a = self._check_key(decoded_json)
        if not a:
            return False

        a = self._check_type(decoded_json)
        if not a:
            return False

        if not os.path.isdir(os.path.join(self.path, "data")):
            return False

        pass  # saving pack description
        self.pack_data["name"] = \
            decoded_json["name"]

        self.pack_data["locale"] = \
            decoded_json["locale"]

        self.pack_data["display_locale"] = \
            decoded_json["display_locale"]

        self.pack_data["compatibleAppVersion"] = \
            decoded_json["compatibleAppVersion"]

        self.pack_data["packVersion"] = \
            decoded_json["packVersion"]

        return True


class Page():
    def __init__(self,
                 name: str,
                 frame: QFrame,
                 entable=True,
                 hide=False):
        self.name = name
        self.hide = hide
        self.frame = frame
        self.entable = entable


class Folder():
    def __init__(self, name: str, entable=True, hide=False):
        self.name = name
        self.entable = entable
        self.hide = hide


class QPageber(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setup()
        self.page = []
        self.page2 = {}
        self.file_dict = {}

    def addFolder(self, folder: Folder):
        self.page2[folder] = []
        self.page.append(folder)

    def addPage(self, page: Page, folder: Folder):
        if folder not in self.page2:
            raise PageNotFound(f"{folder} is not fond.")
        self.page2[folder].append(page)

    def setFolder(self, name: Folder):
        self.layout2.setCurrentWidget(self.file_dict[name])

    def setPage(self, name: Page):
        self.page_wid.setCurrentWidget(name.frame)

    def jen(self):
        for i in self.page:
            text = i.name
            if (not i.hide) or i.entable:
                button = QPushButton(text)
                self.layout1.addWidget(button)
                button.setEnabled(i.entable)
                button.clicked.connect(lambda _,
                                       tex=i: self.setFolder(tex))

        for filename, folder in self.page2.items():
            frame = QFrame()
            layouts = QHBoxLayout()
            frame.setLayout(layouts)
            for page in folder:
                text = page.name
                if (not page.hide) or page.entable:
                    button = QPushButton(text)
                    layouts.addWidget(button)
                    button.setEnabled(page.entable)
                    button.clicked.connect(lambda _,
                                           tex=page: self.setPage(tex))
            self.layout2.addWidget(frame)
            self.file_dict[filename] = frame

        for i in self.page2.values():
            for ii in i:
                self.page_wid.addWidget(ii.frame)

        self.setFolder(self.page[0])
        self.setPage(self.page2[self.page[0]][0])

    def setup(self):
        self.layout1 = QHBoxLayout()
        self.addLayout(self.layout1)
        self.layout2 = QStackedWidget()
        self.addWidget(self.layout2)

        self.page_wid = QStackedWidget()
        self.addWidget(self.page_wid, 2)


class LanguageManager:
    def __init__(self):
        pass

    def load_language_pack(self):
        """
        load language pack
        """
        language_path = os.path.join(EXE_PATH,
                                     "data",
                                     "setting",
                                     "Language.json")

        with open(language_path, "r", encoding="utf-8") as f:
            decoded_json = json.load(f)

        languages = LanguagePack.get_list()
        for i in languages:
            if i.pack_data["name"] == decoded_json["name"]:
                i.load()
                i.set(decoded_json["language"])
                return

        for i in languages:
            if i.pack_data["name"] == "default language pack":
                i.load()
                i.set("en")
                return
        return

    def set_language_pack(self, pack: LanguagePack, language=None):
        """
        set language pack

        Paramenters
        -----------
        pack: LanguagePack
            language pack
        language: str
            language
        """
        language_path = os.path.join(EXE_PATH,
                                     "data",
                                     "setting",
                                     "Language.json")

        with open(language_path, "r", encoding="utf-8") as f:
            decoded_json = json.load(f)

        name = pack.pack_data["name"]

        decoded_json["name"] = name
        decoded_json["language"] = language

        with open(language_path, "w", encoding="utf-8") as f:
            json.dump(decoded_json, f, indent=4)


# gui class


class MainWindow(QMainWindow):
    def __init__(self):
        """
        main window
        """
        super().__init__()
        self.main_frame = QFrame()
        self.main_layout = QVBoxLayout(self.main_frame)
        self.main_layout.setSpacing(0)
        self.pages = {}

        self.setCentralWidget(self.main_frame)
        self.page = QPageber()
        self.main_layout.addLayout(self.page)

        self.pages["home"] = Folder(i18n.t("folders.home.title"))
        self.page.addFolder(self.pages["home"])

        self.pages["setting"] = Folder(i18n.t("folders.setting.title"))
        self.page.addFolder(self.pages["setting"])

        self.jen_mainwindow()

        self.jen_sett_news()

        self.page.jen()

    def jen_sett_news(self):
        frame = QFrame()
        layout = QGridLayout()
        frame.setLayout(layout)
        self.page.addPage(Page(i18n.t("folders.setting.pages.general.title"),
                               frame),
                          self.pages["setting"])

    def jen_mainwindow(self):
        frame = QFrame()
        layout = QGridLayout()
        frame.setLayout(layout)
        self.page.addPage(Page(i18n.t("folders.home.pages.home.title"),
                               frame),
                          self.pages["home"])


if __name__ == "__main__":  # start script
    try:
        logger.info("stating")
        if not check_setting_file(EXE_PATH):
            logger.critical("setting file not found")
            raise BaseException(i18n.t("errors.settingnotfound"))

        logger.debug("creating system")
        app = QApplication(sys.argv)
        logger.debug("loading language pack")
        languageManager = LanguageManager()
        languageManager.load_language_pack()

        logger.debug("creating window...")
        window = MainWindow()
        window.show()
        logger.debug("ended!")
        sys.exit(app.exec())
    except SystemExit:
        pass
    except BaseException:

        def clicked(type):
            ret = type.text()
            if ret == "Retry":
                restart()
            sys.exit(1)

        error_text = "error!\n```\n"
        etype, value, tb = sys.exc_info()
        error_text += "".join(traceback.format_exception(etype, value, tb))

        logger.critical("".join(traceback.format_exception(etype, value, tb)))

        error_text += "```\n\nI would be grateful if you could file a bug \
report!"

        logger.debug("creating message...")

        crit = QMessageBox()
        crit.setWindowTitle("ERROR!")
        crit.setText(error_text)
        crit.setIcon(QMessageBox.Critical)
        crit.setStandardButtons(
            QMessageBox.StandardButton.Ok
            | QMessageBox.StandardButton.Retry
        )
        crit.buttonClicked.connect(clicked)
        crit.exec()
