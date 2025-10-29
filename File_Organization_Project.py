import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from datetime import datetime
import mimetypes
from PIL import Image, ImageTk
import threading


class FileOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organization System")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")

        # Default file type categories
        self.default_categories = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", ".rb", ".go"],
            "Others": []
        }

        # Load custom categories if exists
        self.categories_file = "file_categories.json"
        self.categories = self.load_categories()

        # Selected directory
        self.selected_dir = tk.StringVar()

        # Preview variables
        self.preview_frame = None
        self.preview_label = None

        # Create UI
        self.create_widgets()

    def load_categories(self):
        """Load custom categories from file if exists, otherwise use defaults"""
        if os.path.exists(self.categories_file):
            try:
                with open(self.categories_file, 'r') as f:
                    return json.load(f)
            except:
                return self.default_categories.copy()
        return self.default_categories.copy()

    def save_categories(self):
        """Save current categories to file"""
        with open(self.categories_file, 'w') as f:
            json.dump(self.categories, f)

    def create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(main_frame, text="File Organization System",
                               font=("Arial", 18, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        # Directory selection frame
        dir_frame = ttk.Frame(main_frame)
        dir_frame.pack(fill=tk.X, pady=10)

        tk.Label(dir_frame, text="Select Directory:").pack(side=tk.LEFT, padx=5)
        tk.Entry(dir_frame, textvariable=self.selected_dir, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Button(dir_frame, text="Browse", command=self.browse_directory).pack(side=tk.LEFT, padx=5)

        # Categories frame
        categories_frame = ttk.LabelFrame(main_frame, text="File Categories", padding="10")
        categories_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create treeview for categories
        self.tree = ttk.Treeview(categories_frame, columns=("Extensions",), height=8)
        self.tree.heading("#0", text="Category")
        self.tree.heading("Extensions", text="File Extensions")
        self.tree.column("#0", width=150)
        self.tree.column("Extensions", width=300)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(categories_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Populate treeview with categories
        self.populate_treeview()

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="Add Category", command=self.add_category).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Edit Category", command=self.edit_category).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Delete Category", command=self.delete_category).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Reset to Default", command=self.reset_categories).pack(side=tk.LEFT, padx=5)

        # Preview frame
        self.preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.preview_label = tk.Label(self.preview_frame, text="No preview available",
                                      bg="white", width=50, height=10)
        self.preview_label.pack(fill=tk.BOTH, expand=True)

        # Organize button
        organize_frame = ttk.Frame(main_frame)
        organize_frame.pack(fill=tk.X, pady=10)

        self.organize_button = tk.Button(organize_frame, text="Organize Files",
                                         command=self.organize_files,
                                         bg="#4CAF50", fg="white",
                                         font=("Arial", 12, "bold"),
                                         padx=20, pady=10)
        self.organize_button.pack()

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(main_frame, textvariable=self.status_var,
                              bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def populate_treeview(self):
        """Populate the treeview with categories"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add categories
        for category, extensions in self.categories.items():
            ext_str = ", ".join(extensions) if extensions else "All other files"
            self.tree.insert("", tk.END, text=category, values=(ext_str,))

    def browse_directory(self):
        """Open directory dialog to select a directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.selected_dir.set(directory)
            self.preview_directory()

    def preview_directory(self):
        """Preview the selected directory"""
        directory = self.selected_dir.get()
        if not directory or not os.path.isdir(directory):
            self.preview_label.config(text="Invalid directory")
            return

        # Count files by category
        file_counts = {category: 0 for category in self.categories}
        file_counts["Uncategorized"] = 0

        try:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    _, ext = os.path.splitext(filename)
                    ext = ext.lower()

                    categorized = False
                    for category, extensions in self.categories.items():
                        if ext in extensions:
                            file_counts[category] += 1
                            categorized = True
                            break

                    if not categorized:
                        file_counts["Uncategorized"] += 1

            # Display preview
            preview_text = f"Directory: {directory}\n\n"
            preview_text += "File Distribution:\n"

            for category, count in file_counts.items():
                if count > 0:
                    preview_text += f"{category}: {count} files\n"

            self.preview_label.config(text=preview_text, justify=tk.LEFT)
        except Exception as e:
            self.preview_label.config(text=f"Error: {str(e)}")

    def add_category(self):
        """Add a new category"""
        dialog = CategoryDialog(self.root, "Add Category")
        self.root.wait_window(dialog.dialog)

        if dialog.result:
            category, extensions = dialog.result
            self.categories[category] = extensions
            self.save_categories()
            self.populate_treeview()

    def edit_category(self):
        """Edit selected category"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a category to edit.")
            return

        category = self.tree.item(selected[0])["text"]
        extensions = self.categories[category]

        dialog = CategoryDialog(self.root, "Edit Category", category, extensions)
        self.root.wait_window(dialog.dialog)

        if dialog.result:
            new_category, new_extensions = dialog.result
            if new_category != category:
                del self.categories[category]
            self.categories[new_category] = new_extensions
            self.save_categories()
            self.populate_treeview()

    def delete_category(self):
        """Delete selected category"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a category to delete.")
            return

        category = self.tree.item(selected[0])["text"]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the '{category}' category?"):
            del self.categories[category]
            self.save_categories()
            self.populate_treeview()

    def reset_categories(self):
        """Reset categories to default"""
        if messagebox.askyesno("Reset Categories", "Are you sure you want to reset to default categories?"):
            self.categories = self.default_categories.copy()
            self.save_categories()
            self.populate_treeview()

    def organize_files(self):
        """Organize files in the selected directory"""
        directory = self.selected_dir.get()
        if not directory or not os.path.isdir(directory):
            messagebox.showerror("Invalid Directory", "Please select a valid directory.")
            return

        # Confirm organization
        if not messagebox.askyesno("Confirm Organization",
                                   f"This will organize files in '{directory}'.\n\n"
                                   "Files will be moved to subdirectories based on their categories.\n\n"
                                   "Do you want to continue?"):
            return

        # Disable button during organization
        self.organize_button.config(state=tk.DISABLED)
        self.status_var.set("Organizing files...")

        # Run organization in a separate thread to keep UI responsive
        threading.Thread(target=self._organize_files_thread, args=(directory,), daemon=True).start()

    def _organize_files_thread(self, directory):
        """Thread function to organize files"""
        try:
            # Create category directories if they don't exist
            for category in self.categories:
                category_dir = os.path.join(directory, category)
                if not os.path.exists(category_dir):
                    os.makedirs(category_dir)

            # Create "Others" directory if it doesn't exist
            others_dir = os.path.join(directory, "Others")
            if not os.path.exists(others_dir):
                os.makedirs(others_dir)

            # Move files to appropriate directories
            moved_files = 0
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    _, ext = os.path.splitext(filename)
                    ext = ext.lower()

                    categorized = False
                    for category, extensions in self.categories.items():
                        if ext in extensions:
                            dest_dir = os.path.join(directory, category)
                            dest_path = os.path.join(dest_dir, filename)

                            # Handle filename conflicts
                            counter = 1
                            while os.path.exists(dest_path):
                                name, ext = os.path.splitext(filename)
                                dest_path = os.path.join(dest_dir, f"{name}_{counter}{ext}")
                                counter += 1

                            shutil.move(filepath, dest_path)
                            moved_files += 1
                            categorized = True
                            break

                    if not categorized:
                        dest_path = os.path.join(others_dir, filename)

                        # Handle filename conflicts
                        counter = 1
                        while os.path.exists(dest_path):
                            name, ext = os.path.splitext(filename)
                            dest_path = os.path.join(others_dir, f"{name}_{counter}{ext}")
                            counter += 1

                        shutil.move(filepath, dest_path)
                        moved_files += 1

            # Update UI
            self.root.after(0, lambda: self.status_var.set(f"Organization complete. Moved {moved_files} files."))
            self.root.after(0, lambda: self.organize_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.preview_directory())
            self.root.after(0, lambda: messagebox.showinfo("Organization Complete",
                                                           f"Successfully organized {moved_files} files."))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
            self.root.after(0, lambda: self.organize_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))


class CategoryDialog:
    def __init__(self, parent, title, category="", extensions=None):
        self.result = None

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)

        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Category name
        tk.Label(self.dialog, text="Category Name:").pack(pady=10)
        self.category_entry = tk.Entry(self.dialog, width=30)
        self.category_entry.pack(pady=5)
        self.category_entry.insert(0, category)

        # Extensions
        tk.Label(self.dialog, text="File Extensions (comma-separated, e.g., .jpg,.png):").pack(pady=10)
        self.extensions_text = tk.Text(self.dialog, width=40, height=10)
        self.extensions_text.pack(pady=5)

        if extensions:
            self.extensions_text.insert(tk.END, ", ".join(extensions))

        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)

        # Focus on category entry
        self.category_entry.focus()

    def ok_clicked(self):
        category = self.category_entry.get().strip()
        if not category:
            messagebox.showwarning("Invalid Input", "Please enter a category name.")
            return

        extensions_str = self.extensions_text.get("1.0", tk.END).strip()
        extensions = [ext.strip() for ext in extensions_str.split(",") if ext.strip()]

        # Ensure extensions start with a dot
        for i, ext in enumerate(extensions):
            if not ext.startswith("."):
                extensions[i] = f".{ext}"

        self.result = (category, extensions)
        self.dialog.destroy()

    def cancel_clicked(self):
        self.dialog.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizer(root)
    root.mainloop()