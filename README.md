# Database Schema Designer

**University of Jijel - Department of Computer Science**  
**Module: IHM (Human-Computer Interface)**  
**Mini Project**

---

## ðŸ“‹ Project Overview

A desktop application for visually designing database schemas with real-time SQL code generation. Built with PySide6 following the **Model-View-Controller (MVC)** architectural pattern.

### âœ… Features Implemented

#### 2.1 Table Management
- âœ… Create tables with unique names
- âœ… Add/Edit/Delete attributes (columns)
- âœ… Specify data types and constraints (Primary Key, Nullable)
- âœ… Visual representation as draggable blocks on canvas
- âœ… Automatic position persistence

#### 2.2 Relationship Management
- âœ… Create 1-1, 1-N, and N-N relationships
- âœ… Visual connector lines between tables
- âœ… Color-coded by relationship type:
  - Orange (1-1)
  - Red (1-N)
  - Green (N-N)
- âœ… Automatic foreign key tracking
- âœ… Dynamic updates when tables move

#### 2.3 SQL Code Generation
- âœ… Generate valid `CREATE TABLE` statements
- âœ… Auto-generate `FOREIGN KEY` constraints
- âœ… Display SQL in read-only panel
- âœ… Real-time updates as schema changes

#### 2.4 SQL Query Execution & File I/O
- âœ… Save schemas as JSON files
- âœ… Load previously saved schemas
- âœ… Export generated SQL to `.sql` files
- âœ… Clear/Reset schema

---

## ðŸ—ï¸ Architecture

### MVC Pattern Implementation

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                   VIEW                               â”‚
â”‚  (PySide6 Widgets, Graphics Items)                  â”‚
â”‚  - TableBlockItem                                   â”‚
â”‚  - RelationshipLineItem                             â”‚
â”‚  - CreateTableDialog, AttributeDialog, etc.         â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                       â†•
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚              CONTROLLER (DatabaseSchemaDesigner)     â”‚
â”‚  - Manages user interactions                         â”‚
â”‚  - Coordinates Model and View updates                â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                       â†•
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                   MODEL                              â”‚
â”‚  (Data Classes, Business Logic)                      â”‚
â”‚  - Schema, Table, Attribute, Relationship           â”‚
â”‚  - SQLGenerator                                      â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### File Structure

```
project/
â”œâ”€â”€ main.py                 # Main application (Controller)
â”œâ”€â”€ models.py              # Data models (Model)
â”œâ”€â”€ graphics.py            # Visual components (View - Graphics)
â”œâ”€â”€ dialogs.py             # Dialog windows (View - Dialogs)
â”œâ”€â”€ sql_generator.py       # SQL generation logic (Model helper)
â”œâ”€â”€ requirements.txt       # Python dependencies
â””â”€â”€ README.md              # This file
```

### Module Responsibilities

| File | Purpose | MVC Role |
|------|---------|----------|
| `models.py` | Data classes (Schema, Table, Attribute, Relationship) | Model |
| `graphics.py` | QGraphics items for visual representation | View |
| `dialogs.py` | Dialog windows for user input | View |
| `sql_generator.py` | SQL code generation from schema | Model |
| `main.py` | Main application window & event handling | Controller |

---

## ðŸš€ Installation & Setup

### Requirements
- Python 3.8+
- PySide6

### Installation Steps

```bash
# 1. Clone or download the project
cd database-schema-designer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python main.py
```

---

## ðŸ“– Usage Guide

### Creating a Schema

1. **Add a Table**
   - Click "+ Add Table"
   - Enter table name (e.g., "Users")
   - Table appears as a block on the canvas

2. **Add Attributes**
   - Select table in the list
   - Click "âœŽ Edit Table"
   - Click "+ Add Attribute"
   - Fill in: Name, Data Type, Primary Key (if needed), Nullable status

3. **Create Relationships**
   - Click "+ Add Relationship"
   - Select: From Table, To Table, Relationship Type (1-1, 1-N, N-N)
   - Optionally specify foreign keys
   - Line appears connecting the tables

4. **View Generated SQL**
   - SQL code updates automatically in the right panel
   - Copy/paste or export to `.sql` file

5. **Save Your Work**
   - File â†’ Save Schema (saves as JSON)
   - File â†’ Export SQL (saves as SQL file)

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New Schema |
| `Ctrl+O` | Open Schema |
| `Ctrl+S` | Save Schema |

---

## ðŸŽ¨ User Interface Layout

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                                     â”‚   Control Buttons    â”‚
â”‚          CANVAS VIEW                â”‚  + Add Table         â”‚
â”‚     (Drag & drop tables)            â”‚  + Add Relationship  â”‚
â”‚                                     â”‚  ðŸ—‘ Delete Selected  â”‚
â”‚                                     â”‚  âœŽ Edit Table       â”‚
â”‚                                     â”‚                      â”‚
â”‚                                     â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                     â”‚  Generated SQL Code  â”‚
â”‚                                     â”‚  (Read-only)         â”‚
â”‚                                     â”‚                      â”‚
â”‚                                     â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                     â”‚  Tables List         â”‚
â”‚                                     â”‚  â€¢ Table1            â”‚
â”‚                                     â”‚  â€¢ Table2            â”‚
â”‚                                     â”‚  â€¢ Table3            â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## ðŸ› ï¸ Development Details

### Key Classes

#### Models (models.py)
- `Attribute`: Column definition with name, type, constraints
- `Table`: Collection of attributes with position (x, y)
- `Relationship`: Link between two tables
- `Schema`: Complete database schema with tables and relationships

#### Graphics (graphics.py)
- `TableBlockItem`: Visual QGraphicsRectItem for tables
- `RelationshipLineItem`: Visual QGraphicsLineItem for relationships

#### Dialogs (dialogs.py)
- `CreateTableDialog`: Get table name
- `AttributeDialog`: Add/edit column details
- `RelationshipDialog`: Create relationship between tables

#### SQL Generation (sql_generator.py)
- `SQLGenerator`: Generates CREATE TABLE and ALTER TABLE statements

#### Controller (main.py)
- `DatabaseSchemaDesigner`: Main window, handles all user interactions

### Data Persistence

**Schema Format (JSON)**:
```json
{
  "name": "MySchema",
  "tables": {
    "Users": {
      "name": "Users",
      "x": 100,
      "y": 100,
      "attributes": [
        {
          "name": "user_id",
          "data_type": "INT",
          "is_primary_key": true,
          "is_nullable": false
        }
      ]
    }
  },
  "relationships": [
    {
      "from_table": "Users",
      "to_table": "Orders",
      "relationship_type": "1-N",
      "from_key": "user_id",
      "to_key": "user_id"
    }
  ]
}
```

---

## âœ¨ Example Workflow

### E-Commerce Database

**Step 1: Create Tables**
1. Users table (user_id, email, name, created_at)
2. Products table (product_id, name, price)
3. Orders table (order_id, user_id, order_date)
4. OrderItems table (order_item_id, order_id, product_id, quantity)

**Step 2: Define Relationships**
1. Users â†’ Orders (1-N)
2. Orders â†’ OrderItems (1-N)
3. Products â†’ OrderItems (1-N)

**Step 3: View Generated SQL**
```sql
CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at DATETIME
);

CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2)
);

-- ... and more ...
```

**Step 4: Export & Use**
- Export as `schema.sql`
- Use in your database setup scripts

---

## ðŸ“‹ Project Evaluation Criteria

### âœ… All Features Implemented
- [x] All features from section 2 (Table, Relationship, SQL, Query Execution)

### âœ… No Major Crashes
- [x] Comprehensive error handling with user feedback
- [x] Input validation for all operations

### âœ… Clean Separation: Model/View/Controller
- [x] Model: `models.py` + `sql_generator.py`
- [x] View: `graphics.py` + `dialogs.py`
- [x] Controller: `main.py`
- [x] **No application logic in widgets**

### âœ… Code Quality
- [x] Type hints throughout
- [x] Docstrings for all classes and methods
- [x] Clear variable/function names
- [x] Logical module organization

### âœ… UI/UX Polish
- [x] Intuitive drag-and-drop interface
- [x] Color-coded relationships
- [x] Real-time SQL updates
- [x] Status messages for all actions
- [x] Clear error messages with suggestions

---

## ðŸ› Troubleshooting

**Problem: "ModuleNotFoundError: No module named 'PySide6'"**
```bash
pip install PySide6
```

**Problem: Tables not appearing on canvas**
- Check that table names are unique
- Try refreshing by clicking another table and back

**Problem: SQL code not generating**
- Ensure tables have at least one attribute
- Check that relationship tables exist

---

## ðŸ“ Submission Checklist

Before submitting, ensure:

- [ ] All `.py` files present (main.py, models.py, graphics.py, dialogs.py, sql_generator.py)
- [ ] `requirements.txt` includes PySide6
- [ ] `README.md` included with documentation
- [ ] Application runs without crashes
- [ ] All features from section 2 work correctly
- [ ] MVC pattern clearly implemented
- [ ] Code is well-commented

---

## ðŸ‘¨â€ðŸ’¼ Author

**Aymen Boumezbeur**  
Computer Science Student - Year 3  
University of Jijel - Algeria

---

## License

Educational project for IHM Module @ University of Jijel

---

**Happy Designing! 
