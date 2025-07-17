#!/usr/bin/env python3
"""
Utilities package for VersaAI backend
"""

from .demo_setup import initialize_demo_users, get_demo_user_credentials, log_demo_mode_info

__all__ = [
    "initialize_demo_users",
    "get_demo_user_credentials", 
    "log_demo_mode_info"
]