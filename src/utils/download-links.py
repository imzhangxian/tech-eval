import time, sys
from selenium import webdriver

# url = 'http://www.google.com/' 
# urls = ['https://static.sse.com.cn/disclosure/listedinfo/announcement/c/new/2024-07-26/603391_20240726_EZF5.pdf',
#         'https://static.sse.com.cn/disclosure/listedinfo/announcement/c/new/2024-07-02/603285_20240702_BGFM.pdf',
#         'https://static.sse.com.cn/disclosure/listedinfo/announcement/c/new/2024-06-28/603350_20240628_YQIS.pdf']
url_txt_file = sys.argv[1]
urls = []

with open(f'{url_txt_file}', 'r') as urls_file:
    urls = urls_file.readlines()

options = webdriver.ChromeOptions()
# options.enable_downloads = True
options.add_argument("headless")

driver = webdriver.Chrome(options=options)  # Optional argument, if not specified will search path.
for url in urls:
    driver.get(url)
    time.sleep(2) # Let the user actually see something!

driver.quit()
