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
        return '{} -- {} -- {}'.format(self.title, price_str, self.link)

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

    search_queries = ['fujinon', 'xf 5', 'xf 1', 'xf 6', 'xf 9']

    for qry in search_queries:
        result = requests.get('http://www.afrangdigital.com/AjaxSearchUsed.aspx?Query={}'.format(qry))
        soup = bs4.BeautifulSoup(result.content, 'html.parser')
        all_divs = soup.find_all('div')
        for div in all_divs:
            g = Gear.gear_with_div(div)
            if g and g.link not in results:
                results[g.link] = g

    for i, res in enumerate(results.values()):
        print('{}. {}'.format(i+1, res))

    compare_to_last_search(results)
    save_as_last_search(results)


def compare_to_last_search(results):
    f = open('last_search.json')
    old_results = json.load(f)

    new_ones = []
    for res in results.keys():
        try:
            res = unicode(res)
            if res not in old_results.keys():
                new_ones.append(res)
        except:
            pass

    if len(new_ones) > 0:
        print('\n\n\n')
        for new in new_ones:
            print(new)


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
