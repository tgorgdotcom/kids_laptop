with open("whitelist.txt", "w") as finalList:
    with open("kids_allowlist.txt", "r") as systemList:
        finalList.write(systemList.read())

    with open("system_allowlist.txt", "r") as systemList:
        finalList.write(systemList.read())