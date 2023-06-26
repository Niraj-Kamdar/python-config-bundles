import json
from polywrap_client_config_builder import PolywrapClientConfigBuilder
from polywrap_core import Uri
from polywrap_client import PolywrapClient
from polywrap_sys_config_bundle import get_sys_config


def test_sanity():
    config = PolywrapClientConfigBuilder().add(get_sys_config()).build()
    client = PolywrapClient(config)

    response = client.invoke(
        uri=Uri.from_str("ens/wraps.eth:http@1.1.0"),
        method="get",
        args={"url": "https://jsonplaceholder.typicode.com/todos/1"},
    )

    assert response["status"] == 200
    assert response["body"] is not None
    assert json.loads(response["body"])["id"] == 1
