# File Organization System

A Python GUI application that helps you organize files in a directory based on their types. The system automatically categorizes files into subdirectories according to their extensions, making it easier to keep your folders tidy.

## Features

- **Automatic File Categorization**: Organizes files into folders based on their extensions
- **Customizable Categories**: Add, edit, or delete file categories and their associated extensions
- **Preview Function**: See how files will be organized before committing
- **Persistent Settings**: Custom categories are saved for future use
- **Conflict Resolution**: Handles filename conflicts by adding numbers to duplicates
- **Progress Feedback**: Shows organization progress and results
- **Threaded Operations**: File organization runs in a separate thread to keep UI responsive

## Requirements

- Python 3.6 or higher
- tkinter (usually comes pre-installed with Python)
- Pillow (PIL) package

## Installation

1. Clone or download this repository
2. Install the required package:
   ```
   pip install pillow
   ```

## Usage

1. Run the script:
   ```
   python file_organizer.py
   ```

2. Click "Browse" to select a directory you want to organize

3. Customize the file categories if needed:
   - Click "Add Category" to create a new category
   - Select a category and click "Edit Category" to modify it
   - Select a category and click "Delete Category" to remove it
   - Click "Reset to Default" to restore the original categories

4. Preview the file distribution in the preview section

5. Click "Organize Files" to start the organization process

6. Confirm the operation when prompted

7. Wait for the process to complete - you'll see a status update and a confirmation message

## Default Categories

The application comes with the following default categories:

- **Images**: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp
- **Documents**: .pdf, .doc, .docx, .txt, .rtf, .odt, .xls, .xlsx, .ppt, .pptx
- **Videos**: .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm
- **Audio**: .mp3, .wav, .flac, .aac, .ogg, .wma
- **Archives**: .zip, .rar, .7z, .tar, .gz
- **Code**: .py, .js, .html, .css, .java, .cpp, .c, .php, .rb, .go
- **Others**: All other file types

## How It Works

1. The application scans the selected directory for files
2. Each file is categorized based on its extension
3. Subdirectories are created for each category if they don't exist
4. Files are moved to their appropriate category directories
5. Files that don't match any category are moved to an "Others" folder
6. If a file with the same name already exists in the destination, a number is added to resolve the conflict

## Configuration

Custom categories are saved in a file named `file_categories.json` in the same directory as the script. This file is created automatically when you modify the categories.

## Troubleshooting

- **Permission Errors**: Make sure you have read and write permissions for the directory you're trying to organize
- **Invalid Directory**: Ensure the selected directory exists and is accessible
- **Large Directories**: For directories with many files, the organization process might take some time
