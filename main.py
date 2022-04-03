import sys
import os, shutil
from datetime import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


def human_read_format(size):
    units = ['B', 'KB', 'MB', 'GB']
    unit_i = 0
    while size >= 1024:
        size /= 1024
        size = round(size)
        unit_i += 1
    return f'{size}{units[unit_i]}'


def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        curdir = os.path.abspath(os.curdir)
        self.source.setText(curdir)
        self.dest.setText('/'.join(curdir.split('/')[:-1]))
        w = human_read_format(get_dir_size(self.source.text()))
        self.weight.setText('weight: >=' + str(w))
        self.source_view_btn.clicked.connect(self.source_view)
        self.dest_view_btn.clicked.connect(self.dest_view)
        self.copy_btn.clicked.connect(self.copy)

    def source_view(self):
        my_dir = QFileDialog.getExistingDirectory(
            self,
            "Choose a folder", self.source.text(),
            QFileDialog.ShowDirsOnly
        )
        self.source.setText(my_dir)
        w = human_read_format(get_dir_size(self.source.text()))
        self.weight.setText('weight: >=' + str(w))

    def dest_view(self):
        my_dir = QFileDialog.getExistingDirectory(
            self,
            "Choose a folder", self.dest.text(),
            QFileDialog.ShowDirsOnly
        )
        self.dest.setText(my_dir)

    def copy(self):
        s = self.source.text()
        dirname = s.split('/')[-1]
        d = self.dest.text()
        today = datetime.now()
        d += f"/{dirname}-copy {today.strftime('%Y%m%d')} {str(today.hour).rjust(2, '0')}:{str(today.minute).rjust(2, '0')}:{str(today.second).rjust(2, '0')}"
        os.mkdir(d)
        print(d)
        copytree(s, d)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
