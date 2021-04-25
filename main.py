from bs4 import BeautifulSoup
import requests
import json
import secrets # file that contains your API key
import time
CACHE_FILE_NAME = 'cacheSite_Scrape.json'
import pandas as pd
import numpy as np

import csv, sqlite3



def load_cache():
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def save_cache(cache):
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()

def make_url_request_using_cache(url, cache, params=None, type='text'):
    if (url in cache.keys()):  # the url is our unique key
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(url)
        if type == 'json':
            cache[url] = response.json()
        else:
            cache[url] = response.text
        save_cache(cache)
        return cache[url]

CACHE_DICT = load_cache()


class Apps:
    '''an app site

    Instance Attributes
    -------------------
    category: string
        the category of an app (e.g. 'Games', '')

    name: string
        the name of an app (e.g. 'Zoom Cloud Meetings')

    developer: string
        the developer of an app (e.g. 'MobiSystems')

    stars: float
        the rated stars of an app (e.g. 4.9)

    url: string
        the download address of an app (e.g. '/store/apps/details?id=com.microsoft.teams')
    '''

    def __init__(self, category=None, name=None, developer=None, stars=None, url=None):
        self.category = category
        self.name = name
        self.developer = developer
        self.stars = stars
        self.url = url

    def info(self):
        return self.name + ' (' + str(self.category) + ' ' + str(self.developer) + '): ' + \
               str(self.stars) + ' ' + str(self.url)


def build_cate_url_dict():
    ''' Make a dictionary that maps category name to the category page url from "https://play.google.com"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is the category name and value is the category page url
        e.g. {'Microsoft Teams':'https://play.google.com/store/apps/details?id=com.microsoft.teams', ...}
    '''
    url = 'https://play.google.com/store/apps/'
    page = make_url_request_using_cache(url, CACHE_DICT)
    soup = BeautifulSoup(page, 'html.parser')
    dropdown_menu = soup.find_all('ul', class_="TEOqAc")
    hyperlinks = dropdown_menu[0].find_all('a')
    result_dict = {}
    for i in hyperlinks:
        result_dict[i.text.lower()] = 'https://play.google.com' + i.get('href')
    return result_dict



def build_app_dict(categories_dict):
    ''' Make a dictionary that contains fields of an app

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is the field name and value is the crawled result from each app
    '''

    web = 'https://play.google.com'
    cate_id = 0
    name, developer, stars, url, category_id = [],[],[],[],[]

    for cate_name, cate_url in categories_dict.items():
        cate_page = make_url_request_using_cache(cate_url, CACHE_DICT)
        soup_temp = BeautifulSoup(cate_page, 'html.parser')
        print(cate_name)

        app_list = soup_temp.find_all('div', class_='k6AFYd')
        for app in app_list:
            app_div = app.find_all('div', class_='WsMG1c nnK0zc')
            app_dev = app.find_all('div', class_='KoLSrc')
            app_a = app.find_all('a')
            app_star = app.find_all('div', class_='pf5lIe')
            name.append(app_div[0].text)
            developer.append(app_dev[0].text)
            url.append(web + app_a[0].get('href'))
            category_id.append(cate_id)
            if app_star != []:
                stars.append(str(app_star[0].find_all('div')[0])[23:26])
            else:
                stars.append(0.0)

        cate_id += 1
        # print(len(name), len(developer), len(url), len(stars), len(category_id))

    app_dict = {'id': np.arange(len(name)),
                'app_name': name,
                'developer':developer,
                'stars':stars,
                'url':url,
                'category_id':category_id}

    return app_dict





if __name__ == '__main__':
    categories_dict = build_cate_url_dict()
    categories_data = {'id':np.arange(len(categories_dict)),
                     'category_name': list(categories_dict.keys()),
                     'category_url': list(categories_dict.values())}

    pd_categories = pd.DataFrame(categories_data)
    pd_categories.to_csv('Categories.csv',index=False)

    # conn = sqlite3.connect("App.db")
    # df = pd.read_csv('Categories.csv')
    # df.to_sql('Categories', conn, if_exists='append', index=False)
    # print('ok')

    apps_dict = build_app_dict(categories_dict)
    pd_apps = pd.DataFrame(apps_dict)
    pd_apps.to_csv('Apps.csv', index=False)

    # conn = sqlite3.connect("App.db")
    # df = pd.read_csv('Apps.csv')
    # df.to_sql('Apps', conn, if_exists='append', index=False)
    # print('ok')

