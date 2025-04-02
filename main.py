import base64
import hashlib
import json
import os
import platform
from subprocess import Popen
import sys
import traceback
from logging import config, getLogger
import i18n
import psutil
import functools
import requests
from cryptography.fernet import Fernet
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
                               QMainWindow, QMessageBox, QPushButton,
                               QStackedWidget, QVBoxLayout, QLabel, QLineEdit)
from PySide6.QtCore import QTimer
import initer
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem, QTreeWidget
# constant

VERSION = "v3.0.0-closed-test-alpha.2"

RESTART_TIME = 3


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


if __name__ == "__main__":
    initer.check()


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


def version_check(ver):
    ver2_1 = ver[1:6]
    ver1_1 = VERSION[1:6]

    ver2_2 = ver[7:].split(".")[0]
    ver1_2 = VERSION[7:].split(".")[0]

    if int(ver2_1[0]) < int(ver1_1[0]):
        return 1
    if int(ver2_1[0]) > int(ver1_1[0]):
        return -1

    if int(ver2_1[2]) < int(ver1_1[2]):
        return 1
    if int(ver2_1[2]) > int(ver1_1[2]):
        return -1

    if int(ver2_1[4]) < int(ver1_1[4]):
        return 1
    if int(ver2_1[4]) > int(ver1_1[4]):
        return -1

    if "" == ver1_2 and not ("" == ver2_2):
        return 1

    if "" == ver2_2 and not ("" == ver1_2):
        return -1

    if "" == ver2_2 and "" == ver1_2:
        return 0

    ver2_3 = ver[7:].split(".")[1]
    ver1_3 = VERSION[7:].split(".")[1]

    if int(ver2_3) < int(ver1_3):
        return 1

    if int(ver2_3) > int(ver1_3):
        return -1

    if ver1_2 == "closed-test-alpha" and ver2_2 == "public-test-beta":
        return -1

    if ver2_2 == "closed-test-alpha" and ver1_2 == "public-test-beta":
        return 1

    return 0

def check_setting_file(dir):
    """
    check setting file

    Paramenters
    ---------
    dir: str
        application path

    Returns
    -------
    is_ok: bool
        is ok
    """
    if not os.path.isdir(os.path.join(dir, "data")):
        return False
    if not os.path.isdir(os.path.join(dir, "data", "setting")):
        return False

    setting_dir = os.path.join(dir, "data", "setting")

    if not os.path.isfile(os.path.join(setting_dir, "Language.json")):
        return False
    return True


def restart():
    """
    restart app
    """
    mess = QMessageBox()
    mess.setWindowTitle(i18n.t("restarts.restart"))
    mess.setText(i18n.t("restarts.restart_text", time=RESTART_TIME))
    QTimer.singleShot(RESTART_TIME*1000, _restart)
    mess.exec()


def _restart():
    """
    restart app
    """
    args = sys.argv
    Popen(args)
    sys.exit()


def get_device_fingerprint():
    """
    jen encrypt code

    Returns
    -------
    urlsafe_base64: bytes
        encrypt key
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

# base class


class nlo_acc:
    class name:
        def set(name):
            """
            set accunt name

            Paramenters
            -----------
            name: str
                accunt name
            """
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
            """
            get accunt name

            Returns
            -------
            name: str
                nlo accunt name
            """
            fer = Fernet(get_device_fingerprint())
            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "acc.json"),
                      "r",
                      encoding="utf-8") as f:

                tex = base64.b85decode(f.read())
                tex = json.loads(tex)

            if "name" not in tex:
                return ""

            name = tex["name"]
            return fer.decrypt(name.encode("utf-8")).decode("utf-8")

    class password:
        def set(password):
            """
            get nlo accunt password

            Paramenters
            -----------
            password: str
                nlo accunt password
            """
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
            """
            get accunt password

            Returns
            password: str
                nlo accunt password
            """
            fer = Fernet(get_device_fingerprint())
            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "acc.json"),
                      "r",
                      encoding="utf-8") as f:

                tex = base64.b85decode(f.read())
                tex = json.loads(tex)

            if "password" not in tex:
                return ""

            password = tex["password"]
            return fer.decrypt(password.encode("utf-8")).decode("utf-8")


class nlo_api:
    class url:
        def set(url):
            """
            set nlo api url

            Paramenters
            -----------
            url: str
                nlo api url
            """
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
            """
            get nlo api url

            Returns
            -------
            url: str
                nlo api url
            """
            fer = Fernet(get_device_fingerprint())
            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "api.json"),
                      "r",
                      encoding="utf-8") as f:

                tex = base64.b85decode(f.read())
                tex = json.loads(tex)

            if "url" not in tex:
                return ""

            key = tex["url"]
            return fer.decrypt(key.encode("utf-8")).decode("utf-8")

    class key:
        def set(key):
            """
            get nlo api key

            Paramenters
            -----------
            key: str
                api key
            """
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
            """
            get nlo api key

            Returns
            -------
            key: str
                api key
            """
            fer = Fernet(get_device_fingerprint())
            with open(os.path.join(EXE_PATH,
                                   "data",
                                   "setting",
                                   "api.json"),
                      "r",
                      encoding="utf-8") as f:

                tex = base64.b85decode(f.read())
                tex = json.loads(tex)

            if "key" not in tex:
                return ""

            key = tex["key"]
            return fer.decrypt(key.encode("utf-8")).decode("utf-8")


class api:
    pass


class request:
    def post(self, _url: str | api, data: dict):
        """
        send post method

        Paramenters
        -----------
        _url: str | api
            url
        data: dict
            post data

        Returns
        -------
        content: str
            decoded content data
        """
        if _url == api:
            url = nlo_api.url.get()
            data["apikey"] = nlo_api.key.get()
            data["accunt"] = {
                "name": nlo_acc.name.get(),
                "passowrd": nlo_acc.password.get()
            }
        else:
            url = _url

        try:
            req = requests.post(url, json.dumps(data))
            return req.content.decode()
        except requests.exceptions.RequestException:
            pass

    def get(self, url: str):
        """
        send get method

        Paramenters
        -----------
        _url: str | api
            url

        Returns
        -------
        content: str
            decoded content data
        """
        try:
            req = requests.get(url)
            return req.content.decode()
        except requests.exceptions.RequestException:
            pass


# main class


class LanguagePack:
    def __init__(self, path: str):
        """
        Language pack class.

        paramenters
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
    @functools.cache
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
        dirs = tuple()
        for dir2 in os.listdir(path):
            languages = LanguagePack(os.path.join(path, dir2))
            if languages.check():
                dirs = dirs + (languages,)
        return dirs

    def load(self) -> None:
        """
        load language pack
        """
        i18n.load_path.append(os.path.join(self.path, "language"))

    def display_locale_to_locale(self, display_locale):
        return self.pack_data["locale"][self.pack_data["display_locale"].index(display_locale)]

    def set(self, _language=None):
        """
        set language

        Paramenters
        -----------
        _language: str
            language
        """
        language = _language or self.pack_data["locale"][0]
        i18n.set('locale', language)

    def _check_path(self, path):
        """
        check path

        Paramenters
        -----------
        path: str
            language pack path

        Returns
        -------
        is_ok: bool
            is ok
        """
        if not os.path.isfile(path):
            return False
        if not os.path.isdir(os.path.join(self.path, "language")):
            return False

        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
                dex = json.loads(text)
                locale = dex["locale"]
                for i in locale:
                    a = os.path.join(self.path, "language", i+".json")
                    with open(a, "r", encoding="utf-8") as f:
                        text = json.load(f)
                        if type(text) is not dict:
                            return False
        except json.JSONDecodeError:
            return False
        except UnicodeDecodeError:
            return False
        except FileNotFoundError:
            return False
        return True

    def _check_type(self, decoded_json):
        """
        check json

        Paramenters
        -----------
        decoded_json: dict
            decoded pack.json

        Returns
        -------
        is_ok: bool
            is ok
        """
        if type(decoded_json) is not dict:
            return False

        if type(decoded_json["name"]) is not str:  # type check
            return False

        if type(decoded_json["locale"]) is not list:
            return False

        if type(decoded_json["display_locale"]) is not list:
            return False

        if type(decoded_json["compatibleAppVersion"]) is not list:
            return False

        if type(decoded_json["packVersion"]) is not list:
            return False

        if len(decoded_json["locale"]) < 1:
            return False

        if len(decoded_json["compatibleAppVersion"]) < 1:
            return False

        if len(decoded_json["packVersion"]) < 1:
            return False

        if len(decoded_json["display_locale"]) < 1:
            return False

        if not(len(decoded_json["locale"]) == \
                len(decoded_json["compatibleAppVersion"]) == \
                len(decoded_json["packVersion"]) == \
                len(decoded_json["display_locale"])):
            return False

        return True

    def _check_key(self, decoded_json):
        """
        check json

        Paramenters
        -----------
        decoded_json: dict
            decoded pack.json

        Returns
        -------
        is_ok: bool
            is ok
        """
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
        check pack

        Paramenters
        -----------
        decoded_json: dict
            decoded pack.json

        Returns
        -------
        is_ok: bool
            is ok
        """
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

        if not os.path.isdir(os.path.join(self.path, "language")):
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
        """
        page

        Paramenters
        -----------
        name: str
            page name
        frame: QFrame
            Pyside Frame
        entable: bool
            is entable
        hide: bool
            is seecret
        """
        self.name = name
        self.hide = hide
        self.frame = frame
        self.entable = entable


class Folder():
    def __init__(self, name: str, entable=True, hide=False):
        """
        Folder

        Paramenters
        -----------
        name: str
            folder name
        entable: bool
            is entable
        hide: bool
            is secret
        """
        self.name = name
        self.entable = entable
        self.hide = hide


class QPageber(QVBoxLayout):
    def __init__(self):
        """
        page bar
        """
        super().__init__()
        self.setup()
        self.page = []
        self.page2 = {}
        self.file_dict = {}

    def addFolder(self, folder: Folder):
        """
        add folder

        Paramenters
        -----------
        folder: Folder
            folder
        """
        self.page2[folder] = []
        self.page.append(folder)

    def addPage(self, page: Page, folder: Folder):
        """
        add page

        Paramenters
        -----------
        page: Page
            page
        folder: Folder
            folder
        """
        if folder not in self.page2:
            raise PageNotFound(f"{folder} is not fond.")
        self.page2[folder].append(page)

    def setFolder(self, name: Folder):
        """
        set Folder

        Paramenters
        -----------
        folder: Folder
            dolder
        """
        self.layout2.setCurrentWidget(self.file_dict[name])

    def setPage(self, name: Page):
        """
        set page

        Paramenters
        -----------
        name: Page
            Page

        """
        self.page_wid.setCurrentWidget(name.frame)

    def jen(self):
        """
        jenelate page bar
        """
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
        """
        setup page bar

        """
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

        self.jen_sett_acc_setting()
        self.jen_sett_lang_setting()

        self.page.jen()

    def acc_setting_clicked_lang(self):
        is_child = self.sett_lang_tree.selectedItems()[0].childCount() == 0
        if not is_child:
            self.sett_lang_tree.selectedItems()[0].setSelected(False)

    def acc_setticg_dec_lang(self):
        selected = self.sett_lang_tree.selectedItems()[0]

        if not (selected.childCount() == 0):
            return
        lang = selected.text(0)
        packname = selected.parent().text(0)
        for pack in LanguagePack.get_list():
            if pack.pack_data["name"] == packname:
                lang = pack.display_locale_to_locale(lang)

                languageManager.set_language_pack(pack, lang)
                restart()

    def jen_sett_lang_setting(self):
        """
        jenelate setting-language window
        """
        frame = QFrame()
        layout = QGridLayout()
        frame.setLayout(layout)
        self.page.addPage(Page(i18n.t("folders.setting.pages.language.title"),
                               frame),
                          self.pages["setting"])
        lang_list = list(LanguagePack.get_list())
        treeWidget = QTreeWidget()
        self.sett_lang_tree = treeWidget
        layout.addWidget(treeWidget, 0, 0, 1, 0)
        treeWidget.setColumnCount(len(lang_list))
        treeWidget.itemClicked.connect(self.acc_setting_clicked_lang)
        treeWidget.setHeaderLabels(
            [
                i18n.t("folders.setting.pages.language.name")+"/"+i18n.t("folders.setting.pages.language.locale"),
                i18n.t("folders.setting.pages.language.packversion"),
                i18n.t("folders.setting.pages.language.version"),
                i18n.t("folders.setting.pages.language.caveat")
            ]
            )
        for i in lang_list:
            root = QTreeWidgetItem()
            treeWidget.addTopLevelItem(root)
            root.setText(0, i.pack_data["name"])
            loop = -1
            for lang in i.pack_data["display_locale"]:
                loop += 1
                langs = QTreeWidgetItem()
                root.addChild(langs)

                language_path = os.path.join(EXE_PATH,
                                            "data",
                                            "setting",
                                            "Language.json")
                with open(language_path, "r", encoding="utf-8") as f:
                    decoded_json = json.load(f)

                langs.setText(0, lang)
                langs.setText(1, str(i.pack_data["packVersion"][loop]))
                langs.setText(2, i.pack_data["compatibleAppVersion"][loop])
                langs.setText(3, i18n.t("folders.setting.pages.language.warn.none"))
                try:
                    ret = version_check(i.pack_data["compatibleAppVersion"][loop])
                    if ret == -1:
                        langs.setBackground(2, Qt.GlobalColor.yellow)
                        langs.setText(3, i18n.t("folders.setting.pages.language.warn.ver+"))
                    elif ret == 1:
                        langs.setBackground(2, Qt.GlobalColor.red)
                        langs.setText(3, i18n.t("folders.setting.pages.language.warn.ver-"))
                except ValueError:
                    langs.setBackground(2, Qt.GlobalColor.red)
                    langs.setText(3, i18n.t("folders.setting.pages.language.warn.error"))

                if decoded_json["name"] == i.pack_data["name"] and decoded_json["language"] == i.pack_data["locale"][loop]:
                    langs.setSelected(True)

        self.acc_setting_lang_dec_button = QPushButton(
            i18n.t("folders.setting.Decision")
        )

        self.acc_setting_lang_dec_button.clicked.connect(self.acc_setticg_dec_lang)

        layout.addWidget(
            self.acc_setting_lang_dec_button,
            1,1
        )

    def jen_sett_acc_setting(self):
        """
        jenelate setting-accunt window
        """
        frame = QFrame()
        layout = QGridLayout()
        frame.setLayout(layout)
        self.page.addPage(Page(i18n.t("folders.setting.pages.accunt.title"),
                               frame),
                          self.pages["setting"])
        self.jen_sett_acc_setting_acc(layout)
        self.jen_sett_acc_setting_api(layout)

    def jen_sett_acc_setting_api(self, layout):
        """
        jenelate setting-accunt-api wid
        """
        layout.addWidget(
            QLabel(i18n.t("folders.setting.pages.accunt.api")),
                4, 0
        )
        layout.addWidget(
            QLabel(i18n.t("folders.setting.pages.accunt.input_api")),
            5,
            1
        )

        self.acc_setting_inputapi = QLineEdit(nlo_api.url.get())

        layout.addWidget(
            self.acc_setting_inputapi,
            5, 2
        )

        layout.addWidget(
            QLabel(i18n.t("folders.setting.pages.accunt.input_apikey")),
            6,
            1
        )

        self.acc_setting_inputkey = QLineEdit(nlo_api.key.get())

        layout.addWidget(
            self.acc_setting_inputkey,
            6, 2
        )

        self.acc_setting_api_dec_button = QPushButton(
            i18n.t("folders.setting.Decision")
        )

        self.acc_setting_api_dec_button.clicked.connect(self.acc_setting_api_dec_clicked)

        layout.addWidget(
            self.acc_setting_api_dec_button,
            7,1
        )

    def acc_setting_api_dec_clicked(self):
        """
        click event
        """
        url = self.acc_setting_inputapi.text()
        key = self.acc_setting_inputkey.text()
        if key == nlo_api.key.get() and url == nlo_api.url.get():
            return
        nlo_api.url.set(url)
        nlo_api.key.set(key)
        restart()

    def jen_sett_acc_setting_acc(self, layout):
        """
        jenelate setting-accunt-accunt wid
        """
        layout.addWidget(
            QLabel(i18n.t("folders.setting.pages.accunt.accunt")),
                0, 0
        )

        layout.addWidget(
            QLabel(i18n.t("folders.setting.pages.accunt.input_accunt_name")),
            1,
            1
        )

        self.acc_setting_inputacc = QLineEdit(nlo_acc.name.get())

        layout.addWidget(
            self.acc_setting_inputacc,
            1,2
        )

        layout.addWidget(
            QLabel(i18n.t("folders.setting.pages.accunt.input_accunt_password")),
            2,
            1
        )

        self.acc_setting_inputpas = QLineEdit(nlo_acc.password.get())

        layout.addWidget(
            self.acc_setting_inputpas,
            2,2
        )

        self.acc_setting_acc_dec_button = QPushButton(
            i18n.t("folders.setting.Decision")
        )

        self.acc_setting_acc_dec_button.clicked.connect(self.acc_setting_acc_dec_clicked)

        layout.addWidget(
            self.acc_setting_acc_dec_button,
            3,1
        )

    def acc_setting_acc_dec_clicked(self):
        """
        clicked event
        """
        name = self.acc_setting_inputacc.text()
        passs = self.acc_setting_inputpas.text()
        if name == nlo_acc.name.get() and passs == nlo_acc.password.get():
            return
        nlo_acc.name.set(name)
        nlo_acc.password.set(passs)
        restart()

    def jen_mainwindow(self):
        """
        jenelate main window
        """
        frame = QFrame()
        layout = QGridLayout()
        frame.setLayout(layout)
        self.page.addPage(Page(i18n.t("folders.home.pages.home.title"),
                               frame),
                          self.pages["home"])


if __name__ == "__main__":  # start script
    try:
        logger.info("initing...")

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
