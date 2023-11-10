import requests
from os.path import isfile
from bs4 import BeautifulSoup
import time

WEBHOOK_URL = ""
def main():
    url = "https://www.jascentralohio.org/survival"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0"}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("Not 200")
        return
    soup = BeautifulSoup(r.content, "html.parser")
    results = soup.find(id="allWrapper")
    new_content = str(results)

    if isfile("last_run.html"):
        with open("last_run.html", "r", encoding="utf-8") as f:
            old_content = f.read()
    else:
        old_content = new_content

    new_content = new_content.replace("\r", "")

    if new_content != old_content:
        message = f"Survival class page has changed!\n{url}"
        payload = {"content": message}
        r = requests.post(WEBHOOK_URL, json=payload)
        t=time.time()
        with open(f"old_{t}.html", "w", encoding="utf-8") as f:
            f.write(old_content)
        with open(f"new_{t}.html", "w", encoding="utf-8") as f:
            f.write(new_content)

    with open("last_run.html", "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    main()
