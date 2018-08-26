from smtplib import SMTP
import re
import requests
import os
import dotenv

dotenv.load_dotenv()


response = requests.get("http://fmel.ch/en/no-tenant/applying-for-a-room/registration", headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
})
match = re.search("<strong>REGISTRATION CLOSED</strong>", response.text)

if match is None:
    client = SMTP()
    client.connect("smtp-mail.outlook.com", port=587)
    client.ehlo()
    client.starttls()
    client.ehlo()
    client.login(os.getenv("USER"), os.getenv("PASSWORD"))

    message = """\
    From: {USER}
    To: {TO}
    Subject: FMEL registration open

    FMEL registration open
    """.format(USER=os.getenv("USER"), TO=os.getenv("TO_JAKOB"))

    client.sendmail(os.getenv("USER"), os.getenv("TO_JAKOB"), message)
    client.sendmail(os.getenv("USER"), os.getenv("TO_LOUISE"), message)

    client.quit()