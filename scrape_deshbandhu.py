import requests
import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Comment
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
ROOT_URL = 'https://www.deshbandhucollege.ac.in/library-old-question-papers.php'

def extract_tags(url):
    path = PurePosixPath(unquote(urlparse(url).path)).parts
    ls = list(path)
    pdf = ls.pop()
    ls.append(pdf[0:-4])
    ls.append("ALL PAPERS")
    return ls[-2:]

def extract_pdfs(ROOT_LINK):
    data = []
    visited = set()
    ls = [ROOT_LINK]
    count = 0
    while len(ls)!= 0:
        count +=1 
        l = ls.pop()
        if l in visited:
            continue
        else:
            visited.add(l)
        print(f"Current link: {l}")
        r = requests.get(l, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        heading = soup.find('div',{'class': 'heading'})
        if heading is None:
            continue
        heading_parent = heading.parent
        # Circular reference?
        links = heading_parent.findAll('a')
        for sub_link in links:
            path = urljoin(l, sub_link['href'])
            if sub_link['href'].endswith('pdf') or sub_link['href'].endswith('PDF'):
                print(f'Found PDF: {path}')
                tags = extract_tags(path)
                data.append({
                    "Paper": tags[-2],
                    "Type": tags[-1],
                    "Link": path,

                })
            else:
                print(path)
                ls.append(path)
    return data 
final_data = extract_pdfs(ROOT_URL)
with open("data_desh.json", "w") as f:
    json.dump(final_data, f)
