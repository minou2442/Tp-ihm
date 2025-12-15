"""
Database Schema Designer - Graphics Components
University of Jijel - IHM Module

This module contains all QGraphics classes for visual representation
of tables and relationships on the canvas.
"""

from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsLineItem, QGraphicsTextItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPen, QBrush, QFont

from models import Table, Relationship, RelationshipType


class TableBlockItem(QGraphicsRectItem):
    """Visual representation of a table as a draggable block"""
    
    BLOCK_WIDTH = 200
    BLOCK_HEIGHT = 150
    
    def __init__(self, table: Table, parent=None):
        super().__init__(0, 0, self.BLOCK_WIDTH, self.BLOCK_HEIGHT, parent)
        self.table = table
        self.is_selected = False
        
        # Styling
        self.setPen(QPen(QColor("#2E86AB"), 2))
        self.setBrush(QBrush(QColor("#E8F4F8")))
        self.setCursor(Qt.OpenHandCursor)
        self.setPos(QPointF(table.x, table.y))
        self.setFlag(self.ItemIsMovable, True)
        self.setFlag(self.ItemIsSelectable, True)
        
        # Table name
        title_item = QGraphicsTextItem(table.name, self)
        title_font = QFont("Arial", 10)
        title_font.setBold(True)
        title_item.setFont(title_font)
        title_item.setPos(5, 5)
        
        # Attributes list
        y_offset = 25
        for attr in table.attributes:
            attr_text = f"{'[PK] ' if attr.is_primary_key else ''}{attr.name}: {attr.data_type}"
            attr_item = QGraphicsTextItem(attr_text, self)
            attr_font = QFont("Courier", 8)
            attr_item.setFont(attr_font)
            attr_item.setPos(10, y_offset)
            y_offset += 15
    
    def mouseMoveEvent(self, event):
        """Update table position when dragged"""
        super().mouseMoveEvent(event)
        self.table.x = self.pos().x()
        self.table.y = self.pos().y()
    
    def mousePressEvent(self, event):
        """Handle selection"""
        super().mousePressEvent(event)
        self.is_selected = True
        self.setPen(QPen(QColor("#A23B72"), 3))
    
    def mouseReleaseEvent(self, event):
        """Handle deselection"""
        super().mouseReleaseEvent(event)
        if not self.isSelected():
            self.is_selected = False
            self.setPen(QPen(QColor("#2E86AB"), 2))


class RelationshipLineItem(QGraphicsLineItem):
    """Visual representation of a relationship between tables"""
    
    def __init__(self, rel: Relationship, from_item: TableBlockItem, to_item: TableBlockItem, parent=None):
        super().__init__(parent)
        self.relationship = rel
        self.from_item = from_item
        self.to_item = to_item
        
        self.update_line()
        
        # Styling based on relationship type
        color_map = {
            RelationshipType.ONE_TO_ONE: QColor("#F18F01"),      # Orange
            RelationshipType.ONE_TO_MANY: QColor("#C73E1D"),     # Red
            RelationshipType.MANY_TO_MANY: QColor("#6A994E")     # Green
        }
        
        self.setPen(QPen(color_map[rel.relationship_type], 2))
    
    def update_line(self):
        """Update line position based on table positions"""
        from_pos = QPointF(
            self.from_item.pos().x() + self.from_item.BLOCK_WIDTH,
            self.from_item.pos().y() + self.from_item.BLOCK_HEIGHT / 2
        )
        to_pos = QPointF(
            self.to_item.pos().x(),
            self.to_item.pos().y() + self.to_item.BLOCK_HEIGHT / 2
        )
        self.setLine(from_pos.x(), from_pos.y(), to_pos.x(), to_pos.y())
