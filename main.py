import sys 
from PyQt5.QtWidgets import QApplication 
from appcontroller import ChangeMode

# Code to converter .ui->.py: pyrcc5 resource.qrc -o resource_rc.py
# Code to converter .ui->.py: pyuic5 bankinterface.ui -o bankinterface.py
# Code to converter .ui->.py: pyuic5 logininterface.ui -o logininterface.py
# Code to converter .ui->.py: pyuic5 signininterface.ui -o signininterface.py

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mode = ChangeMode()
    ctrl = mode.logInApp
    ctrl.show()
    app.exec_() 