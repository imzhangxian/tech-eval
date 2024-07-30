import re
import csv

# url as https://static.sse.com.cn/disclosure/listedinfo/announcement/c/new/2024-07-26/603391_20240726_EZF5.pdf
rename_regex = re.compile(r"(?P<code>\d{6})(.SH)?[_|-]?(?P<name>[\u4e00-\u9fff]+)-?[\u4e00-\u9fff]*[\uff1a\s_]?[\u4e00-\u9fff\(\)]*-?(?P<date>\d{4}-?\d{2}-?\d{2})?.pdf\Z", flags=re.I)

work_dir = "./data/links" # sys.argv[1]
all_links = []

with open(f'{work_dir}/ipo-docs.csv', newline='') as csvfile:
    fieldnames = ['url', 'name']
    reader = csv.DictReader(csvfile, fieldnames=fieldnames)
    for row in reader:
        url = row['url']
        name  = row['name']
        link_addr = f'<a href=\'{url}\'>{name}</a>'
        all_links.append(link_addr)

with open(f'{work_dir}/ipo-docs.html', 'w') as html_file:
    for link_addr in all_links:
        html_file.write(link_addr)
