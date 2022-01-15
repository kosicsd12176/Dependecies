import json
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


def test_dependency_dont_exist():
    from app import app
    client = TestClient(app)

    with patch("functionality.crud.get_dependencies") as mock_response:
        mock_response.return_value = MagicMock(
            return_value=json.dumps({'dependencies':
                              {'moment': '2.29.1',
                               'react': '16.6.0',
                               'react-dom': '16.6.0',
                               'react-redux': '6.0.0',
                               'react-scripts': '3.0.1',
                               'redux': '3.0.0',
                               'redux-thunk': '2.1.0',
                               'redux-v10': '3.0.0'},
                          'devDependencies':
                              {'eslint': '6.0.0'}})
        )
        response = client.get("/dependency/info/unknown")
        assert response.status_code == 404
