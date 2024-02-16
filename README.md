# Twitter Trends Fetcher

This is a simple Python script that fetches the current trends in Twitter in any specified country.

This is supposed to serve as a prototype that can be built upon to turn into something more established such as a CLI using [click](https://click.palletsprojects.com/en/8.1.x/). 

## Requirements
This only has two direct dependencies: [requests](https://requests.readthedocs.io/en/latest/) which is used to communicate with the twitter API and [prettytable](https://pypi.org/project/prettytable/) which is used to cleanly output the trends in a table.

```bash
pip install requests prettytable

```
**_OR_**

```bash
pip install -r requirements.txt
```

## `credentials.json`?
These are the comments straight from the code explaining what that's about:
```
# This is the path to the credentials file that needs to have "bearer_token", "auth_token", "csrf_token";
# these can be extracted in a browser (using developer's tools [F12]);
# they can be found in the headers of any request on an active twitter session;
# "bearer_token" is in the "Authorization" header (make sure to leave out the word "Bearer");
# "auth_token" can be found in the "cookies" header, along side other cookie items;
# "csrf_token" can be found in the "x-csrf-token" header.
# The template for the file can be found in `example_credentials.json`.
#
# This is a bypass to the (somewhat) new Twitter API changes,
# where trends can't be accessed with the free API access tier. 
CREDS_FILE_PATH = "./credentials.json"
```

## Notes
This was created as a part of the technical interview process for an internship at [Maida.co](https://maida.co)