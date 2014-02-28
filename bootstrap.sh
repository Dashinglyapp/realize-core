#!/usr/bin/env bash

apt-get update -y
apt-get install build-essential -y
cd /vagrant
xargs -a apt-packages.txt apt-get install -y
pip install virtualenvwrapper
pip install -r requirements.txt
