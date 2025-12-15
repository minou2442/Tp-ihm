"""
Database Schema Designer - Dialog Windows
University of Jijel - IHM Module

This module contains all dialog classes for user interaction
(Create Table, Add Attribute, Create Relationship, etc.)
"""

from typing import Optional
from PySide6.QtWidgets import (
    QDialog, QFormLayout, QHBoxLayout, QLineEdit, QComboBox,
    QCheckBox, QPushButton, QLabel
)
from PySide6.QtGui import QFont

from models import Attribute, Relationship, RelationshipType


class CreateTableDialog(QDialog):
    """Dialog for creating a new table"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Table")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QFormLayout()
        
        self.table_name = QLineEdit()
        self.table_name.setPlaceholderText("e.g., Users, Products")
        layout.addRow("Table Name:", self.table_name)
        
        buttons = QHBoxLayout()
        ok_btn = QPushButton("Create")
        cancel_btn = QPushButton("Cancel")
        
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_table_name(self) -> str:
        return self.table_name.text().strip()


class AttributeDialog(QDialog):
    """Dialog for adding/editing attributes"""
    
    def __init__(self, parent=None, attribute: Optional[Attribute] = None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Attribute")
        self.setGeometry(100, 100, 450, 350)
        
        layout = QFormLayout()
        
        self.attr_name = QLineEdit()
        self.attr_name.setPlaceholderText("e.g., user_id, email")
        
        self.data_type = QComboBox()
        self.data_type.addItems([
            "INT", "VARCHAR(255)", "TEXT", "FLOAT", "BOOLEAN",
            "DATE", "DATETIME", "DECIMAL(10,2)", "BIGINT", "SMALLINT"
        ])
        
        self.is_pk = QCheckBox("Primary Key")
        self.is_nullable = QCheckBox("Nullable")
        self.is_nullable.setChecked(True)
        
        layout.addRow("Attribute Name:", self.attr_name)
        layout.addRow("Data Type:", self.data_type)
        layout.addRow(self.is_pk)
        layout.addRow(self.is_nullable)
        
        if attribute:
            self.attr_name.setText(attribute.name)
            index = self.data_type.findText(attribute.data_type)
            if index >= 0:
                self.data_type.setCurrentIndex(index)
            self.is_pk.setChecked(attribute.is_primary_key)
            self.is_nullable.setChecked(attribute.is_nullable)
        
        buttons = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_attribute(self) -> Attribute:
        return Attribute(
            name=self.attr_name.text().strip(),
            data_type=self.data_type.currentText(),
            is_primary_key=self.is_pk.isChecked(),
            is_nullable=self.is_nullable.isChecked()
        )


class RelationshipDialog(QDialog):
    """Dialog for creating relationships"""
    
    def __init__(self, parent=None, tables: Optional[list] = None):
        super().__init__(parent)
        self.setWindowTitle("Create Relationship")
        self.setGeometry(100, 100, 500, 400)
        
        layout = QFormLayout()
        
        self.from_table = QComboBox()
        self.to_table = QComboBox()
        self.rel_type = QComboBox()
        self.from_key = QLineEdit()
        self.to_key = QLineEdit()
        
        if tables:
            self.from_table.addItems(tables)
            self.to_table.addItems(tables)
        
        self.rel_type.addItems(["1-1", "1-N", "N-N"])
        self.rel_type.setCurrentText("1-N")
        
        layout.addRow("From Table:", self.from_table)
        layout.addRow("To Table:", self.to_table)
        layout.addRow("Relationship Type:", self.rel_type)
        layout.addRow("From Key (Optional):", self.from_key)
        layout.addRow("To Key (Optional):", self.to_key)
        
        buttons = QHBoxLayout()
        ok_btn = QPushButton("Create")
        cancel_btn = QPushButton("Cancel")
        
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_relationship(self) -> Relationship:
        return Relationship(
            from_table=self.from_table.currentText(),
            to_table=self.to_table.currentText(),
            relationship_type=RelationshipType(self.rel_type.currentText()),
            from_key=self.from_key.text().strip(),
            to_key=self.to_key.text().strip()
        )
