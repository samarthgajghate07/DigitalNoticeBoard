# Digital Notice Board System
# Module 1
import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect("notice_board.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_notice():
    title = input("Enter notice title: ").strip()

    if not title:
        print("Error: Notice title cannot be empty!")
        return

    date = input("Enter notice date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Error: Please enter a valid date in YYYY-MM-DD format!")
        return

    category = input("Enter notice category: ").strip()

    if not category:
        print("Error: Category cannot be empty!")
        return

    message = input("Enter notice message: ").strip()

    if not message:
        print("Error: Notice message cannot be empty!")
        return

    conn = sqlite3.connect("notice_board.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notices (title, date, category, message)
        VALUES (?, ?, ?, ?)
    """, (title, date, category, message))

    conn.commit()
    conn.close()

    print("Notice added successfully!")




def update_notice():
    notice_id = input("Enter the Notice ID to update: ").strip()

    if not notice_id.isdigit():
        print("Error: Please enter a valid Notice ID!")
        return

    conn = sqlite3.connect("notice_board.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM notices WHERE id = ?",
        (notice_id,)
    )
    notice = cursor.fetchone()

    if notice:
        title = input("Enter new title: ").strip()

        if not title:
            print("Error: Title cannot be empty!")
            conn.close()
            return

        date = input("Enter new date (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Error: Invalid date! Use YYYY-MM-DD.")
            conn.close()
            return

        category = input("Enter new category: ").strip()

        if not category:
            print("Error: Category cannot be empty!")
            conn.close()
            return

        message = input("Enter new message: ").strip()

        if not message:
            print("Error: Message cannot be empty!")
            conn.close()
            return

        cursor.execute("""
            UPDATE notices
            SET title = ?, date = ?, category = ?, message = ?
            WHERE id = ?
        """, (title, date, category, message, notice_id))

        conn.commit()
        print("Notice updated successfully!")

    else:
        print("Notice ID not found!")

    conn.close()

def delete_notice():
    notice_id = input("Enter Notice ID to delete: ").strip()

    if not notice_id.isdigit():
        print("Error: Please enter a valid Notice ID!")
        return

    conn = sqlite3.connect("notice_board.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM notices WHERE id = ?",
        (notice_id,)
    )

    notice = cursor.fetchone()

    if not notice:
        print("Notice ID not found!")
        conn.close()
        return

    print("\nNotice Details:")
    print(f"Title: {notice[1]}")
    print(f"Date: {notice[2]}")
    print(f"Category: {notice[3]}")

    confirm = input(
        "Are you sure you want to delete this notice? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        cursor.execute(
            "DELETE FROM notices WHERE id = ?",
            (notice_id,)
        )
        conn.commit()
        print("Notice deleted successfully!")
    else:
        print("Deletion cancelled.")

    conn.close()

def display_notices():
    conn = sqlite3.connect("notice_board.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notices ORDER BY date DESC")
    notices = cursor.fetchall()
    conn.close()

    if not notices:
        print("No notices available!")
        return

    print("\n========== ALL NOTICES ==========")
    for notice in notices:
        print(f"\nID: {notice[0]}")
        print(f"Title: {notice[1]}")
        print(f"Date: {notice[2]}")
        print(f"Category: {notice[3]}")
        print(f"Message: {notice[4]}")
        print("------------------------------")


print("========================================")
print("     DIGITAL NOTICE BOARD SYSTEM        ")
print("========================================")

def filter_notices_by_category():
    print("\nAvailable Categories:")
    print("1. Academic")
    print("2. Examination")
    print("3. Events")
    print("4. Sports")
    print("5. General")

    category_choice = input("Select category: ").strip()

    categories = {
        "1": "Academic",
        "2": "Examination",
        "3": "Events",
        "4": "Sports",
        "5": "General"
    }

    if category_choice not in categories:
        print("Invalid category choice!")
        return

    category = categories[category_choice]

    conn = sqlite3.connect("notice_board.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM notices WHERE category = ? ORDER BY date DESC",
        (category,)
    )

    notices = cursor.fetchall()
    conn.close()

    if not notices:
        print(f"No notices found in the {category} category!")
        return

    print(f"\n========== {category.upper()} NOTICES ==========")

    for notice in notices:
        print(f"\nID: {notice[0]}")
        print(f"Title: {notice[1]}")
        print(f"Date: {notice[2]}")
        print(f"Category: {notice[3]}")
        print(f"Message: {notice[4]}")
        print("-----------------------------------")

def search_notices():
    search_title = input("Enter notice title to search: ").strip()

    conn = sqlite3.connect("notice_board.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM notices WHERE title LIKE ? ORDER BY date DESC",
        ('%' + search_title + '%',)
    )

    notices = cursor.fetchall()
    conn.close()

    if not notices:
        print("No matching notices found!")
        return

    print("\n========== SEARCH RESULTS ==========")

    for notice in notices:
        print(f"\nID: {notice[0]}")
        print(f"Title: {notice[1]}")
        print(f"Date: {notice[2]}")
        print(f"Category: {notice[3]}")
        print(f"Message: {notice[4]}")
        print("-----------------------------------")

create_database()

while True:
    print("\n========== MAIN MENU ==========")
    print("1. View Notices")
    print("2. Add Notice")
    print("3. Update Notice")
    print("4. Delete Notice")
    print("5. Search Notices")
    print("6. Filter Notices by Category")
    print("7. Exit")

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":
        display_notices()
    elif choice == "2":
        add_notice()
    elif choice == "3":
        update_notice()
    elif choice == "4":
        delete_notice()
    elif choice == "5":
        search_notices()
    elif choice == "6":
        filter_notices_by_category()
    elif choice == "7":
        print("Thank you for using Digital Notice Board System.")
        break
    else:
        print("Invalid choice! Please try again.")