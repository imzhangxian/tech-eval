# coding: utf-8
import glob
import os
import re

# Rename all SHAR files into pattern : code-name-date(if any).pdf
# IMPORTANT: Only need to run once to rename all  files.

rename_regex = re.compile(r"(?P<code>\d{6})(.SH)?[_|-]?(?P<name>[\u4e00-\u9fff]+)-?[\u4e00-\u9fff]*[\uff1a\s_]?[\u4e00-\u9fff\(\)]*-?(?P<date>\d{4}-?\d{2}-?\d{2})?.pdf\Z", flags=re.I)

def rename_inside_folder(folder_path, extension):
    for old_path in glob.glob(os.path.join(folder_path, extension)):
        dirname, old_name = os.path.split(old_path)
        # new_name = sub_name("\\1.SH_\\2-\\4.pdf", old_name)
        match = rename_regex.match(old_name)
        if match is not None:
            new_name = match.group('code') + '-' + match.group('name')
            if match.group('date') is not None:
                new_name += '-' + match.group('date')
            new_name += '.pdf'
            # print(new_name)
            new_path = os.path.join(dirname, new_name)
            try:
                os.rename(old_path, new_path)
            except OSError as exc:
                print(exc)
        else:
            print(f'Unable to match {old_name}')
        # 
work_dir = "./data/shar/" # sys.argv[1]

rename_inside_folder(work_dir, "*.pdf")
rename_inside_folder(work_dir, "*.PDF")