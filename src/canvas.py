from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsEllipseItem
from PyQt5.QtGui import QPen, QColor, QPainter
from PyQt5.QtCore import Qt, QPointF, QLineF

class ControlPoint(QGraphicsEllipseItem):
    def __init__(self, parent_line, is_start):
        super().__init__(-5, -5, 10, 10)  # Control point size
        self.setBrush(QColor(255, 0, 0))  # Red color for visibility
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)
        self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges, True)
        self.setCursor(Qt.PointingHandCursor)
        self.parent_line = parent_line
        self.is_start = is_start
        self.update_position()

    def update_position(self):
        if self.is_start:
            self.setPos(self.parent_line.line().p1())
        else:
            self.setPos(self.parent_line.line().p2())

    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.ItemPositionChange and self.scene():
            new_pos = value
            line = self.parent_line.line()
            if self.is_start:
                new_line = QLineF(new_pos, line.p2())
            else:
                new_line = QLineF(line.p1(), new_pos)
            self.parent_line.setLine(new_line)
            
            # Console output
            print(f"Control point moved to: ({new_pos.x():.2f}, {new_pos.y():.2f})")
            if hasattr(self.scene().views()[0], 'main_window'):
                self.scene().views()[0].main_window.console_area.append(f"Control point moved to: ({new_pos.x():.2f}, {new_pos.y():.2f})")
        
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("Control point clicked")
            if hasattr(self.scene().views()[0], 'main_window'):
                self.scene().views()[0].main_window.console_area.append("Control point clicked")
        super().mousePressEvent(event)

class DrawingCanvas(QGraphicsView):
    def __init__(self, main_window):
        super().__init__()
        self.scene = QGraphicsScene(0, 0, 800, 600)
        self.setScene(self.scene)
        self.lines = []
        self.control_points = []
        self.current_line = None
        self.start_point = None
        self.selected_line = None
        self.main_window = main_window
        self.current_tool = None
        self.setRenderHint(QPainter.Antialiasing)

    def set_tool(self, tool):
        self.current_tool = tool
        if tool != 'select':
            self.clear_control_points()
            self.selected_line = None

    def mousePressEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        if self.current_tool == 'line' and event.button() == Qt.LeftButton:
            self.start_point = scene_pos
            self.current_line = QGraphicsLineItem()
            self.current_line.setPen(QPen(QColor(0, 0, 0), 2))
            self.current_line.setLine(self.start_point.x(), self.start_point.y(), self.start_point.x(), self.start_point.y())
            self.scene.addItem(self.current_line)
            self.main_window.console_area.append(f"Start Point: ({self.start_point.x():.2f}, {self.start_point.y():.2f})")
        elif self.current_tool == 'select' and event.button() == Qt.LeftButton:
            item = self.scene.itemAt(scene_pos, self.transform())
            if isinstance(item, QGraphicsLineItem):
                self.selected_line = item
                self.add_control_points(item)
            elif not isinstance(item, ControlPoint):
                self.clear_control_points()
                self.selected_line = None
        super().mousePressEvent(event)

    def add_control_points(self, line_item):
        self.clear_control_points()

        cp_start = ControlPoint(line_item, True)
        cp_end = ControlPoint(line_item, False)

        self.control_points.extend([cp_start, cp_end])
        self.scene.addItem(cp_start)
        self.scene.addItem(cp_end)

    def clear_control_points(self):
        for cp in self.control_points:
            self.scene.removeItem(cp)
        self.control_points.clear()

    def mouseMoveEvent(self, event):
        if self.current_line and self.start_point:
            end_point = self.mapToScene(event.pos())
            self.current_line.setLine(self.start_point.x(), self.start_point.y(), end_point.x(), end_point.y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.current_line and event.button() == Qt.LeftButton:
            self.lines.append(self.current_line)
            self.current_line = None
            self.start_point = None
        super().mouseReleaseEvent(event)

    def clear_canvas(self):
        self.clear_control_points()
        self.scene.clear()
        self.lines.clear()
        self.selected_line = None
