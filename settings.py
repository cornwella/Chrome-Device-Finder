# --------
# Settings
# --------

# The Google API scope should be the same for all environments
SCOPES = ['https://www.googleapis.com/auth/admin.directory.device.chromeos.readonly']

# Your API client secret key. Don't share this!
CLIENT_KEY = 'client_key.json'

# Your Meraki Dashboard identifier. Log in to the Meraki dashboard see your unique string.
# (the portion after https://[nnnn].meraki.com/)
MERAKI_URL = ''

# The email address of an administrative user in your G Suite environment (ties to your service account)
# ex. "johnsmith@domain.com"
ADMIN_USER = ''

# Maximum results to return from the serial number query.
# Keep in mind if you use AUTO_OPEN, these will each open a new tab!
MAX_RESULTS = 5

# AUTO_OPEN will open the received Meraki URLs in your browser.
# AUTO_COPY will copy the received Meraki URL to your clipboard;
# When processing multiple serials, use a clipboard manager like Ditto
# for multiple clips (otherwise you just end up with the last result)
AUTO_OPEN = False
AUTO_COPY = False
