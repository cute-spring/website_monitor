from datetime import datetime
from . import db

class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=True)
    response_time = db.Column(db.Integer, nullable=True)
    last_checked = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

class MonitoringRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(db.Integer, db.ForeignKey('website.id'), nullable=False)
    status = db.Column(db.String(50), nullable=True)
    response_time = db.Column(db.Integer, nullable=True)
    check_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship back to the Website model
    website = db.relationship('Website', backref=db.backref('monitoring_records', lazy=True))