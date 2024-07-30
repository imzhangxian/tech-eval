import urllib3 as ul

url = "https://rail.eecs.berkeley.edu/deeprlcourse/deeprlcourse/static/slides/lec-1.pdf"

resp = ul.request('GET', url, preload_content=False, headers={'User-Agent': 'Customer User Agent If Needed'})

with open('lec-1.pdf', 'wb') as f:
    for chunk in resp.stream(65536):
        f.write(chunk)

resp.release_conn()