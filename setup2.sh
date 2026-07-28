
sudo sqlite3 /etc/pihole/gravity.db "UPDATE adlist SET enabled=0 WHERE id=0;"
sudo sqlite3 /etc/pihole/gravity.db "INSERT INTO adlist (address, enabled, comment) VALUES ('https://raw.githubusercontent.com/tgorgdotcom/kids_laptop/refs/heads/main/whitelist.txt', 1, 'tgorgs whitelist');"
sudo podman exec -it systemd-pihole pihole -g
sudo podman exec -it systemd-pihole pihole deny --regex '.*'
sudo pihole-FTL --config dns.cnameRecords '["www.youtube.com,restrict.youtube.com","m.youtube.com,restrict.youtube.com","youtubei.googleapis.com,restrict.youtube.com","youtube.googleapis.com,restrict.youtube.com","www.youtube-nocookie.com,restrict.youtube.com"]'
sudo pihole-FTL --config dns.cnameRecords '["www.google.com,forcesafesearch.google.com"]'