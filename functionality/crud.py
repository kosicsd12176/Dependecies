from typing import Dict, Any
import json
import requests


def get_dependencies() -> Dict:
    """
    Export data from file as dictionary from json
    :return: dependencies in dict type
    """

    # JSON file
    f = open('./data/deps.json', "r")
    # Reading from file
    data = json.loads(f.read())
    # Closing file
    f.close()
    return data


def get_version_data(dependency_name: str) -> Dict:
    """
    This method handles an external api request to extract data for current dependency
    :param dependency_name: name of dependency
    :return: dependency's latest version
    """
    # request on external api pull data for dependency
    response = requests.get(f'https://registry.npmjs.org/{dependency_name}')
    # transform to json type
    res = response.json()
    # return the latest version of dependency
    return res["dist-tags"]["latest"]


def version_update_status(current_version: str, newest_version: str) -> Dict:
    """
    Process controls the need of updating semantic versions
    :param current_version: the installed version
    :param newest_version: the newest version has published
    :return: status boolean codes for each semantic version
    """
    response = {}
    versions = ["major", "minor", "patch"]

    # iterate through each version based semantic versioning
    for index, current_version in enumerate(current_version.split(".")):
        # check if any version needs update so update the response status
        if current_version < newest_version.split(".")[index]:
            response[versions[index]] = True
        else:
            response[versions[index]] = False

    return response
