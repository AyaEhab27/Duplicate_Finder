
import os

from scanner import scan_files
from duplicate_checker import find_duplicates
from statistics import calculate_statistics, show_statistics
from file_manager import move_duplicates
from report import create_report


def main():

    print("================================")
    print("     Duplicate Files Finder     ")
    print("================================")

    folder_path = input(
        "\nEnter folder path to scan: "
    ).strip().strip('"')

    if not os.path.isdir(folder_path):
        print("Error: Folder does not exist.")
        return

    folder_path = os.path.abspath(folder_path)

    print("\nScanning files...")

    files = scan_files(folder_path)

    print("Total files found:", len(files))

    if not files:
        print("No files found!")
        return

    print("\nChecking for duplicates...")

    duplicates = find_duplicates(files)

    if not duplicates:
        print("\nNo duplicate files found.")

    else:
        print("\nDuplicate files found")

        for group_number, group in enumerate(duplicates, start=1):

            print("\nGroup", group_number)

            for file_info in group:
                print("Name:", file_info["name"])
                print("Size:", file_info["size"], "Bytes")
                print("Path:", file_info["path"])
                print("-------------------------")

    stats = calculate_statistics(files, duplicates)

    show_statistics(stats)

    create_report(files, duplicates, stats, folder_path)

    if duplicates:

        choice = input(
            "\nDo you want to move duplicate files to duplicate folder? (y/n): "
        ).strip().lower()

        if choice == "y":

            print("\nMoving duplicate files...")

            moved_files = move_duplicates(
                duplicates, folder_path
            )

            print("\nFiles moved:", len(moved_files))
            print("Duplicate files moved successfully")

        else:
            print("\nNo files were moved.")

    print("\nProgram finished")


if __name__ == "__main__":
    main()
