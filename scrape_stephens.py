import requests
import json
from bs4 import BeautifulSoup

ROOT_LINK_2021 = 'https://www.ststephens.edu/obe-june-2021-question-papers/'
ROOT_LINK_2020 = 'https://www.ststephens.edu/obe-dec2020-question-paper-archive/'

def extract_pdfs(ROOT_LINK):
    data = []
    r = requests.get(ROOT_LINK)
    soup = BeautifulSoup(r.text, 'lxml')
    rows = soup.select('table > tbody > tr')
    for row in rows[1:]:
        cols = row.findAll('td')
        fields = [td.text.strip() for td in cols if "June" not in td.text.strip()]
        link = cols[-1].find('a')
        if not link:
            continue
        data.append({
            "Link": link['href'],
            "Paper": cols[-2].text.strip(),
            "Year and Semester": fields[0:-1] + ["(OBE)"],
            
        })
    return data

final_data = extract_pdfs(ROOT_LINK_2021)
with open("data_stephens_2021.json", "w") as f:
    json.dump(final_data, f)
