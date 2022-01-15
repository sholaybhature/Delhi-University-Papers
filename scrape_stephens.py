import requests
import json
from bs4 import BeautifulSoup

ROOT_LINK_2021 = 'https://www.ststephens.edu/obe-june-2021-question-papers/'
ROOT_LINK_2020 = 'https://www.ststephens.edu/obe-dec2020-question-paper-archive/'

def extract_pdfs(ROOT_LINK, month, year):
    data = []
    r = requests.get(ROOT_LINK)
    soup = BeautifulSoup(r.text, 'lxml')
    rows = soup.select('table > tbody > tr')
    for row in rows[1:]:
        year_sem = year
        cols = row.findAll('td')
        fields = [td.text.strip() for td in cols if month not in td.text.strip()]
        for i in fields:
            if i.startswith(("I", "II", "III", "IV", "V", "VI")):
                year_sem += " " + i + " SEM "
        link = cols[-1].find('a')
        if not link:
            continue
        data.append({
            "graduation": "UNDERGRADUATE",
            "type": fields[0].lower(),
            "year and semester": year_sem,
            "paper": (cols[-2].text.strip() + " (OBE)").lower(),
            "link": link['href'],
            
        })
    return data

def extract_data (links, filenames):
    month = ["June", "December"]
    year = ["2021", "2020"]
    for i in range(0, len(links)):
        final_data = extract_pdfs(links[i], month[i], year[i])
        with open(f"final_data_obe_{filenames[i]}.json", "w") as f:
            json.dump(final_data, f)

links = [ROOT_LINK_2021, ROOT_LINK_2020]
filenames = ["2021", "2020"]
extract_data(links, filenames)
#  final_data = extract_pdfs(ROOT_LINK_2021)
#  with open("data_stephens_2021.json", "w") as f:
    #  json.dump(final_data, f)
