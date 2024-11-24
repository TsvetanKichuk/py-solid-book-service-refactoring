import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class Book:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content


class DisplayStrategy(ABC):
    @abstractmethod
    def display(self, content: str) -> None:
        pass


class ConsoleDisplay(DisplayStrategy):
    def display(self, content: str) -> None:
        print(content)


class ReverseConsoleDisplay(DisplayStrategy):
    def display(self, content: str) -> None:
        print(content[::-1])


class PrintStrategy(ABC):
    @abstractmethod
    def print_book(self, title: str, content: str) -> None:
        pass


class ConsolePrint(PrintStrategy):
    def print_book(self, title: str, content: str) -> None:
        print(f"Printing the book: {title}...")
        print(content)


class ReverseConsolePrint(PrintStrategy):
    def print_book(self, title: str, content: str) -> None:
        print(f"Printing the book in reverse: {title}...")
        print(content[::-1])


class SerializeStrategy(ABC):
    @abstractmethod
    def serialize(self, book: Book) -> str:
        pass


class JsonSerialize(SerializeStrategy):
    def serialize(self, book: Book) -> str:
        return json.dumps({"title": book.title, "content": book.content})


class XmlSerialize(SerializeStrategy):
    def serialize(self, book: Book) -> str:
        root = ET.Element("book")
        title = ET.SubElement(root, "title")
        title.text = book.title
        content = ET.SubElement(root, "content")
        content.text = book.content
        return ET.tostring(root, encoding="unicode")


class BookProcessor:
    def __init__(self, book: Book, display_strategy: DisplayStrategy, print_strategy: PrintStrategy,
                 serialize_strategy: SerializeStrategy):
        self.book = book
        self.display_strategy = display_strategy
        self.print_strategy = print_strategy
        self.serialize_strategy = serialize_strategy

    def display(self) -> None:
        self.display_strategy.display(self.book.content)

    def print_book(self) -> None:
        self.print_strategy.print_book(self.book.title, self.book.content)

    def serialize(self) -> str:
        return self.serialize_strategy.serialize(self.book)


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    display_strategy = ConsoleDisplay()
    print_strategy = ConsolePrint()
    serialize_strategy = JsonSerialize()

    for cmd, method_type in commands:
        if cmd == "display":
            if method_type == "reverse":
                display_strategy = ReverseConsoleDisplay()
            else:
                display_strategy = ConsoleDisplay()
            bp = BookProcessor(book, display_strategy, print_strategy, serialize_strategy)
            bp.display()
        elif cmd == "print":
            if method_type == "reverse":
                print_strategy = ReverseConsolePrint()
            else:
                print_strategy = ConsolePrint()
            bp = BookProcessor(book, display_strategy, print_strategy, serialize_strategy)
            bp.print_book()
        elif cmd == "serialize":
            if method_type == "xml":
                serialize_strategy = XmlSerialize()
            else:
                serialize_strategy = JsonSerialize()
            bp = BookProcessor(book, display_strategy, print_strategy, serialize_strategy)
            return bp.serialize()


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
