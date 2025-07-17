#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.database import engine
from sqlalchemy import text

def check_users():
    try:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT COUNT(*) FROM users'))
            count = result.scalar()
            print(f'Total users in database: {count}')
            
            if count > 0:
                result = conn.execute(text('SELECT id, email, username, full_name, is_active FROM users LIMIT 5'))
                users = result.fetchall()
                print('\nFirst 5 users:')
                for user in users:
                    print(f'  ID: {user[0]}, Email: {user[1]}, Username: {user[2]}, Name: {user[3]}, Active: {user[4]}')
            else:
                print('No users found in database.')
                
    except Exception as e:
        print(f'Error checking users: {e}')

if __name__ == '__main__':
    check_users()