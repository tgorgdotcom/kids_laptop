import urllib.request
import re
import json
import os


whitelistList = []


def addIfNew(domainStr):
    isWildcard = (domainStr.startswith("@@||") and domainStr.endswith("^"))
    testDomain = domainStr[4:-1] if isWildcard else domainStr
    domainLength = len(testDomain.split("."))
    skipAdd = False

    # check if this has a subdomain and there's already a wildcard rule for the domain on the list
    if (domainLength > 2) and (not isWildcard):
        for index, listItem in enumerate(whitelistList):
            if (listItem.startswith("@@||") and listItem.endswith("^\n")):
                testListItem = listItem[4:-2] # -2 to account for newline and ^
                if testDomain.endswith(testListItem):
                    skipAdd = True
                    break
    
    # check if this is a wildcard rule, and there are subdomain rules on the list, we can remove
    # those now that we're adding the wildcard
    if isWildcard:
        for index, listItem in enumerate(whitelistList):
            if listItem.endswith(testDomain + "\n"):
                del whitelistList[index]
                
    if (not skipAdd) and (domainStr + "\n" not in whitelistList):
        whitelistList.append(domainStr + "\n")


def processDomainNames(baseObj):
    if "requiredDomains" in baseObj:
        for domainName in baseObj["requiredDomains"]:
            addIfNew(domainName)

    if "subGroups" in baseObj:
        for subGroup in baseObj["subGroups"]:
            try:
                for domainName in buildlist["subGroups"][subGroup]:
                    addIfNew(domainName)
            except:
                print(f"Error: {subGroup} was not found, skipping...")


index = 0
homepageTemplate = ""
renderedSites = ""
homepageReqHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36'}
titleRegex = re.compile(r'<\s?title[^<>]*\s?>([^<]*)<\/\s?title\s?>', re.IGNORECASE | re.MULTILINE)

with open("homepage.template.html", "r") as homepageTemplateFile:
    homepageTemplate = homepageTemplateFile.read()

with open("siteblock.template.html", "r") as siteBlockTemplateFile:
    siteBlockTemplate = siteBlockTemplateFile.read()

with open("buildlist.json", "r") as buildlistFile:
    buildlistString = ""

    # allow for comments by removing then befroe processing
    for buildlistStringLine in buildlistFile.readlines():
        commentMatches = re.findall(r"(\"[^\"]*\"|'[^']*')|(\s*\/\/.*)$", buildlistStringLine)

        if (len(commentMatches) > 0) and (commentMatches[-1][1] != ''):
            buildlistString += buildlistStringLine[0:len(commentMatches[-1][1]) * -1]

            # if the comment was not the thing on the line
            if len(commentMatches) > 1:
                buildlistString += "\n"
        else:
            buildlistString += buildlistStringLine

    # remove commas that appear after the last item in an array (also causes json error)
    buildlistString = re.sub(r"(['\"}\]]),(\r?\n\s*[}\]])", r"\1\2", buildlistString)

    try:
        buildlist = json.loads(buildlistString)

    except Exception as e:
        print(str(e))
        exit()

if "sites" in buildlist:
    for buildSite in buildlist["sites"]:
        if "url" not in buildSite:
            continue

        domainFromUrl = buildSite["url"].replace("https://", "").replace("http://", "").replace("/", "")
            
        print(f"Getting info for {domainFromUrl}...")
        processDomainNames(buildSite)

        # make this so subdomains will work
        addIfNew("@@||" + domainFromUrl + "^")

        # get the site icon
        local_path = "img/" + domainFromUrl + ".png"
        site_title = domainFromUrl

        # Skip if we already have an image
        if not os.path.exists(local_path):
            try:
                urllib.request.urlretrieve(f"https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url={remote_url}&size=256", local_path)
            except Exception as err:
                #try to save the default icon
                if hasattr(err, 'code') and (err.code == 404):
                    with open(local_path, "wb") as missingIconFile:
                        missingIconFile.write(err.fp.read())

        if buildSite["title"]:
            site_title = buildSite["title"]

        if index % 6 == 0:
            renderedSites = renderedSites + '<div class="row row-cols-6 row card-row">\n'
            
        renderedSites = renderedSites + siteBlockTemplate.replace("{site_url}", buildSite["url"]).replace("{site_img}", local_path).replace("{site_title}", site_title) + "\n"

        if index % 6 == 5:
            renderedSites = renderedSites + "</div>\n"
        
        index += 1

if "system" in buildlist:
    processDomainNames(buildlist["system"])

with open("index.html", "w") as startFile:
    completedFile = homepageTemplate.replace("{site_list}", renderedSites)
    startFile.write(completedFile)

with open("whitelist.txt", "w") as whitelistFile:
    whitelistFile.writelines(whitelistList)

print("DONE!")