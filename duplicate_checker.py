
import hashlib

def get_file_hash(file_path):
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while True:
                data = file.read(4096)

                if not data:
                    break

                sha256.update(data)

        return sha256.hexdigest()

    except OSError:
        return None


def find_duplicates(files):
    size_groups = {}

    for file_info in files:
        size = file_info["size"]

        if size not in size_groups:
            size_groups[size] = []

        size_groups[size].append(file_info)

    duplicates = []

    for group in size_groups.values():

        if len(group) > 1:

            hash_groups = {}

            for file_info in group:
                file_hash = get_file_hash(file_info["path"])

                if file_hash is None:
                    continue

                if file_hash not in hash_groups:
                    hash_groups[file_hash] = []

                hash_groups[file_hash].append(file_info)

            for same_files in hash_groups.values():

                if len(same_files) > 1:
                    duplicates.append(same_files)

    return duplicates
