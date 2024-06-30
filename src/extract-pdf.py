from pypdf import PdfReader

reader = PdfReader("./data/shar/688720_20231117_BLL3.pdf")
number_of_pages = len(reader.pages)
text = ""
for p in range(20):
    page = reader.pages[p]
    text += page.extract_text()

with open("extracted.txt", "w") as f:
    f.write(text)
