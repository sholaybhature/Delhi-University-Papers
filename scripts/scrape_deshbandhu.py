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
    ls[-1] = ls[-1][0:-4]
    # Add year
    ls.append(ls[-1][-4:])
    ls[-2] = ls[-2] + " (all subject papers)"
    return ls[2:]

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
                tags = extract_tags(path)
                data.append({
                    "graduation": "UNDERGRADUATE",
                    "type": tags[-3].lower(),
                    "year and semester": tags[-1],
                    "paper": tags[-2].lower(),
                    "link": path,
                })
            else:
                ls.append(path)
    return data 
final_data = extract_pdfs(ROOT_URL)
with open("final_data_desh.json", "w") as f:
    json.dump(final_data, f)
