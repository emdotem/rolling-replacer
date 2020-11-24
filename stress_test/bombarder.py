from datetime import datetime
from time import sleep

import requests

ENDPOINT_URL = ""


def main() -> None:
    i = 0

    while i < 10000:
        response = requests.get(ENDPOINT_URL)

        now = datetime.now()

        now_string = now.strftime("%d/%m/%Y %H:%M:%S")

        if response.status_code == 200:
            print(f"✅ [{now_string}] {response.status_code} {ENDPOINT_URL}")

        if response.status_code != 200:
            print(f"❌ [{now_string}] {response.status_code} {ENDPOINT_URL}")

        sleep(0.2)


if __name__ == "__main__":
    main()
