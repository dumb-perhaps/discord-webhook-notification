import os
import pandas as pd
import typer
import requests
from dotenv import load_dotenv


load_dotenv()
app = typer.Typer()

pd.options.display.max_rows = 9999


@app.command()
def archive_logs(fle:str):
    try:
        with open(fle, 'r') as f:
            lines = f.readlines()
        df = pd.DataFrame({'logs':lines})
        apps_df = df[df['logs'].str.contains('Application')]
        apps_df['logs'] = apps_df['logs'].str.strip()
        split_df = apps_df['logs'].str.split(" - ", expand=True)
        split_df.columns = ["Date", "Time", "Action"]
        split_df.to_csv('system_audit.csv', index=False)

        webhook_url = os.getenv("webhook_url")
        message = {'content': 'The audit spreadsheet has been successfully generated!'}
        response = requests.post(webhook_url, json=message)
        if response.status_code in [200,204]:
            print('Notified Discord')
        else:
            print("Could not send notification to Discord")

    except FileNotFoundError:
        print("File doesn't exist")

@app.command()
def hello():
    pass


if __name__ == '__main__':
    app()