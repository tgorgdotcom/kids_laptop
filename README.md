# Kids' Laptops setup

This is how I'm setting up my kids' laptops.  Maybe you'll find it useful too.


## Why?

There's a few alternatives:

- Google Chrome OS Flex: I was using this for awhile, and it has a great web restriction interface via Family Link, but it doesn't allow kid accounts to run Linux apps (i.e. Minecraft) and does not have a lot of apps.

- Windows: costs money to upgrade from my old laptops

Instead, I'll be installing Linux.  Fedora Kinoite is the KDE version of Fedora Silverblue, an atomic/immutable version of Fedora.  Immutable means it's really hard to change the core os, and adds some protection against the kids breaking the system (I still remember the time, when I was young, when I thought I'd try formatting the C: drive, it didn't end well).

Additionally, I'll be using pihole to only allow permitted sites (this will be for kids from 6-9ish).  I'll switch to a more permissive solution as my kids get older.  I'm also using `malcontent` to add additional protections against installing flatpaks, and creating my own little "start page" for the kids to see when they open up a browser.

Pull requests for kid sites to be added are most welcome.


## Getting Started

### Initial setup

1. Install Fedora Kinote (check around the web for instructions - it's pretty much the same as other Linux distros)
2. Setup an internet connection
3. Run included setup.sh.  It will:
   - Remove Firefox icon (just a preference)<br>
     https://docs.fedoraproject.org/en-US/atomic-desktops/tips-and-tricks/#_hiding_the_default_browser_firefox
     - Note that this will not remove firefox entry from favorites or taskbar
   - Install Google Chrome<br>
     `flatpak install com.google.Chrome`
   - Install malcontent (Parental Control) into ostree<br>
     `sudo rpm-ostree install malcontent malcontent-tools malcontent-control`
   - Place pihole.container in /etc/containers/systemd folder
   - Make /etc/pihole folder
   - Run systemctl daemon-reload
   - Create a podman secret for the password<br>
     `echo -n "xxxx" | sudo podman secret create pihole_password -`
   - Make system use pihole for DNS
   - Reboot

4. After reboot, go to the PiHole admin https://pi.hole/admin and login using your password
5. Add the allowlist url https://raw.githubusercontent.com/tgorgdotcom/kids_laptop/refs/heads/main/whitelist.txt
6. Disable the builtin "StevenBlack/hosts" blocklist
7. Add the allow site pi.hole
8. Add the regex block site all (.*) 

### Adding a child user:

Use childSetup.sh.  It will:
  - Create the child user
  - Set Screen time (I use 3hrs)
  - Set Bed time (9:00pm)
  - restrict krdc application
  - restrict installing applications
  - set app suitability to everyone

Optionally, set your child's browser to go to https://tgorgdotcom.github.io/kids_laptop/
