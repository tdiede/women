"""Models and database functions for women in tech project."""


from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing).

db = SQLAlchemy()


##############################################################################
# Model definitions

class Company(db.Model):
    """Company contributing data on gender diversity."""

    __tablename__ = "companies"

    company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    key = db.Column(db.String(64), nullable=True, unique=True)
    company = db.Column(db.String(64), nullable=True)
    team = db.Column(db.String(64), nullable=True)
    num_female_eng = db.Column(db.Integer)
    num_eng = db.Column(db.Integer)
    percent_female_eng = db.Column(db.Float)
    last_updated = db.Column(db.DateTime)

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Company num_female_eng=%d num_eng=%d company=%s>" % (self.num_female_eng, self.num_eng, self.company)


##############################################################################
# Helper functions

def connect_to_db(app, db_uri=None):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database.
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgresql:///companies'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print ("Connected to PostgreSQL DB.")
