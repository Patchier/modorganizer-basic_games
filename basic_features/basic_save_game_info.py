# -*- encoding: utf-8 -*-

import os
import sys

from typing import Callable, Optional

from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout

import mobase


class BasicGameSaveGame(mobase.ISaveGame):
    def __init__(self, filename):
        super().__init__()
        self._filename = filename

    def getFilename(self):
        return self._filename

    def getCreationTime(self):
        return QDateTime(os.path.getmtime(self._filename))

    def getSaveGroupIdentifier(self):
        return ""

    def allFiles(self):
        return [self._filename]

    def hasScriptExtenderFile(self):
        return False


class BasicGameSaveGameInfoWidget(mobase.ISaveGameInfoWidget):
    def __init__(self, parent: QWidget, get_preview: Callable[[str], str]):
        super().__init__(parent)

        self._get_preview = get_preview

        layout = QVBoxLayout()
        self._label = QLabel()
        palette = self._label.palette()
        palette.setColor(self._label.foregroundRole(), Qt.white)
        self._label.setPalette(palette)
        layout.addWidget(self._label)
        self.setLayout(layout)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.black)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def setSave(self, filename):
        # Resize the label to (0, 0) to hide it:
        self._label.resize(0, 0)

        # Retrieve the pixmap:
        value = self._get_preview(filename)
        if isinstance(value, str):
            pixmap = QPixmap(value)
        elif isinstance(value, QPixmap):
            pixmap = value
        else:
            print(
                "Failed to retrieve the preview, bad return type: {}.".format(
                    type(value)
                ),
                file=sys.stderr,
            )
            return

        # Scale the pixmap and show it:
        pixmap = pixmap.scaledToWidth(320)
        self._label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())


class BasicGameSaveGameInfo(mobase.SaveGameInfo):
    def __init__(self, get_preview: Optional[Callable[[str], str]] = None):
        super().__init__()
        self._get_preview = get_preview

    def getSaveGameInfo(self, filename):
        return BasicGameSaveGame(filename)

    def getMissingAssets(self, filename):
        return {}

    def getSaveGameWidget(self, parent=None):
        if self._get_preview is not None:
            return BasicGameSaveGameInfoWidget(parent, self._get_preview)
        return None

    def hasScriptExtenderSave(self, filename):
        return False
