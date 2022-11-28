from turtle import down
import requests


DOWNLOAD_LINK = 'https://osf.io/download/djycu/'


def download(url, output):
    r = requests.get(url)
    with open(output, "wb") as file:
        file.write(r.content)


if __name__ == '__main__':
    download(DOWNLOAD_LINK, 'model.pkl')
