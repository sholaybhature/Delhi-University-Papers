import requests
import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

def extract_tags(url):
    path = PurePosixPath(unquote(urlparse(url).path)).parts
    ls = list(path)
    # Return rest of the path except the BASE_LINK and PDF name
    pdf = ls.pop()
    #  if len(ls) == 
    
    ls.append(pdf[0:-4])

    return ls[2:]

ROOT_UG_LINK = 'http://web.du.ac.in/PreviousQuestionPapers/UNDER%20GRADUATE/'
ROOT_PG_LINK = 'http://web.du.ac.in/PreviousQuestionPapers/POST%20GRADUATE/'
ROOT_DIPLOMA_LINK  = 'http://web.du.ac.in/PreviousQuestionPapers/CERTFICATE-DIPLOMA/'
def extract_graduation(root_link):
    r = requests.get(root_link)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table')
    # Ignore the table headers, and other links
    links = table.findAll('a')[5:]
    return links

def extract_pdfs(ROOT_LINK):
    #  r = requests.get(ROOT_LINK)
    #  soup = BeautifulSoup(r.text, 'lxml')
    #  table = soup.find('table')
    #  links = table.findAll('a')[5:]
    #  print(links)
    data = []
    ls = [ROOT_LINK]
    count = 0
    while len(ls) != 0:
        count += 1
        l = ls.pop()
        print(f"Current link: {l}")
        r = requests.get(l)
        soup = BeautifulSoup(r.text, 'lxml')
        table = soup.find('table')
        if table is None:
            continue
        links = table.findAll('a')
        for sub_link in links[5:]:
            path = urljoin(l, sub_link['href'])
            if sub_link['href'].endswith('pdf') or sub_link['href'].endswith('PDF'):
                tags = extract_tags(path)
                data.append({
                    "Graduation": tags[0],
                    "Type": tags[1],
                    "Year and Semester": tags[2:-1],
                    "Paper": tags[-1],
                    "Link": path,
                })
                print(f"Found a PDF: {tags[-1]}")
            else:
                if not sub_link['href'].endswith('db'):
                    ls.append(path)
    print(count)
    return data
final_data = extract_pdfs(ROOT_DIPLOMA_LINK)
with open("data_diploma.json", "w") as f:
    json.dump(final_data, f)

