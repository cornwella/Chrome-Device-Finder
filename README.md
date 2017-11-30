## Chrome Device Finder ##

A quick script to locate ChromeOS devices based on serial numbers in a Meraki network.

It pulls the device MAC from Google Admin, then copies a Meraki device search URL to the clipboard, 
which indicates the AP it last connected to (along with the time and date). It can be used with a sample group of serials
to approximate a cart's location too.

#### Requirements ####

`pip install google-api-python-client google-auth`

#### Setup ####

1. Create a Google Directory Service Account with "View" scope access.
2. Delegate it API access in the Admin console (Security -> Advanced Settings)
3. Copy the `client_secret.json` into the project directory
4. Adjust `settings.py` to match your infrastructure

#### Usage ####

`finder.py -s [serial]`

Use `AUTO_COPY` to copy the Meraki URL to the clipboard,  
and `AUTO_OPEN` to open it in the system default web browser.  
Using partial serials returns all matches.  

*or*

`finder.py -f [file.csv]`

The `csv` is one line of comma-separated serial numbers.  
`testing_serials.csv` is included as example.


#### To-do ####

* Rewrite output to make it less ugly
