#!/usr/bin/env bash
set -e

BASE_DIR=/data/openpilot/installer
python ${BASE_DIR}/make_installer.py
cd ${BASE_DIR} && make all
chmod -R 755 ${BASE_DIR}/installers
rsync -avz ${BASE_DIR}/installers  bwh2:/home/wwwroot/d.sdut.me
