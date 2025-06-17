import sys
import json
import os

class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def show_books(self):  # For JSON serialization
        return {
            "type": "Book",
            "Title": self.title,
            "Author": self.author,
            "Year": self.year,
        }

    def __str__(self):
        return f'"{self.title}" by {self.author} ({self.year})'

    @classmethod
    def from_input(cls):
        title = input("Enter title: ").strip()
        while not title:
            print("Title cannot be empty.")
            title = input("Enter title: ").strip()

        author = input("Enter author: ").strip()
        while not author:
            print("Author cannot be empty.")
            author = input("Enter author: ").strip()

        while True:
            year_input = input("Enter year: ").strip()
            try:
                year = int(year_input)
                if year <= 0 or year > 2100:
                    print("Please enter a realistic year (1-2100).")
                else:
                    break
            except ValueError:
                print("Year must be a number.")

        return cls(title, author, year)

class EBook(Book):
    def display_info(self):
        print(f'"{self.title}" by {self.author} (EBook), published in {self.year}')

    def show_books(self):
        data = super().show_books()
        data["type"] = "EBook"
        return data

    @classmethod
    def from_input(cls):
        return super().from_input()

class AudioBook(Book):
    def display_info(self):
        print(f'"{self.title}" by {self.author} (AudioBook), published in {self.year}')

    def show_books(self):
        data = super().show_books()
        data["type"] = "AudioBook"
        return data

    @classmethod
    def from_input(cls):
        return super().from_input()

class BookManager:
    def __init__(self):
        self.books = []
        self.file_name = "library.json"
        self.load_books()

    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    def show_library(self):
        if not self.books:
            print("No books in the library.")
        for book in self.books:
            print(book)

    def find_books(self, name):
        found = False
        for book in self.books:
            if name.lower() in book.title.lower():
                print("Book found:")
                book.display_info()
                found = True
        if not found:
            print(f"No such book with title: {name}")

    def delete_book(self, name):
        for book in self.books:
            if name.lower() == book.title.lower():
                self.books.remove(book)
                print(f'"{book.title}" was removed from the collection.')
                self.save_books()
                return
        print(f'No book found with the title "{name}".')

    def save_books(self):
        # Convert all books to dicts for JSON
        books_data = [book.show_books() for book in self.books]
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(books_data, f, indent=4)
        # print("Library saved.")  # Uncomment if you want debug info

    def load_books(self):
        if not os.path.exists(self.file_name):
            # Load sample books if no file
            self.load_sample_books()
            return

        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                books_data = json.load(f)
            for b in books_data:
                book_type = b.get("type", "Book")
                if book_type == "EBook":
                    book = EBook(b["Title"], b["Author"], b["Year"])
                elif book_type == "AudioBook":
                    book = AudioBook(b["Title"], b["Author"], b["Year"])
                else:
                    book = Book(b["Title"], b["Author"], b["Year"])
                self.books.append(book)
        except (json.JSONDecodeError, FileNotFoundError):
            print("Error reading library.json, loading sample books.")
            self.load_sample_books()

    def load_sample_books(self):
        self.books.clear()
        self.books.append(Book("1984", "George Orwell", 1949))
        self.books.append(EBook("Python Tricks", "Dan Bader", 2017))
        self.books.append(AudioBook("Becoming", "Michelle Obama", 2018))
        self.save_books()

class UserInterface:
    def __init__(self):
        self.manager = BookManager()

    def display_menu(self):
        print("\nWelcome to the Online Library!")
        print("Please choose what you want to do:")
        print("1. View your book collection.")
        print("2. Add book to the collection.")
        print("3. Search book by title.")
        print("4. Delete book from collection.")
        print("5. Exit")

    def answer(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-5): ").strip()
            if choice not in ("1", "2", "3", "4", "5"):
                print("Invalid choice. Please enter a number between 1 and 5.")
                continue

            if choice == "1":
                self.manager.show_library()

            elif choice == "2":
                book_type = input("Add Regular Book, EBook, or AudioBook? (r/e/a): ").strip().lower()
                if book_type == 'e':
                    new_book = EBook.from_input()
                elif book_type == 'a':
                    new_book = AudioBook.from_input()
                else:
                    new_book = Book.from_input()

                self.manager.add_book(new_book)
                print(f'Book "{new_book.title}" added successfully.')

            elif choice == "3":
                check_book = input("Enter a book title to search: ").strip()
                while not check_book:
                    print("Book title cannot be empty.")
                    check_book = input("Enter a book title to search: ").strip()
                self.manager.find_books(check_book)

            elif choice == "4":
                check_book = input("Enter the title of the book to delete: ").strip()
                while not check_book:
                    print("Book title cannot be empty.")
                    check_book = input("Enter the title of the book to delete: ").strip()
                confirm = input(f"Are you sure you want to delete '{check_book}'? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.manager.delete_book(check_book)
                else:
                    print("Deletion cancelled.")

            elif choice == "5":
                print("Exiting system")
                sys.exit()

if __name__ == "__main__":
    ui = UserInterface()
    ui.answer()
