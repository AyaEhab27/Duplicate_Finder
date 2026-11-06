
from file_manager import get_sort_key


def calculate_statistics(files, duplicates):

    total_size = 0
    duplicate_count = 0
    duplicate_groups = len(duplicates)
    saved_space = 0

    images = 0
    videos = 0
    other_files = 0

    image_extensions = [
        ".jpg", ".jpeg", ".png", ".gif",
        ".bmp", ".webp"
    ]

    video_extensions = [
        ".mp4", ".avi", ".mkv",
        ".mov", ".wmv"
    ]

    for file_info in files:
        total_size += file_info["size"]

        extension = file_info["name"].lower().split(".")[-1]
        extension = "." + extension

        if extension in image_extensions:
            images += 1

        elif extension in video_extensions:
            videos += 1

        else:
            other_files += 1

    for group in duplicates:

        group = sorted(group, key=get_sort_key)
        duplicate_count += len(group) - 1

        saved_space += sum(
            file_info["size"] for file_info in group[1:]
        )

    stats = {
        "total_files": len(files),
        "total_size": total_size,
        "duplicate_groups": duplicate_groups,
        "duplicate_count": duplicate_count,
        "saved_space": saved_space,
        "images": images,
        "videos": videos,
        "other_files": other_files
    }

    return stats


def format_size(size):
    if size < 1024:
        return str(round(size, 2)) + " B"

    elif size < 1024 ** 2:
        return str(round(size / 1024, 2)) + " KB"

    elif size < 1024 ** 3:
        return str(round(size / (1024 ** 2), 2)) + " MB"

    else:
        return str(round(size / (1024 ** 3), 2)) + " GB"


def show_statistics(stats):

    print("\n========== Statistics ==========")

    print("Total files:", stats["total_files"])
    print("Total size:", format_size(stats["total_size"]))

    print("Images:", stats["images"])
    print("Videos:", stats["videos"])
    print("Other files:", stats["other_files"])

    print("Duplicate groups:", stats["duplicate_groups"])
    print("Extra copies:", stats["duplicate_count"])

    print("Space that can be saved:",
          format_size(stats["saved_space"]))

    print("================================")
