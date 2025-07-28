
class Author:
    def __init__(self, name):
        self.name = name

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False

    def borrow(self):
        if not self.is_borrowed:
            self.is_borrowed = True
            print(f"You borrowed '{self.title}' by {self.author.name}.")
        else:
            print(f"Sorry, '{self.title}' is already borrowed. There's always Anna's Archive.")

    def return_book(self):
        if self.is_borrowed:
            self.is_borrowed = False
            print(f"You returned '{self.title}'. Finally, someone who we don't need to send someone after!")
        else:
            print(f"Hold up...what kind of shumuck tries to return a book they NEVER borrowed? Get outta here, and take '{self.title}', with you.")


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def display_books(self):
        if not self.books:
            print("No books available in the library.")
        else:
            print("Available books:")
            for idx, book in enumerate(self.books, start=1):
                status = "Available" if not book.is_borrowed else "Borrowed"
                print(f"{idx}. {book.title} by {book.author.name} - {status}")

    def borrow_book(self, book_number):
        if 1 <= book_number <= len(self.books):
            self.books[book_number - 1].borrow()
        else:
            print("Invalid book number.")

    def return_book(self, book_number):
        if 1 <= book_number <= len(self.books):
            self.books[book_number - 1].return_book()
        else:
            print("Invalid book number.")


def library_menu(library):
    while True:
        print("\nLibrary Menu:")
        print("1. Display Books")
        print("2. Borrow a Book")
        print("3. Return a Book")
        print("4. Exit")

        try:
            choice = int(input("Enter choice (1-4): "))
            if choice == 1:
                library.display_books()
            elif choice == 2:
                book_number = int(input("Enter book number to borrow: "))
                library.borrow_book(book_number)
            elif choice == 3:
                book_number = int(input("Enter book number to return: "))
                library.return_book(book_number)
            elif choice == 4:
                print("Exiting library system.")
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Enter a number next time, square?")

#adding books
library = Library()
author1 = Author("George Orwell")
author2 = Author("Maurice LeBlanc")
library.add_book(Book("1984", author1))
library.add_book(Book("Arsene Lupin Vs. Sherlock Holmes", author2))

library_menu(library)

print("THERE'S NO ERROR HERE!")