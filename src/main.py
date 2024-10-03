import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QAction, QLabel, QTextEdit, QSplitter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

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
        splitter = QSplitter(Qt.Vertical)  # Use vertical orientation
        layout.addWidget(splitter)

        # Add a label for the drawing canvas (for now)
        self.canvas_label = QLabel("Drawing Canvas Area")
        splitter.addWidget(self.canvas_label)

        # Add a title for the console
        console_title = QLabel("Console")
        layout.addWidget(console_title)

        # Add console area
        self.console_area = QTextEdit(self)
        self.console_area.setReadOnly(True)  # Make it read-only
        self.console_area.setFont(QFont("Courier New", 8))  # Set monospaced font
        splitter.addWidget(self.console_area)

        # Set initial sizes for the splitter
        splitter.setSizes([500, 100])  # Adjust sizes as needed

        # Create a toolbar
        self.create_toolbar()

    def create_toolbar(self):
        toolbar = QToolBar("Tools")
        self.addToolBar(toolbar)

        # Add tools/actions to the toolbar
        line_tool_action = QAction("Line Tool", self)
        line_tool_action.triggered.connect(self.select_line_tool)
        toolbar.addAction(line_tool_action)

        curve_tool_action = QAction("Curve Tool", self)
        curve_tool_action.triggered.connect(self.select_curve_tool)
        toolbar.addAction(curve_tool_action)

    def select_line_tool(self):
        self.console_area.append("Line Tool selected")
        self.console_area.append("Use the mouse to draw a line on the canvas.")

    def select_curve_tool(self):
        self.console_area.append("Curve Tool selected")
        self.console_area.append("Use the mouse to create a curve on the canvas.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
