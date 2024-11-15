import requests
from datetime import datetime
from .models import Website, MonitoringRecord
from . import db

def monitor_websites(app):
    with app.app_context():
        websites = Website.query.all()
        for website in websites:
            try:
                response = requests.get(website.url, timeout=5)
                status = 'Success' if response.status_code == 200 else 'Fail'
                response_time = response.elapsed.microseconds // 1000  # in ms
            except requests.RequestException:
                status = 'Fail'
                response_time = None
            
            # Update last_checked in Website model
            website.status = status
            website.response_time = response_time
            website.last_checked = datetime.utcnow()
            
            # Add a new MonitoringRecord for historical data
            record = MonitoringRecord(
                website_id=website.id,
                status=status,
                response_time=response_time,
                check_time=datetime.utcnow()
            )
            db.session.add(record)
            db.session.commit()