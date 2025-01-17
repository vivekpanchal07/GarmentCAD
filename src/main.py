import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar,
    QAction, QLabel, QTextEdit, QSplitter, QToolButton, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from canvas import DrawingCanvas  # Ensure this import is correct

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and dimensions
        self.setWindowTitle("Garment CAD")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Set up the layout
        layout = QVBoxLayout(self.central_widget)

        # Create a horizontal splitter
        self.splitter = QSplitter(Qt.Vertical)  # Use vertical orientation
        layout.addWidget(self.splitter)

        # Create the drawing canvas
        self.canvas = DrawingCanvas(self)
        self.splitter.addWidget(self.canvas)

        # Create a vertical layout for the console
        console_layout = QVBoxLayout()  # Create a new vertical layout for the console

        # Create a horizontal layout for the console title and clear button
        console_header_layout = QHBoxLayout()

        # Add a title for the console
        console_title = QLabel("Console")
        console_header_layout.addWidget(console_title)

        # Add a button to clear the console
        self.clear_console_button = QToolButton()
        self.clear_console_button.setIcon(QIcon("assets/icons/clear_icon.png"))  # Use an icon image (ensure you have the icon file)
        self.clear_console_button.setToolTip("Clear Console")  # Set tooltip for the button
        self.clear_console_button.setFixedSize(20, 20)  # Set a small size for the button
        self.clear_console_button.clicked.connect(self.clear_console)
        console_header_layout.addWidget(self.clear_console_button)

        # Add the console header layout to the console layout
        console_layout.addLayout(console_header_layout)

        # Add console area
        self.console_area = QTextEdit(self)
        self.console_area.setReadOnly(True)  # Make it read-only
        self.console_area.setFont(QFont("Courier New", 8))  # Set monospaced font
        console_layout.addWidget(self.console_area)

        # Add the console layout to the main layout
        layout.addLayout(console_layout)

        # Set initial sizes for the splitter
        self.splitter.setSizes([500, 100])  # Adjust sizes as needed

        # Create a toolbar
        self.create_toolbar()

        # Set the default tool to None
        self.current_tool = None

    def create_toolbar(self):
        toolbar = QToolBar("Tools")
        self.addToolBar(toolbar)

        # Add tools/actions to the toolbar
        line_tool_action = QAction("Line Tool", self)
        line_tool_action.triggered.connect(self.select_line_tool)
        toolbar.addAction(line_tool_action)

        select_tool_action = QAction("Select Tool", self)
        select_tool_action.triggered.connect(self.select_select_tool)
        toolbar.addAction(select_tool_action)

        curve_tool_action = QAction("Curve Tool", self)
        curve_tool_action.triggered.connect(self.select_curve_tool)
        toolbar.addAction(curve_tool_action)

        clear_canvas_action = QAction("Clear Canvas", self)
        clear_canvas_action.triggered.connect(self.canvas.clear_canvas)
        toolbar.addAction(clear_canvas_action)

    def select_line_tool(self):
        self.current_tool = 'line'  # Set the current tool
        self.console_area.append("Line Tool selected")
        self.console_area.append("Use the mouse to draw a line on the canvas.")

    def select_select_tool(self):
        self.current_tool = 'select'  # Set the current tool to select
        self.console_area.append("Select Tool activated. Click on a line to select it.")

    def select_curve_tool(self):
        self.current_tool = 'curve'  # Set the current tool
        self.console_area.append("Curve Tool selected")
        self.console_area.append("Use the mouse to create a curve on the canvas.")

    def clear_console(self):
        self.console_area.clear()  # Clear the console text
        # self.console_area.append("Console cleared.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
