import requests
import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

ROOT_UG_LINK = 'http://web.du.ac.in/PreviousQuestionPapers/UNDER%20GRADUATE/'
ROOT_PG_LINK = 'http://web.du.ac.in/PreviousQuestionPapers/POST%20GRADUATE/'
ROOT_DIPLOMA_LINK  = 'http://web.du.ac.in/PreviousQuestionPapers/CERTFICATE-DIPLOMA/'

def extract_tags(url):
    path = PurePosixPath(unquote(urlparse(url).path)).parts
    ls = list(path)
    # Return rest of the path except the BASE_LINK and PDF name
    ls[-1] = ls[-1][0:-4]
    year_sem = ""
    for i in ls[2:-1]:
        if i.startswith(("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "2")):
            year_sem += i + " "
    ls.append(year_sem) 
    return ls[2:]

def extract_pdfs(ROOT_LINK):
    print(f"Extracting PDFs from {ROOT_LINK}")
    data = []
    ls = [ROOT_LINK]
    while len(ls) != 0:
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
                    "graduation": tags[0],
                    "type": tags[1].lower(),
                    "year and semester": tags[-1],
                    "paper": tags[-2].lower(),
                    "link": path,
                })
            else:
                if not sub_link['href'].endswith('db'):
                    ls.append(path)
    return data

def extract_data (links, filenames):
    for i in range(0, len(links)):
        final_data = extract_pdfs(links[i])
        with open(f"final_data_{filenames[i]}.json", "w") as f:
            json.dump(final_data, f)

links = [ROOT_DIPLOMA_LINK, ROOT_PG_LINK, ROOT_UG_LINK]
filenames = ["diploma", "pg", "ug"]
extract_data(links, filenames)

