# --------
# Settings
# --------

# The scope should be the same for all environments; you do not have to change anything here.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.device.chromeos.readonly']

# Your API client secret key. Don't share this!
CLIENT_KEY = 'client_key.json'

# Your Meraki Dashboard URL. Log in to see your unique string.
# Don't include the backslash after your instance ID.
# Ex. "n114.meraki.com/Cloverlane-Wif/n/8_SMBcYb"
MERAKI_URL = ''

# An administrative user in your G Suite environment (ties to your service account);
# This user needs to have a role in the API console (which admin users do by default).
# Ex. "user@domain.com"
ADMIN_USER = ''

# Maximum results to return from a serial number query with multiple matches.
# Keep in mind if you use AUTO_OPEN below, these will each open a new tab!
MAX_RESULTS = 5

# AUTO_OPEN will open the received Meraki URLs in your default browser.
# AUTO_COPY will copy the received Meraki URL to your clipboard;
# When processing multiple serials, use a clipboard manager like Ditto
# for multiple clips (otherwise you just end up with the last result)
AUTO_OPEN = True
AUTO_COPY = False
