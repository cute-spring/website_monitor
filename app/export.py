import pandas as pd
from .models import Website, MonitoringRecord
from io import BytesIO

def export_to_excel():
    # Fetch current status data from Website table
    websites = Website.query.all()
    current_data = [
        {
            'URL': site.url,
            'Name': site.name,
            'Status': site.status,
            'Response Time (ms)': site.response_time,
            'Last Checked': site.last_checked.strftime('%Y-%m-%d %H:%M:%S') if site.last_checked else 'N/A'
        }
        for site in websites
    ]

    # Fetch historical data from MonitoringRecord table
    history_data = [
        {
            'Website Name': record.website.name,
            'URL': record.website.url,
            'Status': record.status,
            'Response Time (ms)': record.response_time,
            'Check Time': record.check_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        for record in MonitoringRecord.query.all()
    ]

    # Create a BytesIO stream to store the Excel file
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Write current data to the first sheet
        current_df = pd.DataFrame(current_data)
        current_df.to_excel(writer, index=False, sheet_name='Current Status')

        # Write historical data to the second sheet
        history_df = pd.DataFrame(history_data)
        history_df.to_excel(writer, index=False, sheet_name='Monitoring History')
    
    # Move to the beginning of the stream
    output.seek(0)
    return output