import json

import uvicorn
from fastapi import FastAPI, status, Response
from typing import Any
from functionality import crud

app = FastAPI()


@app.get("/dependency/info/{dependency_name}", status_code=status.HTTP_200_OK)
def get_dependency_name(dependency_name: str, resp: Response) -> Any:

    # extract data from json file
    data = crud.get_dependencies()
    # check if dependency has typr devDependencies
    if dependency_name in data["devDependencies"]:
        # response with two instances as version and type
        response = dict(version=data["devDependencies"][dependency_name], type="devDependencies")

    # check if dependency has type dependencies
    elif dependency_name in data["dependencies"]:
        # response with two instances as version and type
        response = dict(version=data["dependencies"][dependency_name], type="devDependencies")

    else:
        resp.status_code = status.HTTP_404_NOT_FOUND
        # response as object not found
        response = dict(details="dependencies not found")

    return json.dumps(response)


@app.get("/dependency/version-check/{dependency_name}", status_code=status.HTTP_200_OK)
def check_dependency_version(dependency_name: str, resp: Response) -> Any:
    current_version = ""
    # extract data from json file
    data = crud.get_dependencies()
    if dependency_name in data["devDependencies"]:
        current_version = data["devDependencies"][dependency_name]
    elif dependency_name in data["dependencies"]:
        current_version = data["dependencies"][dependency_name]
    else:
        resp.status_code = status.HTTP_404_NOT_FOUND
        # response as object not found
        return dict(details="dependencies not found")

    # get newest version
    newest_version = crud.get_version_data(dependency_name=dependency_name)
    # status boolean codes for updates
    response = crud.version_update_status(current_version=current_version, newest_version=newest_version)

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5004)
