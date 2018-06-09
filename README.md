## Chrome Device Finder ##

A quick script to locate ChromeOS devices based on serial numbers.

It pulls the device MAC from Google Admin, then opens a Meraki Dashboard device search URL (or copies it to the clipboard), which indicates the AP it last connected to (along with the time and date).  

It can be used with a sample group of serials to approximate a cart's location too.

Here's a screenshot of it in action:

![screenshot](https://i.imgur.com/NIJb3an.pngg)

#### Requirements ####

`pip install python-dateutil google-api-python-client google-auth google-auth-httplib2 requests`

If you want to use AUTO_COPY for clipboard pasting, you'll need pyperclip too:
`pip install pyperclip`

#### Setup ####

1. Create a Google Directory Service Account with "View" scope access.
2. Delegate it API access in the Admin console (Security -> Advanced Settings)
3. Copy the `client_secret.json` into the project directory
4. Adjust your preferences in `settings.py`

#### Usage ####

`finder.py -s [serial]`

Enable `AUTO_COPY` to copy the Meraki URL to the clipboard,
and `AUTO_OPEN` to open it in the system default web browser (probably more useful).
Partial serials return all valid matches (given the limit in `settings.py`).  

*or*

`finder.py -f [file.csv]`

The `csv` is a list of serial numbers (one per line).  
`testing_serials.csv` is included as example.

There's also the option to use `finder.py -mf [mac_file.csv]`, which will simply generate and open 
Meraki URLs from a list of MAC addresses.
