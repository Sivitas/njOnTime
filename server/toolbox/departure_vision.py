from bs4 import BeautifulSoup
import requests
import re


def get_corrected_time(time, time_of_day):
    if time_of_day == "PM":
        corrected_hour = int(time.split(":")[0]) + 12
        if corrected_hour > 24:
            corrected_hour = corrected_hour - 24
            if corrected_hour == 0:
                corrected_hour = "00"
        corrected_time = str(corrected_hour) + ":" + time.split(":")[1]
    else:
        corrected_time = time
    return corrected_time

def get_train_schedule(station):
    page = requests.get("http://dv.njtransit.com/mobile/tid-mobile.aspx?sid=" + station).text
    soup = BeautifulSoup(page)

    # determine if AM or PM to generate correct 24 hour time data
    time_of_day = soup.find("span", attrs={"id": "Label2"}).text.split(" ")[1]



    departure_list = []
    # loop thru all the rows and generate an info dict with train data
    all_rows = soup.find_all("tr")[2:]
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

        # remove amtrak trains
        if "A" in info_dict["train"]:
            continue

        # get corrected time
        info_dict["departureTime"] = get_corrected_time(info_dict["departureTime"], time_of_day)

        line_dict = {"Northeast Corrdr": "NEC"}
        if info_dict["line"] in line_dict:
            info_dict["line"] = line_dict[info_dict["line"]]


        encoded_str = info_dict["destination"].encode("ascii", "ignore")
        info_dict["destination"] = encoded_str

        # get the details for each train number
        # and add the details to a detail_dict to add to info_dict later
        details_dict = {}
        details_page = requests.get("http://dv.njtransit.com/mobile/train_stops.aspx?sid=" + station + "&train=" + info_dict["train"]).text
        details_soup = BeautifulSoup(details_page)

        # first row is not included in all_details_rows parse separately
        first_row = details_soup.p
        first_row_station = first_row.decode_contents().split("<i>")[0].strip()
        # row status has <i>DEPARTED</i>
        try:
            first_row_status = first_row.i.text
        # row status is a time value
        except AttributeError:
            time_index = len(first_row.text.split("at")) - 1
            first_row_status = first_row.text.split("at")[time_index].strip()
            try:
                first_row_status = get_corrected_time(first_row_status, time_of_day)
            except ValueError:
                import ipdb;ipdb.set_trace()
        details_dict[first_row_station] = first_row_status

        # parse the rest of the rows now and add statuses to details_dict
        all_details_rows = details_soup.find_all("tr")
        for row in all_details_rows:
            # pass empty rows
            if len(row.text) < 3:
                continue
            try:
                row_station = row.p.decode_contents().split("<i>")[0].strip()
                # split again if "at" detected in row_station
                if "at" in row_station:
                    row_station = row_station.split("at")[0].strip()
            except AttributeError:
                row_station = row.p.text.split("at")[0].strip()
            try:
                row_status = row.i.text
            except AttributeError:
                time_index = len(row.p.text.split("at")) - 1
                row_status = row.p.text.split("at")[time_index].strip()
                try:
                    row_status = get_corrected_time(row_status, time_of_day)
                except ValueError:
                    import ipdb;ipdb.set_trace()
            details_dict[row_station] = row_status

        # add details_dict to info_dict under "details"
        info_dict["details"] = details_dict

        # add info_dict to the departure list
        departure_list.append(info_dict)

    import ipdb;ipdb.set_trace()
    return departure_list

