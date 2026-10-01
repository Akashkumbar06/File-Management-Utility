import os
import shutil
from pathlib import Path
from datetime import datetime


# ============================================================
# FILE MANAGEMENT UTILITY
# ============================================================

class FileManager:
    """
    A simple file management utility using Python.
    
    Features:
    - List files and folders
    - Create folders
    - Create files
    - Rename files/folders
    - Copy files/folders
    - Move files/folders
    - Delete files/folders
    - Search files
    - Display file information
    """

    def __init__(self):
        self.current_path = Path.cwd()

    # --------------------------------------------------------
    # INPUT VALIDATION
    # --------------------------------------------------------

    def validate_path(self, path):
        """Validate and return a Path object."""
        try:
            path = Path(path)

            if not path.exists():
                print("❌ Error: Path does not exist.")
                return None

            return path

        except Exception as e:
            print(f"❌ Invalid path: {e}")
            return None

    def validate_name(self, name):
        """Validate file/folder name."""
        if not name or not name.strip():
            print("❌ Name cannot be empty.")
            return False

        invalid_characters = '<>:"/\\|?*'

        if any(char in name for char in invalid_characters):
            print("❌ Name contains invalid characters.")
            return False

        return True

    # --------------------------------------------------------
    # DATA PROCESSING - LIST FILES
    # --------------------------------------------------------

    def list_files(self, directory=None):
        """Display all files and folders in a directory."""

        if directory is None:
            directory = self.current_path
        else:
            directory = self.validate_path(directory)

        if directory is None:
            return

        if not directory.is_dir():
            print("❌ The selected path is not a directory.")
            return

        try:
            items = list(directory.iterdir())

            if not items:
                print("\n📂 Folder is empty.")
                return

            print("\n" + "=" * 65)
            print(f"📁 CONTENTS OF: {directory}")
            print("=" * 65)

            for item in sorted(items):
                if item.is_dir():
                    print(f"📁 [FOLDER] {item.name}")
                else:
                    size = item.stat().st_size
                    print(f"📄 [FILE]   {item.name:<35} {size} bytes")

            print("=" * 65)

        except PermissionError:
            print("❌ Permission denied.")
        except Exception as e:
            print(f"❌ Error reading directory: {e}")

    # --------------------------------------------------------
    # CREATE FOLDER
    # --------------------------------------------------------

    def create_folder(self, folder_name):
        """Create a new folder."""

        if not self.validate_name(folder_name):
            return

        folder_path = self.current_path / folder_name

        try:
            if folder_path.exists():
                print("❌ Folder already exists.")
                return

            folder_path.mkdir()
            print(f"✅ Folder '{folder_name}' created successfully.")

        except PermissionError:
            print("❌ Permission denied.")
        except Exception as e:
            print(f"❌ Error creating folder: {e}")

    # --------------------------------------------------------
    # CREATE FILE
    # --------------------------------------------------------

    def create_file(self, file_name):
        """Create an empty file."""

        if not self.validate_name(file_name):
            return

        file_path = self.current_path / file_name

        try:
            if file_path.exists():
                print("❌ File already exists.")
                return

            file_path.touch()
            print(f"✅ File '{file_name}' created successfully.")

        except PermissionError:
            print("❌ Permission denied.")
        except Exception as e:
            print(f"❌ Error creating file: {e}")

    # --------------------------------------------------------
    # RENAME
    # --------------------------------------------------------

    def rename_item(self, old_name, new_name):
        """Rename a file or folder."""

        if not self.validate_name(new_name):
            return

        old_path = self.current_path / old_name
        new_path = self.current_path / new_name

        try:
            if not old_path.exists():
                print("❌ File or folder does not exist.")
                return

            if new_path.exists():
                print("❌ Destination name already exists.")
                return

            old_path.rename(new_path)

            print(f"✅ Renamed '{old_name}' → '{new_name}'")

        except PermissionError:
            print("❌ Permission denied.")
        except Exception as e:
            print(f"❌ Error renaming item: {e}")

    # --------------------------------------------------------
    # COPY
    # --------------------------------------------------------

    def copy_item(self, source, destination):
        """Copy a file or folder."""

        source_path = self.validate_path(source)

        if source_path is None:
            return

        destination_path = Path(destination)

        try:
            if source_path.is_file():
                shutil.copy2(source_path, destination_path)
            elif source_path.is_dir():
                shutil.copytree(source_path, destination_path)
            else:
                print("❌ Unsupported file type.")
                return

            print("✅ Copy operation completed successfully.")

        except FileExistsError:
            print("❌ Destination already exists.")
        except PermissionError:
            print("❌ Permission denied.")
        except Exception as e:
            print(f"❌ Error copying item: {e}")

    # --------------------------------------------------------
    # MOVE
    # --------------------------------------------------------

    def move_item(self, source, destination):
        """Move a file or folder."""

        source_path = self.validate_path(source)

        if source_path is None:
            return

        try:
            shutil.move(str(source_path), destination)
            print("✅ Move operation completed successfully.")

        except PermissionError:
            print("❌ Permission denied.")
        except Exception as e:
            print(f"❌ Error moving item: {e}")

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------

    def delete_item(self, name):
        """Delete a file or folder."""

        item_path = self.current_path / name

        try:
            if not item_path.exists():
                print("❌ File or folder does not exist.")
                return

            confirmation = input(
                f"⚠️ Are you sure you want to delete '{name}'? (y/n): "
            ).lower()

            if confirmation != "y":
                print("❌ Delete operation cancelled.")
                return

            if item_path.is_file():
                item_path.unlink()
            elif item_path.is_dir():
                shutil.rmtree(item_path)

            print(f"✅ '{name}' deleted successfully.")

        except PermissionError:
            print("❌ Permission denied.")
        except Exception as e:
            print(f"❌ Error deleting item: {e}")

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    def search_files(self, keyword):
        """Search files and folders by name."""

        if not keyword.strip():
            print("❌ Search keyword cannot be empty.")
            return

        print(f"\n🔍 Searching for: {keyword}")
        print("-" * 50)

        found = False

        try:
            for item in self.current_path.rglob("*"):
                if keyword.lower() in item.name.lower():
                    print(f"📌 {item}")
                    found = True

            if not found:
                print("❌ No matching files or folders found.")

        except PermissionError:
            print("❌ Permission denied.")
        except Exception as e:
            print(f"❌ Search error: {e}")

    # --------------------------------------------------------
    # FILE INFORMATION
    # --------------------------------------------------------

    def file_information(self, name):
        """Display detailed information about a file."""

        path = self.current_path / name

        if not path.exists():
            print("❌ File or folder does not exist.")
            return

        try:
            information = path.stat()

            print("\n" + "=" * 50)
            print("📋 FILE INFORMATION")
            print("=" * 50)

            print(f"Name       : {path.name}")
            print(f"Location   : {path.parent}")
            print(
                f"Type       : "
                f"{'Folder' if path.is_dir() else 'File'}"
            )
            print(f"Size       : {information.st_size} bytes")

            modified = datetime.fromtimestamp(
                information.st_mtime
            )

            print(
                f"Modified   : "
                f"{modified.strftime('%d-%m-%Y %H:%M:%S')}"
            )

            print("=" * 50)

        except PermissionError:
            print("❌ Permission denied.")
        except Exception as e:
            print(f"❌ Error getting information: {e}")

    # --------------------------------------------------------
    # CHANGE DIRECTORY
    # --------------------------------------------------------

    def change_directory(self, path):
        """Change current working directory."""

        new_path = Path(path).expanduser()

        try:
            if not new_path.exists():
                print("❌ Directory does not exist.")
                return

            if not new_path.is_dir():
                print("❌ Path is not a directory.")
                return

            self.current_path = new_path.resolve()

            print(f"✅ Current directory: {self.current_path}")

        except PermissionError:
            print("❌ Permission denied.")
        except Exception as e:
            print(f"❌ Error changing directory: {e}")


# ============================================================
# USER INTERFACE
# ============================================================

def display_menu():
    print("\n")
    print("=" * 65)
    print("             📁 FILE MANAGEMENT UTILITY")
    print("=" * 65)
    print("1.  List files and folders")
    print("2.  Create folder")
    print("3.  Create file")
    print("4.  Rename file/folder")
    print("5.  Copy file/folder")
    print("6.  Move file/folder")
    print("7.  Delete file/folder")
    print("8.  Search files")
    print("9.  File information")
    print("10. Change directory")
    print("11. Show current directory")
    print("0.  Exit")
    print("=" * 65)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    manager = FileManager()

    print("\n🎉 Welcome to File Management Utility!")
    print(f"📂 Starting Directory: {manager.current_path}")

    while True:

        display_menu()

        try:
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                manager.list_files()

            elif choice == "2":
                name = input("Enter folder name: ").strip()
                manager.create_folder(name)

            elif choice == "3":
                name = input("Enter file name: ").strip()
                manager.create_file(name)

            elif choice == "4":
                old_name = input("Enter current name: ").strip()
                new_name = input("Enter new name: ").strip()
                manager.rename_item(old_name, new_name)

            elif choice == "5":
                source = input("Enter source path: ").strip()
                destination = input("Enter destination path: ").strip()
                manager.copy_item(source, destination)

            elif choice == "6":
                source = input("Enter source path: ").strip()
                destination = input("Enter destination path: ").strip()
                manager.move_item(source, destination)

            elif choice == "7":
                name = input("Enter file/folder name: ").strip()
                manager.delete_item(name)

            elif choice == "8":
                keyword = input("Enter search keyword: ").strip()
                manager.search_files(keyword)

            elif choice == "9":
                name = input("Enter file/folder name: ").strip()
                manager.file_information(name)

            elif choice == "10":
                path = input("Enter directory path: ").strip()
                manager.change_directory(path)

            elif choice == "11":
                print(f"\n📂 Current Directory:")
                print(manager.current_path)

            elif choice == "0":
                print("👋 Exiting File Management Utility. Goodbye!")
                break

            else:
                print("❌ Invalid choice. Please try again.")

        except Exception as error:
            print(f"❌ Error: {error}")
            