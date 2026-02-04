br1 = "rgb(255, 255, 255)"  # background
br2 = "rgb(230, 230, 240)"  # control elements
br21 = "rgb(163, 173, 198)"  # control elements accent
br3 = "rgb(95, 138, 180)"  # highlight
br4 = "rgb(63, 73, 98)"  # accent
br5 = "rgb(215, 0, 0)"  # alert
font = "Times New Roman"

st = (
    "QMainWindow { background-color: "
    + br1
    + "; border: 1px solid grey; border-radius: 5px; }"

    "QDialog { background-color: "
    + br1
    + "; border: 1px solid grey; border-radius: 5px; }"

    "QToolBar { background-color: " + br1 + "; spacing: 4px }"

    "QToolButton { background-color: "
    + br21
    + "; border: 1px solid grey; border-radius: 5px; }"
    "QToolButton:disabled { background-color: "
    + br2
    + "; border: 1px solid grey; border-radius: 5px; }"
    "QToolButton:hover { background-color: "
    + br3
    + "; border: 1px solid grey; border-radius: 5px; }"
    "QToolButton:checked { background-color: "
    + br4
    + "; border: 1px solid grey; border-radius: 5px; }"

    "QGroupBox { border: 2px solid grey; border-radius: 5px; margin-top: 0px; } "
    'QGroupBox[title] { color: black; font-family:'
    + font
    + '; font-size: 14px; font-weight: bold;'
    "border: 2px solid grey; border-radius: 5px; margin-top: 8px; }  "
    "QGroupBox::title { subcontrol-origin: margin; left: 9px; } "
    "QLabel { color: black; background-color: "
    + br1
    + '; font-family:'
    + font
    + ' ; font-size: 14px; } '

    "QLineEdit { color: black; background-color: "
    + br1
    + "; selection-background-color: "
    + br3
    + "; selection-color: "
    + br1
    + '; font-family:'
    + font
    + '; font-size: 14px;'
    "border: 1px solid grey; border-radius: 5px; padding-left: 4px; } "

    "QTextBrowser { color: black; background-color: "
    + br1
    + "; selection-background-color: "
    + br3
    + "; selection-color: "
    + br1
    + '; font-family:'
    + font
    + '; font-size: 14px; border: 1px solid grey; border-radius: 5px; } '

    "QTextEdit { color: black; background-color: "
    + br1
    + "; selection-background-color: "
    + br3
    + "; selection-color: "
    + br1
    + '; font-family:'
    + font
    + '; font-size: 14px; border: 1px solid grey; border-radius: 5px; } '

    "QComboBox { color: black; background-color: "
    + br1
    + '; font-family:'
    + font
    + '; font-size: 14px;'
    "border: 1px solid grey; border-radius: 5px; padding-left: 6px; }"
    "QComboBox::drop-down { border-left: 1px solid grey; width: 20px; background-color: "
    + br2
    + "; border-radius: 5px; } "
    "QComboBox::drop-down:hover { border-left: 1px solid grey; width: 20px; background-color: "
    + br1
    + "; border-radius: 5px; } "
    "QComboBox QAbstractItemView { color: black; background-color: " + br1 + "; }"
    "QComboBox QAbstractItemView::item:hover { color: black; background-color: "
    + br2
    + "; }"

    "QSpinBox { color: black; background-color: "
    + br1
    + "; selection-background-color: "
    + br3
    + "; selection-color: "
    + br1
    + '; font-family:'
    + font
    + '; font-size: 14px; border: 1px solid grey; border-radius: 5px; } '
    "QSpinBox::up-button { border-left: 1px solid grey; width: 20px; background-color: "
    + br21
    + "; border-radius: 2px; } "
    "QSpinBox::up-button:hover { border-left: 1px solid grey; width: 20px; background-color: "
    + br1
    + "; border-radius: 2px; } "
    "QSpinBox::down-button { border-left: 1px solid grey; width: 20px; background-color: "
    + br2
    + "; border-radius: 2px; } "
    "QSpinBox::down-button:hover { border-left: 1px solid grey; width: 20px; background-color: "
    + br1
    + "; border-radius: 2px; } "

    "QDoubleSpinBox {color: black; background-color: "
    + br1
    + "; selection-background-color: "
    + br3
    + "; selection-color: "
    + br1
    + '; font-family:'
    + font
    + '; font-size: 14px; border: 1px solid grey; border-radius: 5px; } '
    "QDoubleSpinBox::up-button { border-left: 1px solid grey; width: 20px; background-color: "
    + br21
    + "; border-radius: 2px; } "
    "QDoubleSpinBox::up-button:hover { border-left: 1px solid grey; width: 20px; background-color: "
    + br1
    + "; border-radius: 2px; } "
    "QDoubleSpinBox::down-button { border-left: 1px solid grey; width: 20px; background-color: "
    + br2
    + "; border-radius: 2px; } "
    "QDoubleSpinBox::down-button:hover { border-left: 1px solid grey; width: 20px; background-color: "
    + br1
    + "; border-radius: 2px; } "

    'QCheckBox { color: black; background-color: white; font-family:'
    + font
    + '; font-size: 14px; } '
    "QCheckBox::indicator { background-color: "
    + br1
    + "; border: 1px solid grey; border-radius: 4px; } "
    "QCheckBox::indicator:checked { background-color: "
    + br4
    + "; border: 1px solid grey; border-radius: 4px; } "

    'QTabWidget { color: black; font-family:'
    + font
    + '; font-size: 14px; font-weight: bold; } '
    "QTabWidget::pane { border: 2px solid grey; border-radius: 5px;}"
    "QTabBar::tab:selected { color: black; background-color: " + br1 + "; } "
    "QTabBar::tab:!selected { color: black; background-color: " + br2 + "; } "

    "QProgressBar { background-color: "
    + br2
    + "; border: 0px solid grey; border-radius: 4px; } "
    "QProgressBar::chunk { background-color: " + br3 + "; border-radius: 4px; } "

    "QHeaderView { color: black; background-color: "
    + br1
    + '; font-family:'
    + font
    + '; font-size: 14px; } '

    'MyTableWidget { font-family:'
    + font
    + '; font-size: 14px; color: black; selection-color: black; background-color: white;'
    'alternate-background-color: white; selection-background-color: '
    + br2
    + "; border: 1px solid grey; border-radius: 5px; } "
    "MyTableWidget QTableCornerButton::section { background-color: " + br1 + "; } "
    "MyTableWidget::indicator { background-color: "
    + br1
    + "; border: 1px solid grey; border-radius: 4px; } "
    "MyTableWidget::indicator:checked { background-color: "
    + br4
    + "; border: 1px solid grey; border-radius: 4px; } "
    "MyTableWidget::item:hover { background-color: transparent; "
    "border: 0px solid grey; border-radius: 4px; } "

    "MyPushButton { border: 1px solid grey; border-radius: 5px; color: black; background-color: "
    + br2
    + '; font-family:'
    + font
    + '; font-size: 14px; font-weight: bold; } '
    "MyPushButton::hover { background-color: " + br1 + "; } "
    "MyPushButton::pressed { background-color: " + br3 + "; color: " + br1 + "; } "
    "MyPushButton::checked { background-color: " + br4 + "; color: " + br1 + "; } "

    "QPushButton { border: 1px solid grey; border-radius: 5px; color: black; background-color: "
    + br2
    + '; font-family:'
    + font
    + '; font-size: 14px; font-weight: bold; } '
)

def styler(inp):
    inp.setStyleSheet(st)

def alert(inp1, inp2):
    match inp2:
        case True:
            inp1.setStyleSheet(
                "background-color: "
                + br5
                + '; font-family:'
                + font
                + '; font-size: 14px; border: 1px solid grey; border-radius: 5px;'
            )
        case False:
            inp1.setStyleSheet(
                "background-color: "
                + br1
                + '; font-family:'
                + font
                + '; font-size: 14px; border: 1px solid grey; border-radius: 5px;'
            )


def success(inp1, inp2):
    match inp2:
        case True:
            inp1.setStyleSheet(
                "background-color: "
                + br3
                + '; font-family:'
                + font
                + '; font-size: 14px; border: 1px solid grey; border-radius: 5px;'
            )
        case False:
            inp1.setStyleSheet(
                "background-color: "
                + br1
                + '; font-family:'
                + font
                + '; font-size: 14px; border: 1px solid grey; border-radius: 5px;'
            )
