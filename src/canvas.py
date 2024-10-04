from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsEllipseItem
from PyQt5.QtGui import QPen, QColor, QPainter
from PyQt5.QtCore import Qt, QPointF, QLineF

class ControlPoint(QGraphicsEllipseItem):
    def __init__(self, x, y, callback, line):
        super().__init__(x - 5, y - 5, 10, 10)  # Control point size
        self.setBrush(QColor(255, 0, 0))  # Red color for visibility
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemSendsScenePositionChanges)
        self.callback = callback  # Store the callback for position changes
        self.line = line  # Reference to the line

    def update_position(self, pos):
        self.setPos(pos)

    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.ItemScenePositionHasChanged:
            self.callback(value)  # Call the callback with the new position
            print(f"Control point moved to: ({value.x():.2f}, {value.y():.2f})")  # Console message
            self.line.main_window.console_area.append(f"Control point moved to: ({value.x():.2f}, {value.y():.2f})")  # Console output
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        # Notify when a control point is clicked
        if event.button() == Qt.LeftButton:
            print("Control point clicked")
            self.line.main_window.console_area.append("Control point clicked")  # Console output
        super().mousePressEvent(event)  # Call the base class method to ensure normal behavior

class DrawingCanvas(QGraphicsView):
    def __init__(self, main_window):
        super().__init__()

        # Create the scene and set its rect
        self.scene = QGraphicsScene(0, 0, 800, 600)  # Define the scene size to positive coordinates
        self.setScene(self.scene)

        self.lines = []  # Store lines as tuples of start and end points
        self.control_points = []  # Store control points for lines
        self.current_line = None  # Current line being drawn
        self.start_point = None  # Start point of the line
        self.selected_line = None  # Line currently selected
        self.main_window = main_window  # Reference to the main window

        self.setRenderHint(QPainter.Antialiasing)  # Smooth rendering

    def mousePressEvent(self, event):
        if self.main_window.current_tool == 'line' and event.button() == Qt.LeftButton:
            self.start_point = self.mapToScene(event.pos())  # Get start point correctly
            self.current_line = QGraphicsLineItem()  # Create a new line item
            self.current_line.setPen(QPen(QColor(0, 0, 0), 2))  # Set pen color and width
            self.current_line.setLine(self.start_point.x(), self.start_point.y(), self.start_point.x(), self.start_point.y())  # Initialize line with the same start point
            self.scene.addItem(self.current_line)  # Add line to the scene
            
            # Show starting coordinates in the console
            self.main_window.console_area.append(f"Start Point: ({self.start_point.x():.2f}, {self.start_point.y():.2f})")

        elif self.main_window.current_tool == 'select' and event.button() == Qt.LeftButton:
            # Check if a line is clicked
            line_item = self.itemAt(event.pos())
            if isinstance(line_item, QGraphicsLineItem):
                self.selected_line = line_item
                self.add_control_points(line_item)

    def add_control_points(self, line_item):
        # Clear existing control points
        for cp in self.control_points:
            self.scene.removeItem(cp)
        self.control_points.clear()

        # Get line coordinates
        line = line_item.line()
        start = line.p1()
        end = line.p2()

        # Create control points at start and end of the line
        cp_start = ControlPoint(start.x(), start.y(), self.update_line_start, self)
        cp_end = ControlPoint(end.x(), end.y(), self.update_line_end, self)

        self.control_points.append(cp_start)
        self.control_points.append(cp_end)

        # Add control points to the scene
        self.scene.addItem(cp_start)
        self.scene.addItem(cp_end)

    def update_line_start(self, pos):
        # Update the start point of the line
        if self.selected_line:
            line = self.selected_line.line()
            new_line = QLineF(pos, line.p2())
            self.selected_line.setLine(new_line)
            self.update_control_points()

    def update_line_end(self, pos):
        # Update the end point of the line
        if self.selected_line:
            line = self.selected_line.line()
            new_line = QLineF(line.p1(), pos)
            self.selected_line.setLine(new_line)
            self.update_control_points()

    def update_control_points(self):
        # Update the position of control points
        if self.selected_line:
            line = self.selected_line.line()
            start_cp, end_cp = self.control_points
            start_cp.update_position(line.p1())
            end_cp.update_position(line.p2())

    def mouseMoveEvent(self, event):
        if self.current_line and self.start_point:
            end_point = self.mapToScene(event.pos())  # Get end point
            self.current_line.setLine(self.start_point.x(), self.start_point.y(), end_point.x(), end_point.y())  # Update line

    def mouseReleaseEvent(self, event):
        if self.current_line and event.button() == Qt.LeftButton:
            self.lines.append((self.start_point, self.current_line.line()))  # Save line to the list
            self.current_line = None  # Reset current line
            self.start_point = None  # Reset start point

    def clear_canvas(self):
        # Clear the scene and handle control points and lines correctly
        for cp in self.control_points:  # Remove existing control points
            self.scene.removeItem(cp)
        self.control_points.clear()
        
        self.scene.clear()  # Clear all items from the scene
        self.lines.clear()  # Clear lines list
