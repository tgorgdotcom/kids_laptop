#!/bin/bash

# create new child
read -r -p "Enter child username: " user_name
sudo useradd $user_name
sudo passwd $user_name

# setup app filter
sudo malcontent-client set-app-filter $user_name \
--disallow-user-installation \
--disallow-system-installation \
app/org.kde.krdc/x86_64/stable \
drugs-alcohol=none \
drugs-narcotics=none \
drugs-tobacco=none \
language-discrimination=none \
language-humor=mild \
language-profanity=none \
money-advertising=none \
money-gambling=none \
money-purchasing=none \
sex-adultery=none \
sex-appearance=none \
sex-homosexuality=none \
sex-nudity=none \
sex-prostitution=none \
sex-themes=none \
social-audio=none \
social-chat=mild \
social-contacts=none \
social-info=mild \
social-location=none \
violence-bloodshed=none \
violence-cartoon=intense \
violence-desecration=none \
violence-fantasy=mild \
violence-realistic=mild \
violence-sexual=none \
violence-slavery=none \
violence-worship=none

# set for 3 hours daily limit and end at 9pm
sudo malcontent-client set-session-limits $user_name daily-limit --daily-limit 10800
sudo malcontent-client set-session-limits $user_name daily-schedule --start-time 03 --end-time 21