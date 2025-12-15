"""
Database Schema Designer - Main Application
University of Jijel - IHM Module
Mini Project: Database Schema Designer

Main application window with MVC pattern implementation.
Features: Table management, relationship creation, SQL generation, file I/O
"""

import sys
import json
from typing import Dict, List

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGraphicsView, QGraphicsScene, QDialog, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QMessageBox, QFileDialog, QListWidget,
    QListWidgetItem, QTextEdit
)
from PySide6.QtCore import Qt, QPointF, Slot
from PySide6.QtGui import QColor, QPen, QBrush, QFont, QAction, QKeySequence

from models import Schema, Table, Attribute, Relationship, RelationshipType
from graphics import TableBlockItem, RelationshipLineItem
from dialogs import CreateTableDialog, AttributeDialog, RelationshipDialog
from sql_generator import SQLGenerator


class DatabaseSchemaDesigner(QMainWindow):
    """Main application window - Controller in MVC pattern"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Schema Designer - University of Jijel")
        self.setGeometry(100, 100, 1400, 900)
        
        # Model
        self.schema = Schema()
        
        # View components
        self.table_items: Dict[str, TableBlockItem] = {}
        self.relationship_items: List[RelationshipLineItem] = []
        
        self.setup_ui()
        self.setup_menu()
    
    def setup_ui(self):
        """Setup user interface"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout()
        
        # ===== CANVAS/GRAPHICS VIEW =====
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 1200, 800)
        self.scene.setBackgroundBrush(QBrush(QColor("#F5F5F5")))
        
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(self.view.RenderHint.Antialiasing)
        
        main_layout.addWidget(self.view, 3)
        
        # ===== RIGHT CONTROL PANEL =====
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # Control buttons
        btn_layout = QVBoxLayout()
        
        self.btn_add_table = QPushButton("+ Add Table")
        self.btn_add_table.clicked.connect(self.add_table)
        btn_layout.addWidget(self.btn_add_table)
        
        self.btn_add_relationship = QPushButton("+ Add Relationship")
        self.btn_add_relationship.clicked.connect(self.add_relationship)
        btn_layout.addWidget(self.btn_add_relationship)
        
        self.btn_delete_selected = QPushButton("🗑 Delete Selected")
        self.btn_delete_selected.clicked.connect(self.delete_selected)
        btn_layout.addWidget(self.btn_delete_selected)
        
        self.btn_edit_table = QPushButton("✎ Edit Table")
        self.btn_edit_table.clicked.connect(self.edit_selected_table)
        btn_layout.addWidget(self.btn_edit_table)
        
        right_layout.addLayout(btn_layout)
        right_layout.addSpacing(20)
        
        # ===== SQL CODE PANEL =====
        sql_label = QLabel("Generated SQL Code:")
        sql_label.setFont(QFont("Arial", 10, QFont.Bold))
        right_layout.addWidget(sql_label)
        
        self.sql_display = QTextEdit()
        self.sql_display.setReadOnly(True)
        self.sql_display.setFont(QFont("Courier", 9))
        self.sql_display.setPlaceholderText("SQL code will appear here...")
        right_layout.addWidget(self.sql_display)
        
        # ===== TABLES LIST =====
        tables_label = QLabel("Tables:")
        tables_label.setFont(QFont("Arial", 10, QFont.Bold))
        right_layout.addWidget(tables_label)
        
        self.tables_list = QListWidget()
        self.tables_list.itemClicked.connect(self.on_table_selected)
        right_layout.addWidget(self.tables_list)
        
        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel, 1)
        
        main_widget.setLayout(main_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready - Database Schema Designer")
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # ===== FILE MENU =====
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Schema", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_schema)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open Schema", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_schema)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save Schema", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_schema)
        file_menu.addAction(save_action)
        
        export_sql_action = QAction("Export SQL", self)
        export_sql_action.triggered.connect(self.export_sql)
        file_menu.addAction(export_sql_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # ===== EDIT MENU =====
        edit_menu = menubar.addMenu("Edit")
        
        clear_action = QAction("Clear All", self)
        clear_action.triggered.connect(self.clear_all)
        edit_menu.addAction(clear_action)
        
        # ===== HELP MENU =====
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    # =========================================================================
    # TABLE MANAGEMENT SLOTS
    # =========================================================================
    
    @Slot()
    def add_table(self):
        """Add a new table to the schema"""
        dialog = CreateTableDialog(self)
        if dialog.exec() == QDialog.Accepted:
            table_name = dialog.get_table_name()
            
            if not table_name:
                QMessageBox.warning(self, "Error", "Table name cannot be empty")
                return
            
            if table_name in self.schema.tables:
                QMessageBox.warning(self, "Error", f"Table '{table_name}' already exists")
                return
            
            # Create table in model
            table = Table(table_name)
            self.schema.add_table(table)
            
            # Add to graphics scene
            table_item = TableBlockItem(table)
            self.scene.addItem(table_item)
            self.table_items[table_name] = table_item
            
            self.update_tables_list()
            self.update_sql_display()
            self.statusBar().showMessage(f"Table '{table_name}' created")
    
    @Slot()
    def edit_selected_table(self):
        """Edit selected table's attributes"""
        selected_items = self.tables_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "No table selected")
            return
        
        table_name = selected_items[0].text()
        table = self.schema.tables[table_name]
        
        # Create attribute management dialog
        attr_dialog = QDialog(self)
        attr_dialog.setWindowTitle(f"Edit Table: {table_name}")
        attr_dialog.setGeometry(100, 100, 500, 500)
        
        layout = QVBoxLayout()
        
        # Attributes table
        attr_table = QTableWidget()
        attr_table.setColumnCount(4)
        attr_table.setHorizontalHeaderLabels(["Name", "Type", "PK", "Nullable"])
        
        for i, attr in enumerate(table.attributes):
            attr_table.insertRow(i)
            attr_table.setItem(i, 0, QTableWidgetItem(attr.name))
            attr_table.setItem(i, 1, QTableWidgetItem(attr.data_type))
            
            pk_item = QTableWidgetItem("✓" if attr.is_primary_key else "")
            attr_table.setItem(i, 2, pk_item)
            
            null_item = QTableWidgetItem("✓" if attr.is_nullable else "")
            attr_table.setItem(i, 3, null_item)
        
        layout.addWidget(attr_table)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        add_attr_btn = QPushButton("+ Add Attribute")
        add_attr_btn.clicked.connect(lambda: self.add_attribute(table, attr_table))
        btn_layout.addWidget(add_attr_btn)
        
        remove_attr_btn = QPushButton("- Remove Selected")
        remove_attr_btn.clicked.connect(lambda: self.remove_attribute(table, attr_table))
        btn_layout.addWidget(remove_attr_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(attr_dialog.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        attr_dialog.setLayout(layout)
        
        attr_dialog.exec()
        
        # Update graphics
        self.scene.removeItem(self.table_items[table_name])
        table_item = TableBlockItem(table)
        self.scene.addItem(table_item)
        self.table_items[table_name] = table_item
        
        # Redraw relationships
        self.redraw_relationships()
        self.update_sql_display()
        self.statusBar().showMessage(f"Table '{table_name}' updated")
    
    def add_attribute(self, table: Table, attr_table: QTableWidget):
        """Add attribute to table"""
        dialog = AttributeDialog(self)
        if dialog.exec() == QDialog.Accepted:
            attr = dialog.get_attribute()
            
            if not attr.name:
                QMessageBox.warning(self, "Error", "Attribute name cannot be empty")
                return
            
            if any(a.name == attr.name for a in table.attributes):
                QMessageBox.warning(self, "Error", f"Attribute '{attr.name}' already exists")
                return
            
            table.add_attribute(attr)
            
            # Update table widget
            row = attr_table.rowCount()
            attr_table.insertRow(row)
            attr_table.setItem(row, 0, QTableWidgetItem(attr.name))
            attr_table.setItem(row, 1, QTableWidgetItem(attr.data_type))
            attr_table.setItem(row, 2, QTableWidgetItem("✓" if attr.is_primary_key else ""))
            attr_table.setItem(row, 3, QTableWidgetItem("✓" if attr.is_nullable else ""))
    
    def remove_attribute(self, table: Table, attr_table: QTableWidget):
        """Remove attribute from table"""
        current_row = attr_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "No attribute selected")
            return
        
        attr_name = attr_table.item(current_row, 0).text()
        table.remove_attribute(attr_name)
        attr_table.removeRow(current_row)
    
    # =========================================================================
    # RELATIONSHIP MANAGEMENT SLOTS
    # =========================================================================
    
    @Slot()
    def add_relationship(self):
        """Add a new relationship"""
        if len(self.schema.tables) < 2:
            QMessageBox.warning(self, "Error", "At least two tables required to create a relationship")
            return
        
        tables = list(self.schema.tables.keys())
        dialog = RelationshipDialog(self, tables)
        
        if dialog.exec() == QDialog.Accepted:
            rel = dialog.get_relationship()
            
            if rel.from_table == rel.to_table:
                QMessageBox.warning(self, "Error", "Cannot create self-referencing relationship")
                return
            
            self.schema.add_relationship(rel)
            
            # Add to graphics scene
            from_item = self.table_items[rel.from_table]
            to_item = self.table_items[rel.to_table]
            rel_item = RelationshipLineItem(rel, from_item, to_item)
            self.scene.addItem(rel_item)
            self.relationship_items.append(rel_item)
            
            self.update_sql_display()
            self.statusBar().showMessage(
                f"Relationship created: {rel.from_table} ({rel.relationship_type.value}) -> {rel.to_table}"
            )
    
    @Slot()
    def delete_selected(self):
        """Delete selected table"""
        selected_items = self.tables_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "No table selected")
            return
        
        table_name = selected_items[0].text()
        
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Delete table '{table_name}'?\nThis will also remove all related relationships.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.schema.remove_table(table_name)
            self.scene.removeItem(self.table_items[table_name])
            del self.table_items[table_name]
            
            # Remove relationship items
            self.relationship_items = [
                r for r in self.relationship_items
                if r.relationship.from_table != table_name and r.relationship.to_table != table_name
            ]
            
            # Redraw relationships
            self.redraw_relationships()
            self.update_tables_list()
            self.update_sql_display()
            self.statusBar().showMessage(f"Table '{table_name}' deleted")
    
    @Slot()
    def on_table_selected(self, item):
        """Handle table selection from list"""
        for table_item in self.table_items.values():
            table_item.setPen(QPen(QColor("#2E86AB"), 2))
        
        table_name = item.text()
        self.table_items[table_name].setPen(QPen(QColor("#A23B72"), 3))
    
    def redraw_relationships(self):
        """Redraw all relationship lines"""
        for rel_item in self.relationship_items:
            self.scene.removeItem(rel_item)
        
        self.relationship_items.clear()
        
        for rel in self.schema.relationships:
            from_item = self.table_items.get(rel.from_table)
            to_item = self.table_items.get(rel.to_table)
            
            if from_item and to_item:
                rel_item = RelationshipLineItem(rel, from_item, to_item)
                self.scene.addItem(rel_item)
                self.relationship_items.append(rel_item)
    
    # =========================================================================
    # UI UPDATE SLOTS
    # =========================================================================
    
    def update_tables_list(self):
        """Update tables list widget"""
        self.tables_list.clear()
        for table_name in self.schema.tables.keys():
            self.tables_list.addItem(table_name)
    
    def update_sql_display(self):
        """Update SQL code display"""
        sql = SQLGenerator.generate_sql(self.schema)
        self.sql_display.setText(sql)
    
    # =========================================================================
    # FILE OPERATIONS SLOTS
    # =========================================================================
    
    @Slot()
    def new_schema(self):
        """Create new schema"""
        reply = QMessageBox.question(
            self,
            "New Schema",
            "Create new schema? Unsaved changes will be lost.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.schema = Schema()
            self.scene.clear()
            self.table_items.clear()
            self.relationship_items.clear()
            self.update_tables_list()
            self.update_sql_display()
            self.statusBar().showMessage("New schema created")
    
    @Slot()
    def save_schema(self):
        """Save schema to JSON file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Schema",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.schema.to_dict(), f, indent=2)
                self.statusBar().showMessage(f"Schema saved: {file_path}")
                QMessageBox.information(self, "Success", "Schema saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
    
    @Slot()
    def open_schema(self):
        """Open schema from JSON file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Schema",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.schema = Schema.from_dict(data)
                
                self.scene.clear()
                self.table_items.clear()
                self.relationship_items.clear()
                
                # Recreate table items
                for table in self.schema.tables.values():
                    table_item = TableBlockItem(table)
                    self.scene.addItem(table_item)
                    self.table_items[table.name] = table_item
                
                # Recreate relationship items
                self.redraw_relationships()
                
                self.update_tables_list()
                self.update_sql_display()
                self.statusBar().showMessage(f"Schema loaded: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open: {str(e)}")
    
    @Slot()
    def export_sql(self):
        """Export schema as SQL file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export SQL",
            "",
            "SQL Files (*.sql);;All Files (*)"
        )
        
        if file_path:
            try:
                sql = SQLGenerator.generate_sql(self.schema)
                with open(file_path, 'w') as f:
                    f.write(sql)
                self.statusBar().showMessage(f"SQL exported: {file_path}")
                QMessageBox.information(self, "Success", "SQL exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
    
    @Slot()
    def clear_all(self):
        """Clear entire schema"""
        reply = QMessageBox.question(
            self,
            "Clear All",
            "Clear all tables and relationships?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.schema.tables.clear()
            self.schema.relationships.clear()
            self.scene.clear()
            self.table_items.clear()
            self.relationship_items.clear()
            self.update_tables_list()
            self.update_sql_display()
            self.statusBar().showMessage("Schema cleared")
    
    @Slot()
    def show_about(self):
        """Show about dialog"""
        QMessageBox.information(
            self,
            "About Database Schema Designer",
            "Database Schema Designer v1.0\n\n"
            "A visual tool for designing database schemas.\n\n"
            "Features:\n"
            "• Create tables with attributes\n"
            "• Define relationships (1-1, 1-N, N-N)\n"
            "• Auto-generate SQL code\n"
            "• Save/Load schemas (JSON format)\n"
            "• Export SQL files\n"
            "• Drag-and-drop table positioning\n"
            "• Real-time SQL code generation\n\n"
            "University of Jijel - Department of Computer Science\n"
            "IHM Module - Mini Project"
        )


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseSchemaDesigner()
    window.show()
    sys.exit(app.exec())
