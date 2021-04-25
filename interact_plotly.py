import sqlite3
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff
import numpy as np
def hist_plot_stars(categories = None):
    query_categories()
    connection = sqlite3.connect("App.db")
    cursor = connection.cursor()
    group_labels = []
    df = []
    if categories is None:
        query = "SELECT stars FROM Apps a join Categories c on a.category_id = c.id where stars <> 0"
        df = [pd.read_sql_query(query, connection)['stars']]
        group_labels = ['all categories']
    else:
        for category in categories:
            query = "SELECT category_name, stars FROM Apps a join Categories c on a.category_id = c.id " \
                    "where stars <> 0 and category_id = " + category
            df.append(pd.read_sql_query(query, connection)['stars'].to_list())
            query = "SELECT category_name FROM Apps a join Categories c on a.category_id = c.id " \
                    "where stars <> 0 group by category_id having category_id = " + category
            group_labels += pd.read_sql_query(query, connection)['category_name'].to_list()
    connection.close()
    try:
        fig = ff.create_distplot(df, group_labels=group_labels, bin_size=0.1, show_curve=False)
        fig.show()
    except:
        print('[Error] Please enter valid category ids in the right form!')


def box_plot_stars():
    query_categories()
    connection = sqlite3.connect("App.db")
    cursor = connection.cursor()
    query = "SELECT category_name, stars FROM Apps a join Categories c on a.category_id = c.id"
    df = pd.read_sql_query(query, connection)
    connection.close()
    fig = px.box(df, x="category_name", y="stars")
    fig.show()

def bar_plot_num_apps():
    query_categories()
    connection = sqlite3.connect("App.db")
    cursor = connection.cursor()
    query = "SELECT category_name, count(1) as num_apps FROM Apps a join Categories c on a.category_id = c.id group by category_name"
    df = pd.read_sql_query(query, connection)
    connection.close()
    fig = px.bar(df, x='category_name', y='num_apps')
    fig.show()

def query_categories():
    '''
    Constructs and executes SQL query to retrieve
    all fields from the Categories table

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''

    connection = sqlite3.connect("App.db")
    cursor = connection.cursor()
    query = "SELECT * FROM Categories"
    result = cursor.execute(query).fetchall()
    connection.close()
    return result

def query_app(category_id):
    ''' Provided for example only.
    Constructs and executes SQL query to retrieve
    all fields from the App table filtered by category_id

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''

    connection = sqlite3.connect("App.db")
    cursor = connection.cursor()
    query = "SELECT * FROM Apps where category_id = " + str(category_id)
    result = cursor.execute(query).fetchall()
    connection.close()
    return result

if __name__ == "__main__":
    IsFirstStep = 1
    Isgraph = 0
    result_list, categories, apps  = [], [], []
    query_results = query_categories()
    print('-' * 34)
    print('List of categories')
    print('-' * 34)
    category_id = None
    for num, item in enumerate(query_results):
        categories.append(item[1])
        print('['+str(num+1)+']', item[1])
    while True:
        if IsFirstStep == 1:
            if Isgraph == 0:
                category_id = input('Enter a category id (e.g. 1) or "exit" or "show graphs": ').lower()
                if category_id == 'exit':
                    break
                if category_id == 'show graphs':
                    Isgraph = 1
            elif Isgraph == 1:
                print('-' * 34)
                print('List of graph types')
                print('-' * 34)
                print('[1] Box plot of stars of each category')
                print('[2] Bar plot of num of apps in each category')
                print('[3] Histogram of stars')
                isshow = input('Enter the graph id you want to show (e.g. 1) or "back": ').lower()
                if isshow == 'back':
                    Isgraph = 0
                if isshow.isdigit():
                    if int(isshow) == 1:
                        print('Show the box plot...')
                        box_plot_stars()
                    elif int(isshow) == 2:
                        print('Show the bar plot...')
                        bar_plot_num_apps()
                    elif int(isshow) == 3:
                        isall = input('Do you want to show overall distribution of stars? (e.g. yes/no): ').lower()
                        if isall == 'yes':
                            print('Show the overall histogram...')
                            hist_plot_stars()
                        elif isall == 'no' :
                            pre_categories = input('Which categories do you want to compare? (e.g. 2 3): ')
                            print('Show the compared histogram...')
                            result = pre_categories.split()
                            new_result = []
                            for i in result:
                                if i.isdigit():
                                    new_result.append(str(int(i) - 1))
                                else:
                                    break
                            hist_plot_stars(new_result)
                        else:
                            print('[Error] Enter yes or no')
                            continue
                    else:
                        print('[Error] Enter proper graph id')
                        continue
                else:
                    print('[Error] Enter proper graph id')
                    continue
            if category_id.isdigit():
                if 1 <= int(category_id) <= len(categories):
                    IsFirstStep = 0
                    app_list = query_app(int(category_id)-1)
                    print('-' * 34)
                    print('List of apps in category ' + categories[int(category_id)-1])
                    print('-' * 34)
                    apps = []
                    for num, result in enumerate(app_list):
                        apps.append((result[1], result[4]))
                        info = result[1] + ' (' + result[2] + '): ' + str(result[3])
                        print('[' + str(num + 1) + '] ' + info)
                else:
                    print('[Error] Enter proper category id')
                    continue
            else:
                if category_id is None:
                    print('[Error] Enter proper category id')
                continue
        else:
            app_id = input('Choose the number for detail search or "exit" or "back": ').lower()
            if app_id == 'exit':
                break
            elif app_id == 'back':
                IsFirstStep = 1
            else:
                result_dict = {}
                if app_id.isdigit():
                    if 1 <= int(app_id) <= len(apps):
                        print('The url of app ' + apps[int(app_id)-1][0] + ' is: ' + apps[int(app_id)-1][1])
                    else:
                        print('[Error] Invalid input')
                        continue
                else:
                    print('[Error] Invalid input')
                    continue