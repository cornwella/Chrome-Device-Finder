## Chrome Device Finder ##

A quick script to locate ChromeOS devices based on serial numbers.

It pulls the device MAC from Google Admin, then opens a Meraki Dashboard device search URL (or copies it to the clipboard), which indicates the AP it last connected to (along with the time and date).  

It could be used with a sample group of serials to approximate a cart's location too.

#### Requirements ####

`pip install google-api-python-client google-auth google-auth-httplib2 requests`

If you want to use AUTO_COPY, you'll need pyperclip too:  
`pip install pyperclip`

#### Setup ####

* Create a Google Directory service account with "View" access in the API Dashboard (https://console.cloud.google.com/apis/dashboard)
* Enable the "Admin SDK" API for your service account's project
* Delegate your service account ID API access in the Admin console (Security -> Advanced Settings).  
Give it the Scope `https://www.googleapis.com/auth/admin.directory.device.chromeos.readonly`
* Copy the service account's `client_secret.json` into the project directory
* Adjust your preferences in `settings.py`

#### Usage ####

`finder.py -s [serial]`

In `settings.py`, enable `AUTO_COPY` to copy the Meraki URL to the clipboard,  
or `AUTO_OPEN` to open it in the system default web browser (on by default).
Partial serials return all valid matches.  

*or*

`finder.py -f [file.csv]`

The `csv` is one line of comma-separated serial numbers.  
