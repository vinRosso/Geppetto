import maya.cmds as mc
from maya import OpenMayaUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import os, sys
import importlib as imp
from shiboken2 import wrapInstance
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from .utils import toolbox as tb

imp.reload(tb)
 


def get_maya_win():
    """
    Get current Maya QT main window
    
    Returns:
        QMainWindow: current Maya main window
    """    
    win_ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(win_ptr), QMainWindow)


def delete_workspace_control(control):
    """
    Delete given workspace control if exists.

    Args:
        control (str): control to delete
    """
    if mc.workspaceControl(control, q=True, exists=True):
        mc.workspaceControl(control, e=True, close=True)
        mc.deleteUI(control, control=True)
    return


def getScreenRatio():
    dpi = QDesktopWidget().logicalDpiX()
    
    return dpi/144


class Workshop(MayaQWidgetDockableMixin, QMainWindow):
    TOOL_NAME = 'Geppetto'
    _menuBar = None
    _mainWidget = None

    def __init__(self, parent=None):
        # DELETE WINDOW IF ALREADY EXISTS
        delete_workspace_control(self.TOOL_NAME + 'WorkspaceControl')

        # INITIALIZE AND SET PARENT
        super(self.__class__, self).__init__(parent=parent)
        self.mayaMainWindow = get_maya_win()
        self.setObjectName(self.__class__.TOOL_NAME)

        # WINDOW SETTINGS
        self.ratio = getScreenRatio()
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(self.TOOL_NAME)
        self.resize(700*self.ratio, 1000*self.ratio)
                
        return
    
    
    def start(self):
        self._mainWidget = QWidget()
        self.setCentralWidget(self._mainWidget)
        self._mainWidget.setStyleSheet('''
                                       QLineEdit {
                                           border-radius: 5px;
                                           }
                                       QLineEdit:focus {
                                           border: 1 solid white;
                                           }
                                       ''')
        
        if not tb.geppettoExists():
            # IF GEPPETTO DOESN'T EXISTS, CREATE START UI
            self._buildStartUI()
        else:
            # ELSE BUILD STANDARD UI
            self._buildUI()
        
        # SHOW WINDOW AND SET DOCKABLE
        super(self.__class__, self).show(dockable=True)
        
        return
    
        
    '''                '''
    ''' USER INTERFACE '''
    '''                '''

    def _buildStartUI(self):
        # REMOVE MENUBAR
        if self._menuBar:
            self.setMenuBar(QMenuBar())
            self._menuBar = None
            
        mainLayout = QHBoxLayout()
        
        newBtn = QPushButton("New")
        openBtn = QPushButton("Open")
        
        mainLayout.addStretch(1)
        mainLayout.addWidget(newBtn)
        mainLayout.addWidget(openBtn)
        mainLayout.addStretch(1)
        self._mainWidget.setLayout(mainLayout)
        
        newBtn.clicked.connect(self.createNewSession)
        
        return

    def _buildUI(self):
        # modules = tb.get_modules()
        # for module in modules:
        #     button = QPushButton(module)
        #     button.clicked.connect(mc.polyCube)
        #     self.layout().addWidget(button)
            
        # CREATE MENU BAR
        self._createMenuBar()
        
        # TOP LAYOUT
        topLayout = QHBoxLayout()
        testBtn = QPushButton("test")
        topLayout.addWidget(testBtn)
        
        # BOTTOM TAB LAYOUT
        tabWidget = QTabWidget()
        tabWidget.setStyleSheet("QTabWidget#tabWidget{ border: 0px;}")
        # build modules tab
        self._buildModulesTab(tabWidget)
        # build blueprints tabs
        for bp in ["bp1", "bp2"]:
            self._buildBlueprintTab(tabWidget, bp)
        
        # CREATE MAIN LAYOUT
        mainLayout = QGridLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addLayout(topLayout, 0, 0, 2, 2)
        mainLayout.addWidget(tabWidget, 1, 0, 2, 2)
        mainLayout.setRowStretch(0, 1)
        mainLayout.setRowStretch(1, 10)
        self._mainWidget.setLayout(mainLayout)
        
        return

    def _buildModulesTab(self, parent):
        # WIDGET and MAIN LAYOUT
        moduleTab = QWidget()
        parent.addTab(moduleTab, "Modules")
        
        # MAIN LAYOUT
        mainLayout = QHBoxLayout()
        moduleTab.setLayout(mainLayout)
        
        ''' LEFT COLUMN '''
        leftLayout = QVBoxLayout()
        mainLayout.addLayout(leftLayout)
        
        # SAVE GUIDES LAYOUT
        leftTopLayout = QHBoxLayout()
        leftLayout.addLayout(leftTopLayout)
        # save guides button
        savePoseBtn = QPushButton("save")
        leftTopLayout.addWidget(savePoseBtn)
        leftTopLayout.addStretch(1)
        # blueprint override combo
        blueprintGuides = QComboBox()
        leftTopLayout.addWidget(blueprintGuides)
        
        # MODULES FRAME
        modulesFrame = QFrame()
        modulesFrame.setStyleSheet('''
                                   QFrame{ background-color: #373737;
                                           border-radius: 5px;}
                                   QPushButton{ border-radius: 5px; background-color: #EEF4F9; color: #373737; }
                                   QPushButton:hover{ background-color: #BCC0C4; }
                                   ''')
        leftLayout.addWidget(modulesFrame)
        # modules layout
        modulesLayout = QVBoxLayout()
        modulesFrame.setLayout(modulesLayout)
        # modules list
        modulesList = QListView()
        self.model = ModulesListModel()
        modulesList.setModel(self.model)
        modulesList.setStyleSheet("QListView{ border: 0px;}")
        modulesLayout.addWidget(modulesList)
        self._modulesList = modulesList
        # for module in tb.getModules():
        #     self._addModule(module)
        # modules stretch
        modulesLayout.addStretch(1)
        
        # JOINT SIZE SLIDER
        jointSlider = QSlider(Qt.Horizontal)
        jointSlider.setValue(50)
        jointSlider.setStyleSheet('''
                                  QSlider::groove:horizontal { 
                                      background-color: #444444;
                                      border: 0px solid #424242; 
                                      height: '''+str(5*self.ratio)+'''px; 
                                      border-radius: '''+str(4*self.ratio)+'''px;
                                  }  
                                  QSlider::handle:horizontal { 
                                      background-color: white; 
                                      border: 0px solid white; 
                                      width: '''+str(15*self.ratio)+'''px; 
                                      height: '''+str(15*self.ratio)+'''px; 
                                      line-height: '''+str(16*self.ratio)+'''px; 
                                      margin-top: '''+str(-5*self.ratio)+'''px; 
                                      margin-bottom: '''+str(-5*self.ratio)+'''px; 
                                      border-radius: '''+str(7*self.ratio)+'''px; 
                                  }
                                  ''')
        modulesLayout.addWidget(jointSlider)
        
        # ADD MODULES BUTTON
        addModuleBtn = QPushButton("+")
        addModuleBtn.setStyleSheet('''
                                   QPushButton{
                                       background-color: #51C080;
                                       border-radius: 5px;
                                       font-weight: bold;
                                       font-size: 24px;
                                       color: white;
                                       }
                                   QPushButton:hover{
                                       background-color: #6FCF97;
                                       }
                                   ''')
        addModuleBtn.setMinimumHeight(35*self.ratio)
        modulesLayout.addWidget(addModuleBtn)
        
        # RIG GUIDES BUTTONS
        bottomLeftLayout = QGridLayout()
        bottomLeftLayout.setContentsMargins(0, 5, 0, 0)
        modulesLayout.addLayout(bottomLeftLayout)
        # mirror modules button
        mirrorModulesBtn = QPushButton("mirror")
        mirrorModulesBtn.setMinimumHeight(58*self.ratio)
        mirrorModulesBtn.setMinimumWidth(58*self.ratio)
        bottomLeftLayout.addWidget(mirrorModulesBtn, 0, 0)
        # build rig guides button
        buildGuidesBtn = QPushButton("build guides")
        buildGuidesBtn.setMinimumHeight(58*self.ratio)
        bottomLeftLayout.addWidget(buildGuidesBtn, 0, 1)
        # show rig guides button
        showGuidesBtn = QPushButton("show")
        showGuidesBtn.setMinimumHeight(58*self.ratio)
        showGuidesBtn.setMinimumWidth(58*self.ratio)
        bottomLeftLayout.addWidget(showGuidesBtn, 0, 2)
        # set layout stretch
        bottomLeftLayout.setColumnStretch(0, 1)
        bottomLeftLayout.setColumnStretch(1, 7)
        bottomLeftLayout.setColumnStretch(2, 1)
        
        ''' RIGHT COLUMN '''
        rightLayout = QVBoxLayout()
        rightLayout.setMargin(10)
        mainLayout.addLayout(rightLayout)
        
        # MODULE IMAGE
        moduleImage = ImageWidget("blank_w.svg", 50*self.ratio, 50*self.ratio)
        rightLayout.addWidget(moduleImage)
        
        # MODULE NAME
        moduleNameLayout = QHBoxLayout()
        moduleNameLayout.setContentsMargins(0, 10, 0, 0)
        rightLayout.addLayout(moduleNameLayout)
        moduleNameLayout.addStretch(1)
        # module side
        moduleSide = SideButton("-")
        moduleNameLayout.addWidget(moduleSide)
        # module name
        moduleName = QLineEdit("leg")
        moduleName.setMinimumWidth(250*self.ratio)
        moduleName.setMinimumHeight(20*self.ratio)
        moduleName.setTextMargins(5, 0, 0, 2)
        moduleNameLayout.addWidget(moduleName)
        moduleNameLayout.addStretch(1)
        
        # SETTINGS LAYOUT
        centerLayout = QHBoxLayout()
        centerLayout.addStretch(1)
        maxWidth = QWidget()
        maxWidth.setFixedWidth(400*self.ratio)
        settingsLayout = QVBoxLayout()
        maxWidth.setLayout(settingsLayout)
        centerLayout.addWidget(maxWidth)
        centerLayout.addStretch(1)
        rightLayout.addLayout(centerLayout)
        
        # CONNECT TO
        # label
        connectLabel = QLabel("Connect to")
        connectLabel.setAlignment(Qt.AlignVCenter)
        connectLabel.setStyleSheet('''
                                   QLabel{
                                       color: white;
                                       font-weight: bold;
                                       border-bottom: 1px solid white;
                                   }
                                   ''')
        connectLabel.setContentsMargins(0, 30, 0, 0)
        settingsLayout.addWidget(connectLabel)
        # line
        line = QFrame()
        line.setFixedSize(150*self.ratio, 2)
        line.setStyleSheet("background-color: white;")
        settingsLayout.addWidget(line)
        horizontalLayout = QHBoxLayout()
        settingsLayout.addLayout(horizontalLayout)
        # modules combo
        connectModuleCombo = QComboBox()
        horizontalLayout.addWidget(blueprintGuides)
        horizontalLayout.addStretch(1)
        # ctrl jnt switch
        ctrlJntSwitch = SwitchButton("JNT", "CTRL", 50, 12)
        horizontalLayout.addWidget(ctrlJntSwitch)
        # object combo
        connectObjectCombo = QComboBox()
        settingsLayout.addWidget(connectObjectCombo)
        
        # SETTINGS
        # label
        settingsLabel = QLabel("Settings")
        settingsLabel.setAlignment(Qt.AlignVCenter)
        settingsLabel.setStyleSheet('''
                                   QLabel{
                                       color: white;
                                       font-weight: bold;
                                       border-bottom: 1px solid white;
                                   }
                                   ''')
        settingsLabel.setContentsMargins(0, 30, 0, 0)
        settingsLayout.addWidget(settingsLabel)
        # line
        line = QFrame()
        line.setFixedSize(150*self.ratio, 2)
        line.setStyleSheet("background-color: white;")
        settingsLayout.addWidget(line)
        # scroll layout
        scrollArea = QScrollArea()
        scrollArea.setStyleSheet('''QScrollArea{
                                        border: 0;
                                    }''')
        scrollArea.setWidgetResizable(True)
        scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        scrollWidget = QWidget()
        scrollArea.setWidget(scrollWidget)
        scrollLayout = QVBoxLayout()
        scrollLayout.setContentsMargins(0, 0, 5, 0)
        scrollLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        scrollWidget.setLayout(scrollLayout)
        settingsLayout.addWidget(scrollArea)
        
        for i in range(10):
            scrollLayout.addWidget(QPushButton(str(i)))
        
        
        # BUILD MODULE BUTTON
        buildModuleBtn = QPushButton("Build Module")
        buildModuleBtn.setMinimumHeight(58*self.ratio)
        settingsLayout.addWidget(buildModuleBtn)
        
        return

    def _buildBlueprintTab(self, parent, bpName):
        # WIDGET
        blueprintTab = QWidget()
        parent.addTab(blueprintTab, bpName)
        
        # MAIN LAYOUT
        mainLayout = QVBoxLayout()
        blueprintTab.setLayout(mainLayout)
        
        # NAME BAR
        
        # BLUEPRINT NAME AND TYPE
        nameLayout = QHBoxLayout()
        nameLayout.setContentsMargins(0, 15, 0, 15)
        mainLayout.addLayout(nameLayout)
        nameLayout.addStretch(1)
        # bp type
        bpImage = ImageWidget("blank_w.svg", 32*self.ratio, 32*self.ratio)
        nameLayout.addWidget(bpImage)
        # bp name
        bpNameTxt = QLineEdit(bpName)
        bpNameTxt.setMinimumWidth(250*self.ratio)
        bpNameTxt.setMinimumHeight(30*self.ratio)
        bpNameTxt.setTextMargins(5, 0, 0, 2)
        nameLayout.addWidget(bpNameTxt)
        nameLayout.addStretch(1)
        
        # scroll layout
        scrollArea = QScrollArea()
        scrollArea.setStyleSheet('''QScrollArea{
                                        border: 0;
                                    }''')
        scrollArea.setWidgetResizable(True)
        scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        scrollWidget = DragWidget(orientation=Qt.Orientation.Vertical)
        # scrollWidget.setStyleSheet('''
        #                            DragWidget {
        #                                background-color: rgb(255, 0, 0);
        #                                }''')
        scrollArea.setWidget(scrollWidget)
        scrollLayout = QVBoxLayout()
        scrollLayout.setContentsMargins(5, 0, 5, 0)
        scrollLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        # scrollWidget.setLayout(scrollLayout)
        mainLayout.addWidget(scrollArea)
        
        for i in range(10):
            item = DragItem(str(i))
            item.set_data(i)  # Store the data.
            scrollWidget.add_item(item)
        
        
        # BUILD MODULE BUTTON
        buildModuleBtn = QPushButton("Build Puppet")
        buildModuleBtn.setMinimumHeight(58*self.ratio)
        mainLayout.addWidget(buildModuleBtn)
        
        return

    def _addModule(self, module):
        self.model.appendRow(ModuleWidget(module))
        return

    def _createMenuBar(self):
        # CREATE MENU BAR
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)
        
        # CREATE MENU ITEMS
        fileMenu = menuBar.addMenu("&File")
        moduleMenu = menuBar.addMenu("&Module")
        blueprintMenu = menuBar.addMenu("&Blueprint")
        helpMenu = menuBar.addMenu("&Help")
        
        # File
        newAction = fileMenu.addAction("&New")
        openAction = fileMenu.addAction("&Open")
        fileMenu.addSeparator()
        saveAction = fileMenu.addAction("&Save")
        saveAsAction = fileMenu.addAction("Save &As")
        fileMenu.addSeparator()
        replacePathAction = fileMenu.addAction("Replace &Path")
        resetAction = fileMenu.addAction("&Reset")
        
        # Module
        addModuleAction = moduleMenu.addAction("&Add")
        deleteModuleAction = moduleMenu.addAction("&Delete")
        moduleMenu.addSeparator()
        duplicateModuleAction = moduleMenu.addAction("&Duplicate")
        moduleMenu.addSeparator()
        renameModuleAction = moduleMenu.addAction("Re&name")
        reinitializeModuleAction = moduleMenu.addAction("&Reinitialize")
        
        # Blueprint
        addBpAction = blueprintMenu.addAction("&Add")
        deleteBpAction = blueprintMenu.addAction("&Delete")
        blueprintMenu.addSeparator()
        duplicateBpAction = blueprintMenu.addAction("Du&plicate")
        instanciateBpAction = blueprintMenu.addAction("In&stanciate")
        blueprintMenu.addSeparator()
        importBpAction = blueprintMenu.addAction("&Import")
        exportBpAction = blueprintMenu.addAction("&Export")
        blueprintMenu.addSeparator()
        renameBpAction = blueprintMenu.addAction("Re&name")
        
        # Help
        docsAction = helpMenu.addAction("&Documentation")
        aboutAction = helpMenu.addAction("&About")
        
        # # CONNECT FUNCTIONS
        # newAction.triggered.connect(tb.newSession)
        # openAction.triggered.connect(tb.openSession)
        # saveAction.triggered.connect(tb.saveSession)
        # saveAsAction.triggered.connect(tb.saveSessionAs)
        # replacePathAction.triggered.connect(tb.replaceSessionPaths)
        resetAction.triggered.connect(self.start)
        
        # addModuleAction.triggered.connect(tb.addModule)
        # deleteModuleAction.triggered.connect(tb.deleteModule)
        # duplicateModuleAction.triggered.connect(tb.duplicateModule)
        # renameModuleAction.triggered.connect(tb.renameModule)
        # reinitializeModuleAction.triggered.connect(tb.reinitializeModule)
        
        # addBpAction.triggered.connect(tb.addBlueprint)
        # deleteBpAction.triggered.connect(tb.deleteBlueprint)
        # duplicateBpAction.triggered.connect(tb.duplicateBlueprint)
        # instanciateBpAction.triggered.connect(tb.instanceBlueprint)
        # importBpAction.triggered.connect(tb.importBlueprint)
        # exportBpAction.triggered.connect(tb.exportBlueprint)
        # renameBpAction.triggered.connect(tb.renameBlueprint)
        
        # docsAction.triggered.connect(tb.openDocumentation)
        # aboutAction.triggered.connect(tb.aboutWindow)
        
        self._menuBar = menuBar
        
        return

    def createNewSession(self):
        tb.createBaseStructure()
        self.start()
        
        return

class ModulesListModel(QAbstractListModel):
    def __init__(self, data=[], parent=None):
        super().__init__(parent)
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()]

        if role == Qt.UserRole:
            # Return a custom widget instance for the item
            widget = ModuleWidget(self._data[index.row()])
            return widget

        return None

    def appendRow(self, data, parent=QModelIndex()):
        row = len(self._data)-1
        self.beginInsertRows(parent, row, row)
        self._data.insert(row, data)
        self.endInsertRows()
        return True

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in range(count):
            self._data.pop(row)
        self.endRemoveRows()
        return True

    def moveRows(self, sourceParent, sourceRow, count, destinationParent, destinationChild):
        self.beginMoveRows(sourceParent, sourceRow, sourceRow + count - 1, destinationParent, destinationChild)
        items = self._data[sourceRow:sourceRow + count]
        del self._data[sourceRow:sourceRow + count]
        self._data[destinationChild:destinationChild] = items
        self.endMoveRows()
        return True


class ModuleWidget(QWidget):
    def __init__(self, name, parent=None):
        super(self.__class__, self).__init__(parent)

        self.row = QHBoxLayout()

        self.row.addWidget(QLabel(name))
        self.row.addWidget(QPushButton("view"))
        self.row.addWidget(QPushButton("select"))

        self.setLayout(self.row)


class SideButton(QPushButton):
    def __init__(self, side, parent=None):
        super().__init__(parent)
        self.ratio = getScreenRatio()
        self.setFixedSize(25*self.ratio, 25*self.ratio)
        self.setStyleSheet('''
                           QPushButton{
                               color: white;
                               border: 0px solid;
                               border-radius: 5px;
                               font-weight: bold;}
                           ''')
        
        self.set(side)
        
        self.clicked.connect(self._nextState)
            
    def get(self):
        if self.state == "-":
            return ""
        else:
            return f"{self.state}_"
        
    def set(self, side):
        if side not in "-LR":
            return
        
        self.state = side
        self.setText(side)
        
        if side == "-":
            r, g, b = [255, 255, 255]
        elif side == "L":
            r, g, b = [108, 200, 255]
        else:
            r, g, b = [255, 108, 108]
        self.setStyleSheet(f"background-color: rgba({r}, {g}, {b}, 50)")
        
        return

    def _nextState(self):
        states = "-LR"
        i = states.find(self.state)
        next = states[(i+1)%3]
        
        self.set(next)
        
        return

class EditableLabel(QLineEdit):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setEnabled(False)
        
    def mouseDoubleClickEvent(self):
        self.setEnabled(True)
        return

class ImageWidget(QWidget):
    def __init__(self, filename, parent=None):
        super().__init__(parent)
        self.path = self._absolutePath(filename)
        self._initUI()
        
    def __init__(self, filename, width, height, parent=None):
        super().__init__(parent)
        self.path = self._absolutePath(filename)
        self.size = [width, height]
        self._initUI()
        
    def _absolutePath(self, filename):
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, 'icons', filename)
        
        return path
    
    def _initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        pixmap = QPixmap(self.path)
        if self.size:
            w, h = self.size
            pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)

class SwitchButton(QPushButton):
    def __init__(self, onText, offText, parent = None):
        super().__init__(parent)
        self.setCheckable(True)
        self._onText = onText
        self._offText = offText
        
    def __init__(self, onText, offText, width, height, parent = None):
        super().__init__(parent)
        ratio = getScreenRatio()
        self.setCheckable(True)
        self._onText = onText
        self._offText = offText
        self._width = width*ratio
        self._height = height*ratio
        
        self.setFixedWidth(self._width*2.1)
        self.setFixedHeight(self._height*3)

    def paintEvent(self, event):
        palette = self.palette()
        label = self._onText if self.isChecked() else self._offText
        other_label = self._offText if self.isChecked() else self._onText
        bg_color = palette.light()

        radius = self._height
        width = self._width
        center = self.rect().center()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(palette.dark())

        pen = QPen(palette.light().color())
        pen.setWidth(2)
        
        font = QFont()
        font.setPixelSize(16*getScreenRatio())
        font.setBold(True)
        painter.setFont(font)

        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRect(-width, -radius, 2*width, 2.5*radius), radius, radius)
        
        painter.setPen(Qt.NoPen)
        off_rect = QRect(0, -radius, width, 2.5*radius)
        if self.isChecked():
            off_rect.moveLeft(-width)
        painter.drawRoundedRect(off_rect, radius, radius)
        painter.setPen(pen)
        pen.setColor(palette.text().color())
        painter.drawText(off_rect, Qt.AlignCenter, other_label)
        
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        sw_rect = QRect(0, -radius, width, 2.5*radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.setPen(pen)
        painter.drawText(sw_rect, Qt.AlignCenter, label)
        
class DragWidget(QWidget):  # MAYBE QListView?
    """
    Generic list sorting handler.
    """

    orderChanged = Signal(list)

    def __init__(self, *args, orientation=Qt.Orientation.Vertical, **kwargs):
        super().__init__()
        self.setAcceptDrops(True)

        # Store the orientation for drag checks later.
        self.orientation = orientation

        if self.orientation == Qt.Orientation.Vertical:
            self.blayout = QVBoxLayout()
        else:
            self.blayout = QHBoxLayout()

        self.setLayout(self.blayout)
        self.blayout.setSizeConstraint(QLayout.SetMinAndMaxSize)

    def dragEnterEvent(self, e):
        e.accept()
        self.setDropIndicatorShown(True)

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()
        # dropIndicator = DropIndicatorPosition()

        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            if self.orientation == Qt.Orientation.Vertical:
                # Drag drop vertically.
                drop_here = pos.y() < w.y() + w.size().height() // 2
            else:
                # Drag drop horizontally.
                drop_here = pos.x() < w.x() + w.size().width() // 2

            if drop_here:
                # We didn't drag past this widget.
                # insert to the left of it.
                self.blayout.insertWidget(n-1, widget)
                self.orderChanged.emit(self.get_item_data())
                break
            
        self.setDropIndicatorShown(False)

        e.accept()

    def add_item(self, item):
        self.blayout.addWidget(item)

    def get_item_data(self):
        data = []
        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            data.append(w.data)
        return data

class DragItem(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContentsMargins(25, 5, 25, 5)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 1px solid black;")
        # Store data separately from display label, but use label for default.
        self.data = self.text()
        self.setFixedHeight(50)

    def set_data(self, data):
        self.data = data

    def mouseMoveEvent(self, e):

        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)
