import requests
import zipfile


DOWNLOAD_LINK = 'https://files.de-1.osf.io/v1/resources' \
                '/f8n3g/providers/osfstorage/6321cf89d88c070f879d0d11/?zip='


def download(url, output):
    r = requests.get(url)
    with open(output, "wb") as file:
        file.write(r.content)


if __name__ == '__main__':
    download(DOWNLOAD_LINK, 'examples.zip')
    zipfile.ZipFile('examples.zip').extractall()


