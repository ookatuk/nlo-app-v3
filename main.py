import argparse
import json
import os
import subprocess
import sys
import traceback

import i18n
import requests
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
                               QLabel, QMainWindow, QMessageBox, QPushButton,
                               QStackedWidget, QVBoxLayout)

# Erorr list


class PageNotFound(BaseException):
    pass


# constant setting
i18n.set("skip_locale_root_data", True)
i18n.set("file_format", "json")
i18n.set("filename_format", "{locale}.{format}")

EXE_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))

IS_PY = sys.argv[0].split(".")[-1] == "py"

MODPACK_PATH = os.path.join(EXE_PATH, "mod")


# Function


def restart():
    args = [sys.executable] + sys.argv
    subprocess.Popen(args)
    sys.exit()

# class


class request:
    def post(self, url: str, data: dict):
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
        dirs = [LanguagePack(os.path.join(path, f)) for f in os.listdir(path)
                if os.path.isdir(os.path.join(path, f)) and
                LanguagePack(os.path.join(path, f)).check()]
        for i in dirs:
            i.check()
        return dirs

    def load(self) -> None:
        """
        load language pack
        """
        i18n.load_path.append(os.path.join(self.path, "data"))

    def set(self, _language=None):
        if _language is None:
            language = self.pack_data["locale"][0]
        else:
            language = _language
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

        for filename, i in self.page2.items():
            frame = QFrame()
            layouts = QHBoxLayout()
            frame.setLayout(layouts)
            for ii in i:
                text = ii.name
                if (not ii.hide) or ii.entable:
                    button = QPushButton(text)
                    layouts.addWidget(button)
                    button.setEnabled(ii.entable)
                    button.clicked.connect(lambda _,
                                           tex=ii: self.setPage(tex))
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

        self.pages["news"] = Folder(i18n.t("folders.news.title"))
        self.page.addFolder(self.pages["news"])

        self.jen_mainwindow()

        self.jen_news_news()

        self.page.jen()

    def jen_news_news(self):
        frame = QFrame()
        layout = QGridLayout()
        frame.setLayout(layout)
        self.page.addPage(Page(i18n.t("folders.news.pages.news.title"),
                               frame),
                          self.pages["news"])

    def jen_mainwindow(self):
        frame = QFrame()
        layout = QGridLayout()
        frame.setLayout(layout)
        self.page.addPage(Page(i18n.t("folders.home.pages.home.title"),
                               frame),
                          self.pages["home"])


if __name__ == "__main__":  # start script
    try:
        app = QApplication(sys.argv)
        languageManager = LanguageManager()
        languageManager.load_language_pack()
        window = MainWindow()
        window.show()
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

        error_text += "```\n\nI would be grateful if you could file a bug \
report!"

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
