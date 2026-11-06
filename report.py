import csv
import os
from datetime import datetime

from file_manager import get_sort_key   


def create_report(files, duplicates, stats, folder_path):

    reports_folder = os.path.join(folder_path, "reports")
    os.makedirs(reports_folder, exist_ok=True)

    report_name = "duplicate_report_" + datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    ) + ".csv"

    report_path = os.path.join(reports_folder, report_name)

    with open(
        report_path, "w", newline="", encoding="utf-8-sig"
    ) as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow([
            "Group Number",
            "File Name",
            "File Size (Bytes)",
            "File Path",
            "Status"
        ])

        for group_number, group in enumerate(duplicates, start=1):

            group = sorted(group, key=get_sort_key)

            for index, file_info in enumerate(group):

                if index == 0:
                    status = "Keep"
                else:
                    status = "Duplicate"

                writer.writerow([
                    group_number,
                    file_info["name"],
                    file_info["size"],
                    file_info["path"],
                    status
                ])

        writer.writerow([])
        writer.writerow(["Statistics"])
        writer.writerow(["Total Files", stats["total_files"]])
        writer.writerow(["Total Size", stats["total_size"]])
        writer.writerow([
            "Duplicate Groups", stats["duplicate_groups"]
        ])
        writer.writerow([
            "Extra Copies", stats["duplicate_count"]
        ])
        writer.writerow([
            "Saved Space (Bytes)", stats["saved_space"]
        ])
        writer.writerow(["Images", stats["images"]])
        writer.writerow(["Videos", stats["videos"]])
        writer.writerow(["Other Files", stats["other_files"]])

    print("\nReport created successfully!")
    print("Report location:", report_path)

    return report_path