---
layout: post
title: "Create splunk template"
date: 2026-04-01
categories: [tools]
tags: [splunk]
---

### Add key

```shell
ssh-import-id-gh <github_name>
```

### Change hostname

```shell
sudo hostnamectl set-hostname <new_hostname>
sudo systemctl restart systemd-hostnamed
```

### Create new machine-id

```shell
rm -r /etc/machine-id
systemd-machine-id-setup
new-name
```

### Limit ip permission

```shell
cd /etc/netplan
sudo chmod 600 *.yaml
sudo netplan try
```

### Create new disk for splunk

### Download and install splunk

```shell
wget -O splunk-9.2.1-78803f08aabb-Linux-x86_64.tgz "https://download.splunk.com/products/splunk/releases/9.2.1/linux/splunk-9.2.1-78803f08aabb-Linux-x86_64.tgz"
sudo tar -xvzf splunk-9.2.1-78803f08aabb-Linux-x86_64.tgz -C /app
cd /app/splunk/bin
./splunk start
./splunk enable boot-start -systemd-managed 0 (to run when boot)
```

### Permission for splunk user

```shell
export SPLUNK_HOME=/app/splunk
sudo chown -R splunk:splunk $SPLUNK_HOME
sudo chown -R splunk $SPLUNK_HOME
```

### Edit file host for custom domain

```shell
sudo nano /etc/hosts
10.11.13.54 sh01.splunk.cyberrange.local
10.11.13.47 indexer-01.splunk.cyberrange.local
10.11.13.48 indexer-02.splunk.cyberrange.local
10.11.13.44 manage-node.splunk.cyberrange.local
10.11.13.66 heavyforwader.splunk.cyberrange.local
```

### Setup NTP

```shell
sudo timedatectl set-timezone Asia/Ho_Chi_Minh
nano /etc/systemd/timesyncd.conf
	-> uncomment ls NTP and add values, example (NTP=10.11.13.254, NTP=0.ubuntu.pool.ntp.org, NTP=10.11.13.254 ...)
systemctl restart systemd-timesyncd
```

### Disable **Transparent huge pages**

```shell
nano /etc/systemd/system/disable-thp.service
```

```shell
[Unit]
Description=Disable Transparent Huge Pages
DefaultDependencies=no
After=sysinit.target local-fs.target
Before=basic.target

[Service]
Type=oneshot
ExecStart=/bin/sh -c '/bin/echo never > /sys/kernel/mm/transparent_hugepage/enabled'
ExecStart=/bin/sh -c '/bin/echo never > /sys/kernel/mm/transparent_hugepage/defrag'

[Install]
WantedBy=basic.target
```

```shell
sudo systemctl daemon-reload
sudo systemctl enable disable-thp
sudo service disable-thp start
```

```shell
cat /sys/kernel/mm/transparent_hugepage/enabled
cat /sys/kernel/mm/transparent_hugepage/defrag
```

### Install network tools

```shell
sudo apt-get install net-tools tcpdump wget telnet traceroute open-vm-tools lsof -y
```

### Edit ~/.profile and ~/.bashrc

```shell
echo "TMOUT=900" >> ~/.bashrc
source ~/.bashrc
tail ~/.bashrc

echo "export SPLUNK_HOME=/app/splunk" >> ~/.profile
source ~/.profile
tail ~/.profile
```

### Delete splunk user from sudo group and adm group

```shell
#Create new user name vss and add to sudo & adm group
sudo adduser vss
sudo usermod -aG sudo vss
sudo usermod -aG adm vss

#Delete usersplunk from sudo group
sudo nano /etc/group
	Delete splunk in (sudo:x:27:splunk,vss) & (adm:x:4:syslog,splunk,vss)

#Check command
id splunk
	uid=1000(splunk) gid=1000(splunk) groups=1000(splunk),24(cdrom),30(dip),46(plugdev),110(lxd)
id vss
	uid=1001(vss) gid=1001(vss) groups=1001(vss),4(adm),27(sudo)
```

