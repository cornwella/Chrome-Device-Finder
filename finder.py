from apiclient import discovery
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from json import loads
from csv import reader
from sys import argv

import settings

# These are the optional components for AUT_COPY and AUTO_OPEN.
# They're not strictly required and can be turned off in settings.py.
try:
    from pyperclip import copy
    from webbrowser import open
    extras = True
except ImportError:
    print("Install pyperclip or webbrowser to use AUTO_COPY & AUTO_OPEN")
    extras = False
    pass

# Initialize credentials for Google API auth
credentials = service_account.Credentials.from_service_account_file(
    settings.CLIENT_KEY,
    scopes=settings.SCOPES,
    subject=settings.ADMIN_USER)

service = discovery.build('admin', 'directory_v1', credentials=credentials)


def get_asset(serial_numbers):

    authed_session = AuthorizedSession(credentials)
    mac_address_list = []

    for serial in serial_numbers:

        request_id_url = "https://www.googleapis.com/admin/directory/v1/customer/" \
                         "my_customer/devices/chromeos?projection=full&query=id:" + \
                         serial + "&orderBy=status&sortOrder=ascending&maxResults=10"

        response = authed_session.get(request_id_url)

        if response.status_code == 200:
            response_json = loads(response.content)
            for device in response_json["chromeosdevices"]:
                try:
                    mac_address_list.append([device["serialNumber"], device["macAddress"]])
                except Exception:
                    mac_address_list.append("none")
                    pass
        else:
            print("Something went wrong, return code:", response.status_code)
            pass

    for mac in mac_address_list:
        if mac[1] != "none":
            hex_mac = ':'.join(s.encode('hex') for s in mac[1].decode('hex'))

            meraki_link = "https://" + settings.MERAKI_URL \
                          + "/manage/usage/list#q=" \
                          + hex_mac + "&timespan=2592000"

            print("%s \t %s" % (mac[0], meraki_link))

            if extras:
                if meraki_link:
                    if settings.AUTO_COPY:
                        copy(meraki_link)
                    if settings.AUTO_OPEN:
                        open(meraki_link)

    print("Found %s results." % (len(mac_address_list)))
    return


if __name__ == "__main__":

    if len(argv) < 3:
        print('''Usage:
finder.py -s [whole or partial serial]
finder.py -f [csv of serials]''')
        quit(0)

    if len(argv) > 2 and argv[1] == "-s":
        get_asset([argv[2]])

    elif len(argv) > 2 and argv[1] == "-f":
        filename = argv[2]

        with open(filename, 'rb') as f:
            reader = reader(f)
            serial_list = list(reader)[0]

        serial_list = [x.strip(' ') for x in serial_list]
        get_asset(serial_list)
