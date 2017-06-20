from __future__ import print_function

from typing import List

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BbrHOoKTIhldz4Eh3tMEM7ne6rUujojyjs00ikO311A/edit#gid=0
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheet_id = '1BbrHOoKTIhldz4Eh3tMEM7ne6rUujojyjs00ikO311A'

    first_empty_line = get_first_empty_line(service, spreadsheet_id)
    print("Inserting at first empty line {0}".format(first_empty_line))

    write_into_spreadsheet(service, spreadsheet_id, ["test", "test2", "05.02.1072"], first_empty_line)


def write_into_spreadsheet(service, spreadsheet_id, row_data: List[str], line_number):
    valueInputOption = "RAW"

    body = {
        'values': [
            row_data,
            # Another row, currently not supported
        ]
    }

    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range="Sheet1!A{0}:Z{0}".format(line_number),
        valueInputOption=valueInputOption, body=body).execute()

    return result


def get_first_empty_line(service, spreadsheet_id) -> int:
    for line_number in range(1, 1000):
        result = get_line_data(service, spreadsheet_id, line_number)
        if result_contains_data(result):
            continue
        return line_number


def get_line_data(service, spreadsheet_id, line_number) -> dict:
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range="Sheet1!A{0}:Z{0}".format(line_number)).execute()
    return result


def result_contains_data(result) -> bool:
    try:
        values = result.get('values', [])
        if not values or not values[0]:
            return False
        return True
    except:
        return False


if __name__ == '__main__':
    main()
