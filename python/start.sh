#!/bin/sh

export WORKON_HOME=~/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
workon cv

python /home/pi/pfe/bouton.py
