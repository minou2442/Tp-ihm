"""
Database Schema Designer - Data Models
University of Jijel - IHM Module
Mini Project: Database Schema Designer

This module contains all data model classes using dataclasses
and Enums for type safety and serialization.
"""

from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import Dict, List, Optional


class RelationshipType(Enum):
    """Enum for relationship types"""
    ONE_TO_ONE = "1-1"
    ONE_TO_MANY = "1-N"
    MANY_TO_MANY = "N-N"


@dataclass
class Attribute:
    """Represents a database attribute/column"""
    name: str
    data_type: str
    is_primary_key: bool = False
    is_nullable: bool = True
    
    def to_dict(self):
        return asdict(self)
    
    @staticmethod
    def from_dict(data):
        return Attribute(**data)


@dataclass
class Table:
    """Represents a database table"""
    name: str
    x: float = 100
    y: float = 100
    attributes: List[Attribute] = field(default_factory=list)
    
    def add_attribute(self, attr: Attribute):
        if not any(a.name == attr.name for a in self.attributes):
            self.attributes.append(attr)
    
    def remove_attribute(self, attr_name: str):
        self.attributes = [a for a in self.attributes if a.name != attr_name]
    
    def to_dict(self):
        return {
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "attributes": [a.to_dict() for a in self.attributes]
        }
    
    @staticmethod
    def from_dict(data):
        table = Table(data["name"], data.get("x", 100), data.get("y", 100))
        table.attributes = [Attribute.from_dict(a) for a in data.get("attributes", [])]
        return table


@dataclass
class Relationship:
    """Represents a relationship between two tables"""
    from_table: str
    to_table: str
    relationship_type: RelationshipType
    from_key: str = ""
    to_key: str = ""
    
    def to_dict(self):
        return {
            "from_table": self.from_table,
            "to_table": self.to_table,
            "relationship_type": self.relationship_type.value,
            "from_key": self.from_key,
            "to_key": self.to_key
        }
    
    @staticmethod
    def from_dict(data):
        return Relationship(
            data["from_table"],
            data["to_table"],
            RelationshipType(data["relationship_type"]),
            data.get("from_key", ""),
            data.get("to_key", "")
        )


@dataclass
class Schema:
    """Represents the complete database schema"""
    name: str = "MySchema"
    tables: Dict[str, Table] = field(default_factory=dict)
    relationships: List[Relationship] = field(default_factory=list)
    
    def add_table(self, table: Table):
        self.tables[table.name] = table
    
    def remove_table(self, table_name: str):
        if table_name in self.tables:
            del self.tables[table_name]
            # Remove relationships involving this table
            self.relationships = [
                r for r in self.relationships
                if r.from_table != table_name and r.to_table != table_name
            ]
    
    def add_relationship(self, rel: Relationship):
        if rel not in self.relationships:
            self.relationships.append(rel)
    
    def to_dict(self):
        return {
            "name": self.name,
            "tables": {k: v.to_dict() for k, v in self.tables.items()},
            "relationships": [r.to_dict() for r in self.relationships]
        }
    
    @staticmethod
    def from_dict(data):
        schema = Schema(data.get("name", "MySchema"))
        schema.tables = {k: Table.from_dict(v) for k, v in data.get("tables", {}).items()}
        schema.relationships = [Relationship.from_dict(r) for r in data.get("relationships", [])]
        return schema
