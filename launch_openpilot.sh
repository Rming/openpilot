#!/usr/bin/bash

/usr/bin/sh /data/openpilot/fonts/chinese-fonts/installer.sh &
export PASSIVE="0"
exec ./launch_chffrplus.sh

