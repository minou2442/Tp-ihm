"""
Database Schema Designer - SQL Generator
University of Jijel - IHM Module

This module handles SQL code generation from the database schema,
including CREATE TABLE statements and foreign key constraints.
"""

from models import Schema, Table, Relationship, RelationshipType


class SQLGenerator:
    """Generates SQL CREATE TABLE statements from schema"""
    
    @staticmethod
    def generate_sql(schema: Schema) -> str:
        """Generate SQL CREATE TABLE statements"""
        sql_statements = []
        
        for table_name, table in schema.tables.items():
            sql = SQLGenerator._generate_table_sql(table)
            sql_statements.append(sql)
        
        # Add foreign key constraints from relationships
        for rel in schema.relationships:
            sql = SQLGenerator._generate_relationship_sql(rel)
            if sql:
                sql_statements.append(sql)
        
        return "\n\n".join(sql_statements)
    
    @staticmethod
    def _generate_table_sql(table: Table) -> str:
        """Generate CREATE TABLE statement for a single table"""
        if not table.attributes:
            return f"-- Table {table.name} has no attributes"
        
        lines = [f"CREATE TABLE {table.name} ("]
        
        for i, attr in enumerate(table.attributes):
            line = f"    {attr.name} {attr.data_type}"
            
            if attr.is_primary_key:
                line += " PRIMARY KEY"
            
            if not attr.is_nullable:
                line += " NOT NULL"
            
            if i < len(table.attributes) - 1:
                line += ","
            
            lines.append(line)
        
        lines.append(");")
        return "\n".join(lines)
    
    @staticmethod
    def _generate_relationship_sql(rel: Relationship) -> str:
        """Generate ALTER TABLE statement for relationships"""
        if not rel.from_key or not rel.to_key:
            return ""
        
        if rel.relationship_type == RelationshipType.ONE_TO_MANY:
            return (
                f"ALTER TABLE {rel.to_table} "
                f"ADD CONSTRAINT fk_{rel.from_table}_{rel.to_table} "
                f"FOREIGN KEY ({rel.to_key}) "
                f"REFERENCES {rel.from_table}({rel.from_key});"
            )
        
        return ""
