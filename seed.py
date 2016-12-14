"""Utility file to seed database."""

from model import db, connect_to_db
from model import (Company)

from server import app

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import os

# Whenever seeding,
# drop existing database and create a new database.
# os.system("dropdb companies")
# print "dropdb companies"
# os.system("createdb companies")
# print "createdb companies"


def load_companies():
    """Load companies from data_spreadsheet.csv into database."""

    print "companies"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicates.
    Company.query.delete()

    # Read data file and insert data.
    for row in open("data/data_spreadsheet.csv"):
        row = row.rstrip()
        key, company, team, num_female_eng, num_eng, percent_female_eng, last_updated, submit, site = row.split(",")

        print "*"*80

        key = key.strip('"')
        company = company.strip('"')
        team = team.strip('"')
        num_female_eng = num_female_eng.strip('"')
        num_eng = num_eng.strip('"')
        percent_female_eng = percent_female_eng.strip('"')
        last_updated = last_updated.strip('"')

        if key != 'key':
            print row
            company = Company(key=key,
                              company=company,
                              team=team,
                              num_female_eng=int(num_female_eng),
                              num_eng=int(num_eng),
                              percent_female_eng=float(percent_female_eng),
                              last_updated=last_updated)

            print company

            # We need to add to the session or it won't ever be stored.
            db.session.add(company)

    # Once we're done, we should commit our work.
    db.session.commit()


################################################################################

if __name__ == "__main__":

    connect_to_db(app, os.environ.get("DATABASE_URL"))

    # In case tables haven't been created, create them.
    # db.drop_all()
    db.create_all()

    # Import different types of data
    load_companies()
