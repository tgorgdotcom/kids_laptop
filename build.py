import urllib.request
import json
from html.parser import HTMLParser


class TitleParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


htmlTemplate = ""
renderedSites = ""
homepageReqHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36'}

with open("start.template.html", "r") as templateFile:
    htmlTemplate = templateFile.read()

with open("site.template.html", "r") as siteTemplateFile:
    siteTemplate = siteTemplateFile.read()

with open("whitelist.txt", "w") as finalList:
    with open("kids_allowlist.txt", "r") as kidsList:

        index = 0
        for domainName in kidsList.readlines():
            if domainName.startswith("#"):
                continue

            # get the site icon
            domainName = domainName.strip()
            remote_url = "https://" + domainName
            local_path = "img/" + domainName + ".png"
            site_title = domainName

            print(f"Getting info for {domainName}...")

            try:
                urllib.request.urlretrieve(f"https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url={remote_url}&size=256", local_path)
            except Exception as err:
                #try to save the default icon
                if hasattr(err, 'code') and (err.code == 404):
                    with open(local_path, "wb") as missingIconFile:
                        missingIconFile.write(err.fp.read())


            homepageReq = urllib.request.Request(remote_url, headers=homepageReqHeaders)

            # look for the title of the homepage
            try:
                with urllib.request.urlopen(homepageReq, timeout=10) as response:
                    tmpTitleParser = TitleParser()
                    tmpTitleParser.feed(response.read().decode("utf-8", errors='ignore'))
                    site_title = tmpTitleParser.title.strip().replace('"', '&quot;')

            except Exception as err:
                pass

            if index % 6 == 0:
                renderedSites = renderedSites + '<div class="row row-cols-6 row card-row">'
                
            renderedSites = renderedSites + siteTemplate.replace("{site_url}", remote_url).replace("{site_img}", local_path).replace("{site_title}", site_title)

            if index % 6 == 5:
                renderedSites = renderedSites + "</div>"
                
            finalList.write(domainName + "\n")
            index += 1
            
    with open("system_allowlist.txt", "r") as systemList:
        finalList.write(systemList.read())

unsplash_api = input("Please enter the unsplash API key: ")
random_image = ""

# look for the title of the homepage
with urllib.request.urlopen(f"https://api.unsplash.com/photos/random?client_id={unsplash_api}&orientation=landscape&content_filter=high&query=fun%20backgrounds") as response:
    randomImageResult = json.loads(response.read())

with open("index.html", "w") as startFile:
    completedFile = htmlTemplate.replace("{site_list}", renderedSites).replace("{random_image}", randomImageResult['urls']['regular']).replace("{artist_name}", randomImageResult['user']['username'])
    startFile.write(completedFile)
