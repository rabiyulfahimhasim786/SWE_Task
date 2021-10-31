import requests
import logging

logger = logging.getLogger(__name__)


def fetchData():
    api_url = "https://api.rootnet.in/covid19-in/stats/history"
    response = requests.get(api_url)
    data = response.json()
    return data


def getStats(states, from_date, to_date, data, altogether):
    logger.info(f'{states}, {from_date}, {to_date}, {altogether}')
    cases = 0
    state_cases = []
    for i in data["data"]:
        day = i["day"]
        if states == None:  # if only date is mentioned
            if from_date == day or to_date == day:
                cases = cases + i["summary"]["total"]
        else:
            if from_date == day or to_date == day:  # if date & state values are present
                regional = i["regional"]
                for j in regional:
                    for state in states:
                        if j["loc"].lower() == state.lower():
                            if altogether:
                                cases = cases + j["totalConfirmed"]
                            else:
                                state_cases.append(
                                    {"state": state, "cases": j["totalConfirmed"]}
                                )

    return {"cases": cases, "state_cases": state_cases}
