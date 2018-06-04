from googleapiclient import discovery
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from json import loads
import os.path
from sys import argv, modules
import webbrowser
from dateutil.parser import *

import settings

# Optional component for AUTO_COPY.
# It's off by default in settings.py.
if settings.AUTO_COPY:
    try:
        from pyperclip import copy
    except ImportError:
        print("Install pyperclip to use AUTO_COPY")
        pass

# Check for the Client Key
if not os.path.exists(settings.CLIENT_KEY):
    print("Missing Client Key! Check your settings.py file.\nExiting.")
    quit(0)

# Initialize credentials for Google API auth
credentials = service_account.Credentials.from_service_account_file(
    settings.CLIENT_KEY,
    scopes=settings.SCOPES,
    subject=settings.ADMIN_USER)

service = discovery.build('admin', 'directory_v1', credentials=credentials)


# Retrieve ChromeOS Assets by Serial Number.
def get_asset_from_serial(serial_numbers):
    authed_session = AuthorizedSession(credentials)
    mac_address_list = []

    for serial in serial_numbers:

        request_id_url = "https://www.googleapis.com/admin/directory/v1/customer/" \
                         "my_customer/devices/chromeos?projection=full&query=id:" + \
                         serial + "&orderBy=status&sortOrder=ascending&maxResults=" + str(settings.MAX_RESULTS)

        response = authed_session.get(request_id_url)

        if response.status_code == 200:
            response_json = loads(response.content)
            if response_json.get("chromeosdevices"):
                for device in response_json["chromeosdevices"]:
                    try:
                        if not "annotatedAssetId" in device:
                            device["annotatedAssetId"] = "(none)"

                        mac_address_list.append([device["serialNumber"], device["macAddress"], device["lastSync"], device["annotatedAssetId"]])

                    except Exception as error:
                        print("Error: ", error)
                        mac_address_list.append("(none)")
                        pass
            else:
                print("Received no valid Chrome device data from request. Check serial numbers.")
                return
        else:
            print("Bad response, return code:", response.status_code)
            return

    for mac in mac_address_list:
        if mac != "(none)":
            hex_mac = ':'.join(s.encode('hex') for s in mac[1].decode('hex'))

            meraki_link = "https://" + settings.MERAKI_URL \
                          + "/manage/usage/list#q=" \
                          + hex_mac + "&timespan=2592000"

            print("Serial: %s || Asset: %s || Last Sync: %s\n%s\n" % (mac[0],
                                                                      mac[3],
                                                                      parse(mac[2]).strftime('%Y-%m-%d %I:%M %p'),
                                                                      meraki_link))

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


# Retrieve any device in Meraki via its MAC Address
def get_asset_from_mac(mac_addresses):
    for mac in mac_addresses:
        if mac != "none":
            meraki_link = "https://" + settings.MERAKI_URL \
                          + "/manage/usage/list#q=" \
                          + mac + "&timespan=2592000"

            print("%s \t %s" % (mac, meraki_link))

            if meraki_link:
                if settings.AUTO_COPY and "pypercut" in modules:
                    copy(meraki_link)
                if settings.AUTO_OPEN:
                    webbrowser.open(meraki_link)

    result_count = len(mac_addresses)

    if result_count >= settings.MAX_RESULTS and argv[1] == "-mf":
        print("Found %s results." % result_count)
    return


if __name__ == "__main__":

    if len(argv) < 3:
        print('''Usage:
finder.py -s [whole or partial serial]
finder.py -f [list of serials]
finder.py -mf [list of mac addresses]''')
        quit(0)

    if len(argv) > 2 and argv[1] == "-s":
        get_asset_from_serial([argv[2]])

    elif len(argv) > 2 and argv[1] == "-f":
        filename = argv[2]

        serial_list = [line.rstrip('\n') for line in open(filename)]
        serial_list = [x.strip(' ') for x in serial_list]
        get_asset_from_serial(serial_list)

    elif len(argv) > 2 and argv[1] == "-mf":
        filename = argv[2]

        mac_list = [line.rstrip('\n') for line in open(filename)]
        mac_list = [x.strip(' ') for x in mac_list]

        get_asset_from_mac(mac_list)
