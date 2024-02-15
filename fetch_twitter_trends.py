from prettytable import PrettyTable
import requests
import json
import os




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

# This is the path to the locations file that contains the `place_id` attribute for all countries.
# The script creates this file automatically if it's not found.
LOCS_FILE_PATH = "./locations.json"

# "Renew the locations file even if it exists".
RENEW_LOCS = False

# The default country to fetch the trends of.
DEFAULT_LOC = "Pakistan"

# The default number of trends entries to fetch.
DEFAULT_COUNT = 20

# Twitter API link
API = "https://twitter.com/i/api/2"





def main() -> None:
    session = get_session()

    if RENEW_LOCS or not os.path.exists(LOCS_FILE_PATH):
        locs_list = get_twitter_locs(session=session)
        locs_dict = get_locs_dict(locs_list=locs_list)
        save_locs_file(locs_dict=locs_dict)
    
    else:
        locs_dict = load_locs_file()
    
    loc_id = get_loc_id(locs_dict=locs_dict)
    set_twitter_trends_loc(session=session, loc_id=loc_id)
    timeline_list = get_twitter_timeline(session=session)
    trends = get_trends_from_timeline(timeline_list=timeline_list)

    table = tablize_trends(trends=trends)
    print(table)



def get_session(creds_file_path : str = CREDS_FILE_PATH) -> requests.Session:
    session = requests.Session()
    with open(creds_file_path, "r", encoding="UTF-8") as creds_file:
        creds = json.load(creds_file)
        bearer_token = creds["bearer_token"]
        auth_token = creds["auth_token"]
        csrf_token = creds["csrf_token"]

        headers = {
            "authorization": "Bearer " + bearer_token,
            "x-csrf-token": csrf_token
        }

        cookies = {
            "auth_token": auth_token,
            "ct0": csrf_token
        }

        session.headers.update(headers)
        session.cookies.update(cookies)
    
    return session



def get_twitter_locs(session: requests.Session) -> list:
    endpoint = "/guide/explore_locations_with_auto_complete.json"
    full_path = API + endpoint

    locs_response = session.get(url=full_path)
    locs_json = locs_response.text
    locs_list = json.loads(locs_json)
    
    return locs_list


def get_twitter_timeline(session: requests.Session, count: int = DEFAULT_COUNT) -> dict:
    endpoint = "/guide.json"
    full_path = API + endpoint

    params = {
        "count": count,
        "candidate_source": "trends"
    }

    timeline_response = session.get(url=full_path, params=params)
    timeline_json = timeline_response.text
    timeline_dict = json.loads(timeline_json)

    return timeline_dict


def set_twitter_trends_loc(session: requests.Session, loc_id: int) -> None:
    endpoint = "/guide/set_explore_settings.json"
    full_path = API + endpoint

    data = {
        "places": loc_id
    }

    session.post(url=full_path, data=data)



def get_locs_dict(locs_list: list) -> dict:
    locs_dict = { loc["name"]: loc["place_id"] for loc in locs_list }

    return locs_dict


def save_locs_file(locs_dict: dict, locs_file_path: str = LOCS_FILE_PATH) -> str:
    with open(locs_file_path, "w", encoding="UTF-8") as locs_file:
        json.dump(locs_dict, locs_file, indent=4, sort_keys=True)
        
        return locs_file_path


def load_locs_file(locs_file_path: str = LOCS_FILE_PATH) -> dict:
    with open(locs_file_path, "r", encoding="UTF-8") as locs_file:
        locs_dict = json.load(locs_file)
    
        return locs_dict


def get_loc_id(locs_dict: dict, loc_name: str = DEFAULT_LOC) -> int:
    return locs_dict[loc_name] if loc_name in locs_dict else locs_dict[DEFAULT_LOC]


def get_trends_from_timeline(timeline_list: list) -> list:
    content_list = timeline_list["timeline"]["instructions"]

    trends = list()
    for content_item in content_list:
        if "addEntries" in content_item:
            entries = content_item["addEntries"]["entries"]
            for entry in entries:
                if "entryId" in entry and entry["entryId"] == "trends":
                    trends_list = entry["content"]["timelineModule"]["items"]
                    for trend_object in trends_list:
                        trend = trend_object["item"]["content"]["trend"]
                        trends.append({
                            "rank": trend["rank"],
                            "name": trend["name"],
                            "desc": trend["trendMetadata"]["metaDescription"] if "metaDescription" in trend["trendMetadata"] else ""
                        })
                    
                    return trends



def tablize_trends(trends: dict) -> PrettyTable:
    table = PrettyTable()
    table.field_names = ["Rank", "Trend", "Description"]
    
    for trend in trends:
        table.add_row([trend["rank"], trend["name"], trend["desc"]])
    
    return table




if __name__ == "__main__":
    main()