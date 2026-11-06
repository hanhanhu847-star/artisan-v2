"""PyQt6 示例：与 PySide6 共用 QSS；无需更改源素材。"""
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication,QWidget,QVBoxLayout,QLabel,QPushButton
from PyQt6.QtGui import QPixmap
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'ADAPTERS/python'))
from assets import load,find,path_for
app=QApplication(sys.argv);style=sys.argv[1] if len(sys.argv)>1 else 'dark-academia'
rows=find(load(),style,'ornaments','png');assert rows,'未知风格'
app.setStyleSheet((ROOT/'ADAPTERS/pyside6/themes'/(style+'.qss')).read_text(encoding='utf8'))
w=QWidget();w.setWindowTitle('ARTISAN / 素材样本');l=QVBoxLayout(w);im=QLabel();im.setPixmap(QPixmap(str(path_for(rows[-1]))).scaledToWidth(110));l.addWidget(im);l.addWidget(QLabel(rows[-1]['asset_name']));b=QPushButton('收藏样本');b.setCheckable(True);b.toggled.connect(lambda on:b.setText('已收藏' if on else '收藏样本'));l.addWidget(b);w.resize(320,220);w.show();sys.exit(app.exec())
