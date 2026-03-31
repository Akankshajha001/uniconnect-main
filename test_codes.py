"""
Test script - Verify database connectivity and data
"""

from database.lost_found_db import get_all_items
from database.notes_db import get_all_notes

print("=== Lost & Found Items ===\n")
items = get_all_items()
for item in items:
    print(f"ID: #{item['id']} | Type: {item['type']} | Category: {item['category']} | Status: {item['status']}")

print(f"\nTotal items: {len(items)}")

print("\n=== Notes ===\n")
notes = get_all_notes()
for note in notes:
    print(f"ID: #{note['id']} | Subject: {note['subject']} | File: {note['file_name']} | Downloads: {note['downloads']}")

print(f"\nTotal notes: {len(notes)}")
