import re
import csv

# url as https://static.sse.com.cn/disclosure/listedinfo/announcement/c/new/2024-07-26/603391_20240726_EZF5.pdf
list_re = re.compile(r"(?P<code>\d{6})[_|-](?P<date>\d{8})[_|-]([0-9][-|_])?[a-zA-Z0-9]*.pdf\Z", flags=re.I)

work_dir = "./data/links" # sys.argv[1]
ashare_links = []
ashare_urls = []
star_links = []
star_urls = []

with open(f'{work_dir}/ipo-docs.csv', newline='') as csvfile:
    fieldnames = ['url', 'name']
    reader = csv.DictReader(csvfile, fieldnames=fieldnames)
    for row in reader:
        url = row['url']
        name  = row['name']
        try:
            filename = url.split('/')[-1]
            match = list_re.match(filename)
            code = match.group('code')
            date = match.group('date')
            link_addr = f'<a href=\'{url}\'>{code}-{name}, {date}</a>'
            if code.startswith('60'):
                ashare_links.append(link_addr)
                ashare_urls.append(url)
            elif code.startswith('68'):
                star_links.append(link_addr)
                star_urls.append(url)
        except Exception:
            print(f'error processing url : {url}')
            pass

with open(f'{work_dir}/ipo-docs-ashare.html', 'w') as html_file:
    html_file.write('<html><body><ol>\n')
    for link_addr in ashare_links:
        html_file.write(f'<li>{link_addr}</li>\n')
    html_file.write('</ol></body></html>')

with open(f'{work_dir}/ipo-docs-ashare-urls.txt', 'w') as txt_file:
    for url in ashare_urls:
        txt_file.write(f'{url}\n')

with open(f'{work_dir}/ipo-docs-star.html', 'w') as html_file:
    html_file.write('<html><body><ol>\n')
    for link_addr in star_links:
        html_file.write(f'<li>{link_addr}</li>\n')
    html_file.write('</ol></body></html>')

with open(f'{work_dir}/ipo-docs-star-urls.txt', 'w') as txt_file:
    for url in star_urls:
        txt_file.write(f'{url}\n')
