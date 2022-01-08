import requests
import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath


def extract_tags(url):
    path = PurePosixPath(unquote(urlparse(url).path)).parts
    # Bad?
    ls = list(path)
    # Return rest of the path except the BASE_LINK and PDF name
    pdf = ls.pop()
    ls.append(pdf[0:-4])
    return ls[2:]


BASE_LINK = 'http://web.du.ac.in/PreviousQuestionPapers/UNDER%20GRADUATE/'
def extract_graduation(root_link):
    r = requests.get(root_link)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table')
    # Ignore the table headers, and other links
    links = table.findAll('a')[5:]
    return links

def extract_pdfs(traversal_links, base_link):
    data = []
    for i in traversal_links[0:6]:
        ls = [base_link]
        for i in range(0,9):
            l = ls.pop()
            print(f"Current link: {l}")
            # Add error checks
            r = requests.get(l)
            soup = BeautifulSoup(r.text, 'lxml')
            table = soup.find('table')
            links = table.findAll('a')
            for i in links[5:]:
                path = urljoin(l, i['href'])
                if i['href'].endswith('pdf'):
                    tags = extract_tags(path)
                    data.append({
                        "Graduation": tags[0],
                        "Type": tags[1],
                        "Year": tags[2],
                        "Sem": tags[3],
                        "Year": tags[4],
                        "Paper": tags[5],
                        "Link": path,
                    })
                    print(tags[0])

                else:
                    ls.append(path)
    return data
final_data = extract_pdfs(links, BASE_LINK)
j = json.dumps(final_data)
print(j)
