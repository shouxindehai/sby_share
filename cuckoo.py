import requests

REST_URL = "http://192.168.6.128:8090"
SAMPLE_FILE = "./exampleFile"
HEADERS = {"Authorization": "Bearer 123456"}


def createFile():
    url = REST_URL + "/tasks/create/file"
    with open(SAMPLE_FILE, "rb") as sample:
        files = {"file": ("temp_file_name", sample)}
        r = requests.post(url, headers=HEADERS, files=files)

    return r.json()["task_id"]


def createSubmit():
    r = requests.post("http://localhost:8090/tasks/create/submit", files=[
        ("files", open("1.exe", "rb")),
        ("files", open("2.exe", "rb")),
    ], headers=HEADERS)

    # Add your code to error checking for r.status_code.

    submit_id = r.json()["submit_id"]
    task_ids = r.json()["task_ids"]
    errors = r.json()["errors"]

    # Add your code to error checking on "errors".

    # Submit one or more URLs or hashes.
    urls = [
        "google.com", "facebook.com", "cuckoosandbox.org",
    ]
    r = requests.post(
        REST_URL + "/tasks/create/submit",
        headers=HEADERS,
        data={"strings": "\n".join(urls)}
    )


if __name__ == '__main__':
    print(createFile())
