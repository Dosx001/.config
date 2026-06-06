#!/bin/bash

if tail -n 1 /etc/hosts | grep -q '^#'; then
  cmd='$ s/^# *//'
else
  cmd='$ s/^/# /'
fi

SUDO_ASKPASS=/usr/bin/ksshaskpass sudo sed -i "$cmd" /etc/hosts
