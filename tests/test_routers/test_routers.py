import json
import pytest
from dataclasses import asdict
from fastapi.testclient import TestClient
from app.main import app
from app.model.BenchmarkModel import Benchmark


# CONSTANTS
def get_client():
    """
    Get the fastapi test client.
    :return:
    """
    return TestClient(app)


def get_some_other_static_info():
    """
    Use functions outside of the TestClass-Scope to get global infos
    :return:
    """
    return "ThisIsAnGlobalInfo"

def get_benchmark_data():
    return {
          "name": "string",
          "number": 0,
          "another_class": {
            "nested_name": "string",
            "nested_number": 0
          }
        }

class TestConfigRouter:
    """
    Tests for the config router
    """

    def test_health_endpoint(self):
        # get the test client (Test instance of the fastapi-app)
        client = get_client()
        # the enpoint to test
        endpoint = "/actuator/health/"
        # Make the appropriate request
        response = client.get(endpoint)
        # do the needed testing with assert
        assert response.status_code == 200
        # just optinal printing for you
        print(response.json())

class TestBenchmarkRouter:
    """

    """

    def test_post_and_return_modified_endpoint(self):
        # get the test client (Test instance of the fastapi-app)
        client = get_client()
        # the enpoint to test
        endpoint = "/benchmark/json/post_and_return_modified"
        payload = get_benchmark_data()
        response = client.post(endpoint, json=payload)
        assert response.status_code == 200
        benchmark_data = Benchmark(**response.json())
        assert benchmark_data.number == 1
        # you could also use the plain json:
        assert response.json()["number"] == 1
