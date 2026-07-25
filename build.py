import urllib.request
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
with open("start.template.html", "r") as templateFile:
    htmlTemplate = templateFile.read()

with open("site.template.html", "r") as siteTemplateFile:
    siteTemplate = siteTemplateFile.read()

with open("whitelist.txt", "w") as finalList:
    with open("kids_allowlist.txt", "r") as kidsList:
        for domainName in kidsList.readline():
            # get the site icon
            remote_url = "https://" + domainName
            local_filename = domainName + ".png"
            local_path = "startpage/" + local_filename
            site_title = domainName
            urllib.request.urlretrieve(f"https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url={remote_url}&size=256", local_path)

            # look for the title of the homepage
            with urllib.request.urlopen(remote_url) as response:
                tmpTitleParser = TitleParser()
                tmpTitleParser.feed(response.read().decode("utf-8"))
                site_title = tmpTitleParser.title.strip()
        
            renderedSites = renderedSites + siteTemplate.replace("{site_url}", remote_url).replace("{site_img}", local_filename).replace("{site_title}", site_title)

            finalList.writelines(domainName)
            
    with open("system_allowlist.txt", "r") as systemList:
        finalList.write(systemList.read())

with open("startpage/index.html", "w") as startFile:
    completedFile = htmlTemplate.replace("{site_list}", renderedSites)
    startFile.write(completedFile)
