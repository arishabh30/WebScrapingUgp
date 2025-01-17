#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request
from source import *
import csv
import numpy as np
import pandas as pd
app = Flask(__name__)


# DOIList_main =[]

@app.route('/<string:doi_link>', methods=['GET', 'POST'])
def home(doi_link):

    # print(int(doi_link))

    # print(index.DOIList_main)
    q =request.args.get("q")
    print(q)

    url = q
    link = doi_link
    seperate1 = link.split('https:$$doi.org$')
    print(seperate1)
    print(url)

    # print(html)

    # if "doi.org" in str(url):
    url_new = convert_to_actual_url(str(url))
    # else:
    #     url_new = url
    html = gettingUrl(url_new)
    string = url_new.split('.')
    if 'springer' in string:
        (
            auth,
            titles,
            journalList,
            yearlist,
            DOIs,
            scholarLinks,
            # Data
            ) = Springer(html)
    elif 'nature' in string:

        (
            auth,
            titles,
            journalList,
            yearlist,
            DOIs,
            scholarLinks,
            ) = Nature(html)
    elif 'science' in string and 'sciencedirect' not in string:

        (
            auth,
            titles,
            journalList,
            yearlist,
            DOIs,
            scholarLinks,
            ) = Science(html)
    elif 'mdpi' in string:

        (
            auth,
            titles,
            journalList,
            yearlist,
            DOIs,
            scholarLinks,
            ) = MDPI(html)
    elif 'ieee' in string:

        url = url + '/references#references'
        (
            auth,
            titles,
            journalList,
            yearlist,
            DOIs,
            scholarLinks,
            ) = IEEE(html)
    elif 'cambridge' in string:

        (
            auth,
            titles,
            journalList,
            yearlist,
            DOIs,
            scholarLinks,
            ) = Cambridge(html)
    elif 'sciencedirect' in string:

        (
            auth,
            titles,
            journalList,
            yearlist,
            DOIs,
            scholarLinks,
            ) = ScienceDirect(html)
    elif 'acs' in string:
        (
            auth,
            titles,
            journalList,
            yearlist,
            DOIs,
            scholarLinks,
            ) = ACS(html)

        # dict = {'Author':auth,'Title':titles,'Journal':journalList,'Year of publication':yearlist,'DOI number':DOIs,'Scholar Links':scholarLinks}
        # df = pd.DataFrame(dict)
        # # saving the dataframe
        # df.to_csv('content.csv')

    return render_template(
        'link.html',
        name=url,
        author=auth,
        titleAll=titles,
        DOIList=DOIs,
        YearList=yearlist,
        journals=journalList,
        array=scholarLinks,
        # DOICited=Data
        )


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('enteredurl')
        print(url)
        html = gettingUrl(url)

        # print(html)

        string = url.split('.')

        if 'springer' in string:
            (
                auth,
                titles,
                journalList,
                yearlist,
                index.DOIList_main,
                scholarLinks,
                # Data
                ) = Springer(html)
        elif 'nature' in string:

            (
                auth,
                titles,
                journalList,
                yearlist,
                index.DOIList_main,
                scholarLinks,
                ) = Nature(html)
        elif 'science' in string and 'sciencedirect' not in string:

            (
                auth,
                titles,
                journalList,
                yearlist,
                index.DOIList_main,
                scholarLinks,
                ) = Science(html)
        elif 'mdpi' in string:

            (
                auth,
                titles,
                journalList,
                yearlist,
                index.DOIList_main,
                scholarLinks,
                ) = MDPI(html)
        elif 'ieee' in string:

            url = url + '/references#references'
            (
                auth,
                titles,
                journalList,
                yearlist,
                index.DOIList_main,
                scholarLinks,
                ) = IEEE(html)
        elif 'cambridge' in string:

            (
                auth,
                titles,
                journalList,
                yearlist,
                index.DOIList_main,
                scholarLinks,
                ) = Cambridge(html)
        elif 'sciencedirect' in string:

            (
                auth,
                titles,
                journalList,
                yearlist,
                index.DOIList_main,
                scholarLinks,
                ) = ScienceDirect(html)
        elif 'acs' in string:
            (
                auth,
                titles,
                journalList,
                yearlist,
                index.DOIList_main,
                scholarLinks,
                ) = ACS(html)

        # dict = {'Author':auth,'Title':titles,'Journal':journalList,'Year of publication':yearlist,'DOI number':DOIs,'Scholar Links':scholarLinks}
        # df = pd.DataFrame(dict)
        # # saving the dataframe
        # df.to_csv('content.csv')

        return render_template(
            'index.html',
            name=url,
            author=auth,
            titleAll=titles,
            DOIList=index.DOIList_main,
            YearList=yearlist,
            journals=journalList,
            array=scholarLinks,
            # DOICited=Data
            )
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
