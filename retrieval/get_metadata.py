from pathlib import Path
from datetime import datetime


class FileMetadata:

    def __init__(self, path_file):
        """ class that makes the metadata of file accessible - init with path of single file"""
        self.path_file = Path(path_file)
        if not self.path_file.exists():
            raise FileNotFoundError(f"the path file: {path_file} does not exists")


    def name(self):
        return self.path_file.name


    def size(self):
        size = self.path_file.stat().st_size
        size_by_KB = format(size/1024, ".2f") + " KB"
        return size_by_KB


    def creation_date(self):
        creation_date = self.path_file.stat().st_ctime
        new_format_creation_date = datetime.fromtimestamp(creation_date)
        return new_format_creation_date


    def modified_date(self):
        modified_date = self.path_file.stat().st_mtime
        new_format_modified_date = datetime.fromtimestamp(modified_date)
        return new_format_modified_date


    def last_access_date(self):
        last_access_date = self.path_file.stat().st_mtime
        new_format_last_access_date = datetime.fromtimestamp(last_access_date)
        return new_format_last_access_date