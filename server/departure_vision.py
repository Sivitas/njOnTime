from bs4 import BeautifulSoup
import requests
import re


def get_train_schedule():
    station_list = ["MP"]

    for station in station_list:
        page = requests.get("http://dv.njtransit.com/mobile/tid-mobile.aspx?sid=" + station).text
        soup = BeautifulSoup(page)

        all_rows = soup.find_all("tr")[2:]

        departure_list = []

        for row in all_rows:
            info_dict = {}
            all_cols = row.find_all("td")

            if len(all_cols) == 7:
                info_dict["departureTime"] = all_cols[1].text.strip()
                info_dict["destination"] = all_cols[2].text.strip()
                info_dict["track"] = all_cols[3].text.strip()
                info_dict["line"] = all_cols[4].text.strip()
                info_dict["train"] = all_cols[5].text.strip()
                info_dict["status"] = all_cols[6].text.strip()

            if len(all_cols) == 6:
                info_dict["departureTime"] = all_cols[0].text.strip()
                info_dict["destination"] = all_cols[1].text.strip()
                info_dict["track"] = all_cols[2].text.strip()
                info_dict["line"] = all_cols[3].text.strip()
                info_dict["train"] = all_cols[4].text.strip()
                info_dict["status"] = all_cols[5].text.strip()

            line_dict = {"Northeast Corrdr": "NEC"}
            if info_dict["line"] in line_dict:
                info_dict["line"] = line_dict[info_dict["line"]]

            encoded_str = info_dict["destination"].encode("ascii", "ignore")
            info_dict["destination"] = encoded_str

            if "A" not in info_dict["train"]:
                departure_list.append(info_dict)

    return departure_list

# git test
