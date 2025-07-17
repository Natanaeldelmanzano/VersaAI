#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.database import engine
from sqlalchemy import text, inspect

def check_database():
    try:
        # Check if database file exists
        print("Checking database connection...")
        
        with engine.connect() as conn:
            # Get table names
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"Tables found: {tables}")
            
            # Check if users table exists and its structure
            if 'users' in tables:
                print("\nUsers table structure:")
                columns = inspector.get_columns('users')
                for col in columns:
                    print(f"  {col['name']}: {col['type']} (nullable: {col['nullable']})")
            else:
                print("Users table not found!")
                
    except Exception as e:
        print(f"Database error: {e}")
        print("Database might not be initialized. Run migrations first.")

if __name__ == "__main__":
    check_database()