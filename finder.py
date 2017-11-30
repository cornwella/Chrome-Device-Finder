from apiclient import discovery
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from json import loads
from csv import reader
from sys import argv, modules
import webbrowser

import settings

# Optional component for AUTO_COPY.
# It's off by default in settings.py.
if settings.AUTO_COPY:
    try:
        from pyperclip import copy
    except ImportError:
        print("Install pyperclip to use AUTO_COPY")
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
                         serial + "&orderBy=status&sortOrder=ascending&maxResults=" + str(settings.MAX_RESULTS)

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

            if meraki_link:
                if settings.AUTO_COPY and "pypercut" in modules:
                    copy(meraki_link)
                if settings.AUTO_OPEN:
                    webbrowser.open(meraki_link)

    result_count = len(mac_address_list)

    if result_count >= settings.MAX_RESULTS and argv[1] == "-s":
        print("Found %s results (may be more, reached limit)" % result_count)
    else:
        print("Found %s results." % result_count)
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

        with open(filename, 'rb+') as f:
            reader = reader(f)
            serial_list = list(reader)[0]

        serial_list = [x.strip(' ') for x in serial_list]
        get_asset(serial_list)
