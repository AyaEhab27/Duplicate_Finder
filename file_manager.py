import os
import re
import shutil


COPY_PATTERNS_SUFFIX = [
    r"\(\d+\)$",                      # fileName (1)
    r"[-_ ]+copy(\s*\(\d+\))?$",      # fileName - copy  /  fileName - copy (2)  /  fileName_copy
    r"[-_ ]+copy\s*\d+$",             # fileName - copy 2
    r"\(copy(\s*\d+)?\)$",            # fileName (copy)  /  fileName (copy 2)
    r"[-_ ]+\d+$",                    # fileName - 1  /  fileName_1
]

COPY_PATTERNS_PREFIX = [
    r"^copy\s+of\s+",                 # Copy of fileName
]


def is_copy_name(filename):
    name_without_ext = os.path.splitext(filename)[0]
    name_lower = name_without_ext.lower()

    for pattern in COPY_PATTERNS_SUFFIX:
        if re.search(pattern, name_lower):
            return True

    for pattern in COPY_PATTERNS_PREFIX:
        if re.search(pattern, name_lower):
            return True

    return False


def get_sort_key(file_info):
   
    try:
        mtime = os.path.getmtime(file_info["path"])
    except OSError:
        mtime = 0   

    return (
        is_copy_name(file_info["name"]),
        mtime,
        file_info["name"],
    )


def move_duplicates(duplicates, folder_path):

    quarantine_folder = os.path.join(
        folder_path, "duplicate"
    )

    os.makedirs(quarantine_folder, exist_ok=True)

    moved_files = []

    for group in duplicates:

        group = sorted(group, key=get_sort_key)

        for file_info in group[1:]:

            source_path = file_info["path"]

            try:
                relative_path = os.path.relpath(
                    source_path, folder_path
                )

                destination_path = os.path.join(
                    quarantine_folder, relative_path
                )

                destination_folder = os.path.dirname(
                    destination_path
                )

                os.makedirs(destination_folder, exist_ok=True)

                if os.path.exists(destination_path):
                    name, extension = os.path.splitext(
                        destination_path
                    )

                    number = 1

                    while os.path.exists(destination_path):
                        destination_path = (
                            name + "_" + str(number) + extension
                        )
                        number += 1

                shutil.move(source_path, destination_path)

                moved_files.append({
                    "original_path": source_path,
                    "new_path": destination_path
                })

                print("Moved duplicate:", source_path)

            except OSError as error:
                print("Could not move file:", error)

    return moved_files