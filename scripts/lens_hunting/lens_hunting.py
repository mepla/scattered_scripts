import json

__author__ = 'mepla'
import requests
import bs4
from bs4.element import Tag

class Gear(object):
    def __init__(self):
        self.title = None
        self.link = None
        self.owner_email = None
        self.owner_phone = None
        self.owner_name = None
        self.price = None

    def __str__(self):
        price_str = self.price[0:-4]
        return '{} -- {} -- {}'.format(self.title, self.link, price_str)

    def to_json(self):
        return {'title': self.title, 'link': self.link, 'price': self.price}

    @staticmethod
    def gear_with_div(div):
        g = Gear()
        try:
            a_tag = div.find('div', {'class': 'name-pro2'}).h2.a
            assert isinstance(a_tag, Tag)
            tag_str = str(a_tag)
            link = tag_str[tag_str.index('"')+1:tag_str.rindex('"')]
            g.link = 'http://www.afrangdigital.com' + link

            title = tag_str[tag_str.index('">')+2:-4]
            g.title = title

            price_tag = div.find('span', {'class': 'price-pro'}).price
            price_str = str(price_tag)
            price_str = price_str.split(' ')[0].replace('<price>', '').replace(',', '')
            g.price = price_str

            return g
        except:
            # print('Could not parse div: {}\n\n'.format(div))
            pass

def search_afrang():
    results = {}

    fujinon_result = requests.get('http://www.afrangdigital.com/AjaxSearchUsed.aspx?Query=fujinon')
    xf55_200_result = requests.get('http://www.afrangdigital.com/AjaxSearchUsed.aspx?Query=xf55')
    fujinon_soup = bs4.BeautifulSoup(fujinon_result.content, 'html.parser')
    xf55_200_soup = bs4.BeautifulSoup(xf55_200_result.content, 'html.parser')

    fujinon_all_divs = fujinon_soup.find_all('div')
    for div in fujinon_all_divs:
        g = Gear.gear_with_div(div)
        if g and g.link not in results:
            results[g.link] = g

    xf55_200_all_divs = xf55_200_soup.find_all('div')
    for div in xf55_200_all_divs:
        g = Gear.gear_with_div(div)
        if g and g.link not in results:
            results[g.link] = g

    for res in results.values():
        print(res)

    compare_to_last_search(results)
    save_as_last_search(results)

def compare_to_last_search(results):
    f = open('last_search.json')
    old_results = json.load(f)

    for res in results.keys():
        try:
            res = unicode(res)
            if res not in old_results.keys():
                print('\n\n\n\n\n')
                print(res)
        except:
            pass

def save_as_last_search(results):
    assert isinstance(results, dict)
    json_results = {}
    for k, v in results.items():
        json_results[k] = v.to_json()
    f = open('last_search.json', 'w')
    f.write(json.dumps(json_results))
    f.close()

def main():
    search_afrang()

if __name__ == '__main__':
    main()
