from datetime import datetime, timezone
from passlib.apache import HtpasswdFile
import string
import secrets
import os
import json

import requests
import sseclient

from keyvaluestore import KeyValueStore


def main() -> None:
    project_name = os.environ.get("DISCO_PROJECT_NAME")
    project_domain = os.environ.get("DISCO_PROJECT_DOMAIN")
    api_key = os.environ.get("DISCO_API_KEY")
    assert project_name is not None
    assert project_domain is not None
    assert api_key is not None
    store = KeyValueStore(api_key=api_key, project_name=project_name)
    username, password = create_auth_user()
    store_auth_user(store, username, password)
    set_env_variables(
        api_key=api_key, project_name=project_name, project_domain=project_domain
    )
    use_registry(api_key, project_domain, username, password)


def create_auth_user() -> tuple[str, str]:
    username = generate_str()
    password = generate_str()
    is_new = not os.path.exists("/auth/htpasswd")
    ht = HtpasswdFile("/auth/htpasswd", new=is_new, default_scheme="bcrypt")
    ht.set_password(username, password)
    ht.save()
    return username, password


CREDENTIALS_KEY = "CREDENTIALS"


def store_auth_user(store: KeyValueStore, username: str, password: str) -> None:
    def update_func(value: str | None) -> str:
        if value is None:
            credentials: dict[str, dict[str, dict[str, str]]] = {"users": {}}
        else:
            credentials = json.loads(value)
        credentials["users"][username] = {
            "created": datetime.now(timezone.utc).isoformat(),
            "password": password,
        }
        new_value = json.dumps(credentials)
        return new_value

    store.update(key=CREDENTIALS_KEY, update_func=update_func)


def assert_status_code(response, status_code) -> None:
    if response.status_code != status_code:
        raise Exception(
            f"Response status code not {status_code}, "
            f"reveived {response.status_code}: {response.text}"
        )


def set_env_variables(api_key: str, project_name: str, project_domain: str) -> None:
    url = f"http://disco/projects/{project_name}/env"
    req_body = {
        "envVariables": [
            {
                "name": "REGISTRY_HTTP_HOST",
                "value": f"https://{project_domain}",
            },
            {
                "name": "REGISTRY_AUTH",
                "value": "htpasswd",
            },
            {
                "name": "REGISTRY_AUTH_HTPASSWD_REALM",
                "value": "Registry Realm",
            },
            {
                "name": "REGISTRY_AUTH_HTPASSWD_PATH",
                "value": "/auth/htpasswd",
            },
        ],
    }
    response = requests.post(
        url,
        json=req_body,
        auth=(api_key, ""),
        headers={"Accept": "application/json"},
        timeout=10,
    )
    assert_status_code(response, 200)
    resp_body = response.json()
    assert resp_body["deployment"] is not None
    url = f"http://disco/.disco/projects/{project_name}/deployments/{resp_body['deployment']['number']}/output"
    response = requests.get(
        url,
        auth=(api_key, ""),
        headers={"Accept": "text/event-stream"},
        stream=True,
    )
    for event in sseclient.SSEClient(response).events():
        output = json.loads(event.data)
        print(output["text"], end="")


def use_registry(
    api_key: str, project_domain: str, username: str, password: str
) -> None:
    url = "http://disco/.disco/meta/registry"
    req_body = {
        "host": project_domain,
        "authType": "basic",
        "username": username,
        "password": password,
    }
    response = requests.post(
        url,
        json=req_body,
        auth=(api_key, ""),
        headers={"Accept": "application/json"},
    )
    assert_status_code(response, 200)


def generate_str() -> str:
    alphabet = string.ascii_letters + string.digits
    first_char = secrets.choice(string.ascii_letters)
    rest = "".join(secrets.choice(alphabet) for _ in range(15))
    return first_char + rest


if __name__ == "__main__":
    main()
