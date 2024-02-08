import os
import shutil
import sys
import zipfile

def zip_folder(source_folder, destination_zip):
    try:
        # Check if source folder exists
        if not os.path.exists(source_folder):
            print(f"Source folder '{source_folder}' does not exist.")
            return

        # Remove existing destination zip file if it exists
        if os.path.exists(destination_zip):
            os.remove(destination_zip)

        # Create a zip file and add contents of the source folder
        with zipfile.ZipFile(destination_zip, 'w') as zipf:
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, source_folder))

        print(f"Folder '{source_folder}' zipped to '{destination_zip}' successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <source_folder> <destination_zip>")
        sys.exit(1)

    source_folder = sys.argv[1]
    destination_zip = sys.argv[2]
    zip_folder(source_folder, destination_zip)
