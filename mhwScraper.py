#! python3
# mhwScraper.py - Downloads large monster information for Monster Hunter World.

import requests, bs4


def check_attr(attr_name, attr_source):
    for item in attr_source:
        attr_found = ""  # attribute not found yet
        if item.get_text() == attr_name:  # search for attribute
            next_index = attr_source.index(item) + 1
            attr_found = attr_source[next_index].get_text()
            print(f"{attr_name:15}: {attr_found.strip():}")
            break
    if not attr_found:
        print(f"{attr_name} not found")


url = "https://monsterhunterworld.wiki.fextralife.com/Large+Monsters"  # starting url

print(f"Downloading page {url}...")
res = requests.get(url)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "lxml")

monsterElem = soup.select(
    "div #tagged-pages-container a"
)  # Select all links that lead to monster information
for monster_link in monsterElem:
    # print(f"Getting info from {monster_link}")
    # go to each monster page one at a time
    monsterUrl = "https:" + monster_link.get("href")
    res = requests.get(monsterUrl)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "lxml")

    # select the table containing the monster data from the page
    monster_table = soup.select("div.infobox > div > table > tbody > tr > td")

    try:
        monsterName = soup.select(
            "div.infobox > div > table > tbody > tr:nth-child(1) > th > h2"
        )
        print(monsterName[0].get_text())
    except:
        monsterName = soup.select(
            # one monster page name is wrapped in a p instead of a h2 element
            "div.infobox > div > table > tbody > tr:nth-child(1) > th > p"
        )
        print(monsterName[0].get_text())

    # list of elements to match from the table
    attr_list = [
        "Species",
        "Elements",
        "Ailments",
        "Weakness",
        "Resistances",
        "Locations",
    ]
    for attr in attr_list:
        check_attr(attr, monster_table)
    print()
