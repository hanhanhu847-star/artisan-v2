"""运行：安装 PySide6 后 python example.py [风格ID]。"""
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication,QWidget,QVBoxLayout,QLineEdit,QPushButton,QLabel
from PySide6.QtGui import QPixmap
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'ADAPTERS/python'))
from assets import load,find,path_for
app=QApplication(sys.argv);style=sys.argv[1] if len(sys.argv)>1 else 'blueprint'
rows=find(load(),style,'ornaments','png');assert rows,'未知风格'
app.setStyleSheet((Path(__file__).parent/'themes'/(style+'.qss')).read_text(encoding='utf8'))
w=QWidget();w.setWindowTitle('ARTISAN / 图版登记');l=QVBoxLayout(w);symbol=QLabel();symbol.setPixmap(QPixmap(str(path_for(rows[0]))).scaledToWidth(70));l.addWidget(symbol);label=QLabel('图版名称');l.addWidget(label);edit=QLineEdit();label.setBuddy(edit);l.addWidget(edit);b=QPushButton('登记图版');l.addWidget(b);msg=QLabel();l.addWidget(msg)
def save():
    v=edit.text().strip();edit.setProperty('invalid',not v);edit.style().unpolish(edit);edit.style().polish(edit);msg.setText('已登记：'+v if v else '请先填写名称。')
b.clicked.connect(save);w.resize(360,240);w.show();sys.exit(app.exec())
