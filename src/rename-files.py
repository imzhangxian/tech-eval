# coding: utf-8
import glob
import os
import re
# import sys

# sub_name = re.compile(r"(\d{6}).SH_([\u4e00-\u9fff]+)：([\u4e00-\u9fff]+)-(\d{8}).pdf\Z", flags=re.I).sub
sub_name = re.compile(r"(\d{6})_([\u4e00-\u9fff]+)[\uff1a]([\u4e00-\u9fff]+).PDF\Z", flags=re.I).sub

work_dir = "./data/shar/" # sys.argv[1]

for old_path in glob.glob(os.path.join(work_dir, "*.pdf")):
    dirname, old_name = os.path.split(old_path)
    # new_name = sub_name("\\1.SH_\\2-\\4.pdf", old_name)
    new_name = sub_name("\\1.SH_\\2.pdf", old_name)
    new_path = os.path.join(dirname, new_name)
    try:
        os.rename(old_path, new_path)
    except OSError as exc:
        print(exc)
