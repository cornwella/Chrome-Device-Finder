## Chrome Device Finder ##

A quick script to locate ChromeOS devices based on serial numbers.

It pulls the device MAC from Google Admin, then opens a Meraki Dashboard device search URL (or copies it to the clipboard), which indicates the AP it last connected to (along with the time and date).  

It could be used with a sample group of serials to approximate a cart's location too.

#### Requirements ####

`pip install google-api-python-client google-auth google-auth-httplib2 requests`

If you want to use AUTO_COPY, you'll need pyperclip too:  
`pip install pyperclip`

#### Setup ####

1. Create a Google Directory Service Account with "View" scope access.
2. Delegate it API access in the Admin console (Security -> Advanced Settings)
3. Copy the `client_secret.json` into the project directory
4. Adjust your preferences in `settings.py`

#### Usage ####

`finder.py -s [serial]`

Use `AUTO_COPY` to copy the Meraki URL to the clipboard,  
and `AUTO_OPEN` to open it in the system default web browser.  
Partial serials return all valid matches.  

*or*

`finder.py -f [file.csv]`

The `csv` is one line of comma-separated serial numbers.  


#### To-do ####

* Rewrite output to make it less ugly
