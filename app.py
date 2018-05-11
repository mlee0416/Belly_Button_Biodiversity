# Import dependencies
import os
import numpy as np
import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect
)

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

###########################
#######Flask Setup#########
###########################
app = Flask(__name__)

###########################
######Database Setup#######
###########################
from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "") or "sqlite:///datasets/belly_button_biodiversity.sqlite"
db = SQLAlchemy(app)
# Set up engine for reflection
engine = create_engine(os.environ.get("DATABASE_URL", "") or "sqlite:///datasets/belly_button_biodiversity.sqlite")
# Reflect an existing database into a new model
Base = automap_base()
# Reflect tables
Base.prepare(engine, reflect = True)
#Save reference to the samples table
Samples = Base.classes.samples


# Set up table for Otu
class Otu(db.Model):
    __tablename__ = "otu"
    otu_id = db.Column(db.Integer, primary_key=True)
    lowest_taxonomic_unit_found = db.Column(db.Text)

    def __repr__(self):
        return "<Otu %r>" % (self.lowest_taxonomic_unit_found)

# Set up table for Metadata
class Metadata(db.Model):
    __tablename__ = "samples_metadata"
    SAMPLEID = db.Column(db.Integer, primary_key=True)
    EVENT = db.Column(db.Text)
    ETHNICITY = db.Column(db.Text)
    GENDER = db.Column(db.Text)
    AGE = db.Column(db.Integer)
    WFREQ = db.Column(db.Integer)
    BBTYPE = db.Column(db.Text)
    LOCATION = db.Column(db.Text)
    COUNTRY012 = db.Column(db.Text)
    ZIP012 = db.Column(db.Integer)
    COUNTRY1319 = db.Column(db.Text)
    ZIP1319 = db.Column(db.Integer)
    DOG = db.Column(db.Text)
    CAT = db.Column(db.Text)
    IMPSURFACE013 = db.Column(db.Integer)
    NPP013 = db.Column(db.Float)
    MMAXTEMP013 = db.Column(db.Float)
    PFC013 = db.Column(db.Float)
    IMPSURFACE1319 = db.Column(db.Integer)
    NPP1319 = db.Column(db.Float)
    MMAXTEMP1319 = db.Column(db.Float)
    PFC1319 = db.Column(db.Float)

    def __repr__(self):
        return "<Metadata %r>" % (self.sampleid)

# Run database before running other flask routes
@app.before_first_request
def setup():
    db.create_all()

#Flask Routes#
@app.route("/")
def index():
    return render_template("index.html")

# Create route for list of sample names
@app.route("/names")
def names():
    col_names = Samples.__table__.columns.keys()
    col_names.remove("otu_id")
    return jsonify(col_names)

# Create route for list of OTU description
@app.route("/otu")
def otu():
    results = db.session.query(Otu.lowest_taxonomic_unit_found).all()
    otu_list = list(np.ravel(results))
    return jsonify(otu_list)

# Create route for MetaData for a given sample
@app.route("/metadata/<sample>")
def metadata(sample):
    sample = sample.replace("BB_", "") # Strips sample id prefix
    sel_data = [
        Metadata.SAMPLEID,
        Metadata.ETHNICITY,
        Metadata.GENDER,
        Metadata.AGE,
        Metadata.LOCATION,
        Metadata.BBTYPE
    ]
    results = db.session.query(*sel_data).filter(Metadata.SAMPLEID == sample).all()
    sample_metadata_dict = {}
    for result in results:
        sample_metadata_dict["SAMPLEID"] = result[0]
        sample_metadata_dict["ETHNICITY"] = result[1]
        sample_metadata_dict["GENDER"] = result[2]
        sample_metadata_dict["AGE"] = result[3]
        sample_metadata_dict["LOCATION"] = result[4]
        sample_metadata_dict["BBTYPE"] = result[5]
    return jsonify(sample_metadata_dict)


# Create route for weekly washing frequency as a number
@app.route("/wfreq/<sample>")
def wfreq(sample):
    sample = sample.replace("BB_", "") # Strips sample id prefix
    results = db.session.query(Metadata.WFREQ).filter(Metadata.SAMPLEID == sample).all()
    wfreq_sample = list(np.ravel(results))
    print(f"{sample}'s washing frequency is {wfreq_sample[0]}")
    return jsonify(int(wfreq_sample[0]))

@app.route("/samples/<sample>")
def samples(sample):
    otu_df = pd.read_sql("SELECT * FROM Samples", engine)
    otu_df = otu_df.sort_values(by = sample, ascending = False)

    samples_data = [{
        "otu_ids": otu_df[sample].index.values.tolist(),
        "sample_values": otu_df[sample].values.tolist()
    }]
    return jsonify(samples_data)


if __name__ == "__main__":
    app.run(debug = True)
