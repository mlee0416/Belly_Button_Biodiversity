from .app import db

class Otu(db.Model):
    __tablename__ = "otu"
    otu_id = db.Column(db.Integer, primary_key = True)
    lowest_taxonomic_unit_found = db.Column(db.Text)

    def __repr__(self):
        return "<Otu %r>" % (self.lowest_taxonomic_unit_found)

class Metadata(db.Model):
    __tablename__ = "samples_meta"
    sampleid = db.Column(db.Integer, primary_key = True)
    event = db.Column(db.Text)
    ethnicity = db.Column(db.Text)
    gender = db.Column(db.Text)
    age = db.Column(db.Integer)
    wfreq = db.Column(db.Integer)
    bbtype = db.Column(db.Text)
    location = db.Column(db.Text)
    country012 = db.Column(db.Text)
    zip012 = db.Column(db.Integer)
    country1319 = db.Column(db.Text)
    zip1319 = db.Column(db.Integer)
    dog = db.Column(db.Text)
    cat = db.Column(db.Text)
    impsurface013 = db.Column(db.Integer)
    npp013 = db.Column(db.Float)
    mmaxtemp013 = db.Column(db.Float)
    pfc013 = db.Column(db.Float)
    impsurface1319 = db.Column(db.Integer)
    npp1319 = db.Column(db.Float)
    mmaxtemp1319 = db.Column(db.Float)
    pfc1319 = db.Column(db.Float)

    def __repr__(self):
        return "<Metadata %r>" % (self.sampleid)