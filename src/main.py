import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout 

from Gui.playback_controls import ControlsWidget

app = QApplication()
window = QWidget()

# This just for the titel and the icon for the app it self. 
window.setWindowTitle("Kora")
window.resize(1100, 650)
window.setMinimumSize(600, 400)
my_icon = QIcon()
my_icon.addFile("images//kora.png")
window.setWindowIcon(my_icon)

main_layout = QVBoxLayout()    
controls_layout = ControlsWidget() 

main_layout.addStretch()           
main_layout.addWidget(controls_layout)

window.setLayout(main_layout)

window.show()
app.exec()