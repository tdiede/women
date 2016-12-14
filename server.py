"""Women in tech."""

import os

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import requests
import json
from bs4 import BeautifulSoup
import html5lib

from flask import (Flask, render_template, redirect, jsonify, request, session, flash)
# from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db
from model import (Company)


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "abcdef")


@app.route("/error")
def error():
    raise Exception("Error!")


@app.route('/')
def index():
    """Single page web app."""

    companies = db.session.query(Company).all()

    return render_template("index.html", companies=companies)


@app.route('/data_simple.json')
def data_simple():

    data = {}

    companies = db.session.query(Company).all()

    for company in companies:
        data['team'] = company.team
        data['num_female_eng'] = company.num_female_eng

    return jsonify(data)


@app.route('/data.json')
def data():
    """Returns json of data from database."""

    data = {}

    companies = db.session.query(Company).all()

    for company in companies:
        nested = {}
        data[company.company_id] = nested
        nested['key'] = company.key
        nested['company'] = company.company
        nested['team'] = company.team
        nested['num_female_eng'] = company.num_female_eng
        nested['num_eng'] = company.num_eng
        nested['percent_female_eng'] = company.percent_female_eng
        nested['last_updated'] = company.last_updated

    return jsonify(data)


@app.route('/request_wikipedia.json')
def wikipedia():
    """Make data request to wikipedia."""

    companies = db.session.query(Company).all()
    test_company = companies[10]
    name = test_company.company
    print (name)
    name = 'Pinterest'

    # Response object.
    r = requests.get('https://en.wikipedia.org/wiki/'+name)

    # Content of Response object as string.
    content = r.content

    soup = BeautifulSoup(content, "html5lib")
    soup.prettify()

    table = soup.find_all('table', attrs={"class": "vcard"})

    data = {}
    data['html'] = table[0].encode('utf-8')

    return jsonify(data)


@app.route('/request_linkedin.json')
def linkedin():
    """Make data request to linkedin."""

    companies = db.session.query(Company).all()
    test_company = companies[10]
    name = test_company.company
    print (name)
    name = 'Airbnb'

    # Response object.
    r = requests.get('https://www.linkedin.com/jobs/search?keywords=' + name + ' engineer')

    # Content of Response object as string.
    content = r.content

    soup = BeautifulSoup(content, "html5lib")
    soup.prettify()

    search_results = soup.find_all('code', attrs={"id": "metaTagModule"})
    commented_out = search_results[0].string
    j = json.loads(commented_out)
    header = j['resultHeader']
    link = j['canonical']
    title = j['title']

    data = {}
    data['header'] = header
    data['link'] = link
    data['title'] = title

    return jsonify(data)


################################################################################

if __name__ == "__main__":

    connect_to_db(app, os.environ.get("DATABASE_URL"))

    # Create the tables we need from our models (if they don't already exist).
    db.create_all()

    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
