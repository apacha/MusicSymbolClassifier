import traceback
from typing import List

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
MAX_NUMBER_OF_LINES = 400
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Training Reporter'


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


def append_result_to_spreadsheet(dataset_size: int = 15200, image_sizes: str = "192x96px",
                                 stroke_thicknesses: str = "3", staff_lines: str = "60,67,74,81",
                                 model_name: str = "vgg4", data_augmentation="20% zoom, 10° rotation",
                                 optimizer: str = "Adadelta", early_stopping: int = 20, reduction_patience: int = 8,
                                 learning_rate_reduction_factor: float = 0.5, minibatch_size: int = 64,
                                 initialization: str = "glorot_uniform", initial_learning_rate: float = 1.0,
                                 accuracy: float = "0.10", date: str = "24.12.9999", use_fixed_canvas: bool = True,
                                 datasets: str = "homus", execution_time_in_seconds: int = "0",
                                 balancing_method="None"):
    """ Appends the provided results to the Google Spreadsheets document
        https://docs.google.com/spreadsheets/d/1D9kHRhrOBogcrr5ko1DleCnHVKGGNkwbBc6_mnfA6XE/edit#gid=0
    """
    try:
        service, spreadsheet_id = get_service_and_spreadsheet_id()
        first_empty_line = get_first_empty_line_fast(service, spreadsheet_id)
        print("Uploading results to Google Spreadsheet and appending at first empty line {0}".format(first_empty_line))
        data = [dataset_size, image_sizes, stroke_thicknesses, staff_lines, model_name, data_augmentation, optimizer,
                early_stopping, reduction_patience, learning_rate_reduction_factor, minibatch_size, initialization,
                initial_learning_rate, accuracy, date, use_fixed_canvas, datasets, execution_time_in_seconds,
                balancing_method]
        write_into_spreadsheet(service, spreadsheet_id, data, first_empty_line)
    except Exception as exception:
        print("Info: Results could not be uploaded to Google Spreadsheet because it is probably not configured: {0}".format(str(exception)))
        # traceback.print_exc()


def get_service_and_spreadsheet_id():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = ('https://sheets.googleapis.com/$discovery/rest?'
                     'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discovery_url)
    spreadsheet_id = '1D9kHRhrOBogcrr5ko1DleCnHVKGGNkwbBc6_mnfA6XE'
    return service, spreadsheet_id


def write_into_spreadsheet(service, spreadsheet_id, row_data: List[str], line_number):
    value_input_option = "RAW"

    body = {
        'values': [
            row_data,
            # Another row, currently not supported
        ]
    }

    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range="Sheet1!A{0}:Z{0}".format(line_number),
        valueInputOption=value_input_option, body=body).execute()

    return result


def get_first_empty_line_fast(service, spreadsheet_id) -> int:
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range="Sheet1!A1:A{0}".format(MAX_NUMBER_OF_LINES)).execute()
    values = result.get('values', [])
    return len(values) + 1


if __name__ == '__main__':
    append_result_to_spreadsheet()
