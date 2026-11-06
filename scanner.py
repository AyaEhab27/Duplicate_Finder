
import os

def scan_files(folder_path):
    files = []

    for folder, subfolders, filenames in os.walk(folder_path):

        subfolders[:] = [
            name for name in subfolders
            if name not in ["duplicate", "reports"]
        ]

        for filename in filenames:
            file_path = os.path.join(folder, filename)

            try:
                file_size = os.path.getsize(file_path)

                file_info = {
                    "name": filename,
                    "path": file_path,
                    "size": file_size
                }

                files.append(file_info)

            except OSError:
                print("Could not read:", file_path)

    return files
