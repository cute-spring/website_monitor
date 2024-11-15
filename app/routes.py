from flask import render_template, request, redirect, url_for, send_file
from . import db
from .models import Website, MonitoringRecord
from .export import export_to_excel
from io import BytesIO

def add_routes(app):
    @app.route('/')
    def index():
        websites = Website.query.all()
        return render_template('index.html', websites=websites)

    @app.route('/manage', methods=['GET', 'POST'])
    def manage():
        if request.method == 'POST':
            url = request.form['url']
            name = request.form['name']
            new_website = Website(url=url, name=name)
            db.session.add(new_website)
            db.session.commit()
            return redirect(url_for('manage'))
        websites = Website.query.all()
        return render_template('manage.html', websites=websites)

    @app.route('/delete/<int:id>')
    def delete(id):
        website = Website.query.get_or_404(id)
        db.session.delete(website)
        db.session.commit()
        return redirect(url_for('manage'))

    @app.route('/export')
    def export():
        output = export_to_excel()
        return send_file(output, as_attachment=True, download_name="detection_results.xlsx")

    @app.route('/history/<int:website_id>')
    def history(website_id):
        website = Website.query.get_or_404(website_id)
        records = MonitoringRecord.query.filter_by(website_id=website.id).order_by(MonitoringRecord.check_time.asc()).all()

        # Prepare data for the chart
        chart_data = {
            "labels": [record.check_time.strftime('%Y-%m-%d %H:%M:%S') for record in records],
            "data": [record.response_time for record in records]
        }

        return render_template('history.html', website=website, records=records, chart_data=chart_data)