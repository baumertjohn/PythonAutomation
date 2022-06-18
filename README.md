# Overnight Temps via SMS

## A 100 Days of Code capstone project for Day 97 - Python Automation

This project acquires a 7 day forcast from weather.gov for a given location. The data is parsed to build an overnight temperature message and the location is used to find the closest town/city to add to the message (via geonames.org).  Once this is complete, an SMS is sent with the results. The SMS message is sent via a Gmail account to the appropriate carrier "email".

## How To:

An .env file with following will need to be created:
1. **MY_EMAIL** - An email address to send the SMS **FROM**
2. **PASSWORD** - The password for the above email address - *if Gmail, this will need to be an application specific password*
3. **SMTP_ADDRESS** - For the send from email
4. **PHONE** - The number to send (email) the SMS **TO** - *example 5558675309<span>@</span>vzwpix.com (for a Verizon number)*
5. **GEONAME_USER** - Username for the api.geonames.org website - *for finding closest city/town to weather search*
    * *This requires a free account*
6. **HOME_LOCATION** - The location to gather weather from api.weather.gov in the form of AAA/##,##

## Known Issues
Occasionally, weather.gov will not return data.  This will cause the program to stop and not send the SMS.  I implemented a "try/except" block to send an alternative message (which still needs refined), but ultimately would like to add a feature to retry the request for a set number of times with a pause to avoid "spamming" the weather.gov server.
