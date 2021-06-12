# Get an alarm when a COVID vaccine slot is available

This script retrieves OTP from Google Messages and gets Auth token from COWIN website. It then queries cowin API to check if vaccine slot is available every 20 seconds until the token expires. This is then repeated again in loop.

## Requirements
1. Tampermonkey - https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo
2. Google Messages - https://play.google.com/store/apps/details?id=com.google.android.apps.messaging as the default SMS app on your phone
3. Google Chrome - https://chrome.google.com
4. Python 3 - https://www.python.org/downloads/

## Steps

1. Clone/download this repo.
2. Install required python dependencies
```
pip3 install playsound
pip3 install pycurl
```
3. Set Google Messages as your default SMS app in mobile and Log in to https://messages.google.com/web 
4. Open the conversion in which you get your OTPs. The URL will look similar to https://messages.google.com/web/conversations/12 
5. Create a new script from this page and copy the contents of `copy_to_tampermonkey.js`. Replace the URL in Line 7.
6. Open cowin.py and edit the config. Set the required districtID (see below on how to get districtID of you district), vaccine, dose, min_age_limit.
7. Run `python3 cowin.py`. Then enter your mobile number.
8. `alarm.mp3` will be played when a vaccine slot becomes available. You will see the list of available centers which contains an open slot in terminal.


## How to find district ID?
1. Got to https://cdn-api.co-vin.in/api/v2/admin/location/states and get the `state_id` of your state.
2. Then go to https://cdn-api.co-vin.in/api/v2/admin/location/districts/<state_id> , For ex: Tamilnadu: https://cdn-api.co-vin.in/api/v2/admin/location/districts/31
3. You'll find the district_id of your district in this URL.
