#!/usr/bin/bash

###############################################################################
# The MIT License
#
# Copyright (c) 2019-, Rick Lan, dragonpilot community, and a number of other of contributors.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Noto is a trademark of Google Inc. Noto fonts are open source.
# All Noto fonts are published under the SIL Open Font License,
# Version 1.1. Language data and some sample texts are from the Unicode CLDR project.
#
###############################################################################


# Android system locale, zh-TW = Traditional Chinese, zh-CN = Simplified Chinese
lang=zh-CN

update_font=0
remove_old_font=0

# check regular font
if [ ! -f "/system/fonts/NotoSansCJKtc-Regular.otf" ]; then
    update_font=1
fi

# check miui font
if ls /system/fonts/Miui*.ttf 1> /dev/null 2>&1; then
    remove_old_font=1
fi

if [ $update_font -eq "1" ] || [ $remove_old_font -eq "1" ]; then
    # sleep 3 secs in case, make sure the /system is re-mountable
    sleep 3
    mount -o remount,rw /system
    if [ $update_font -eq "1" ]; then
        # install font
        cp -rf /data/openpilot/fonts/chinese-fonts/NotoSansCJKtc-* /system/fonts/
        # install font mapping
        cp -rf /data/openpilot/fonts/chinese-fonts/fonts.xml /system/etc/fonts.xml
        # change permissions
        chmod 644 /system/etc/fonts.xml
        chmod 644 /system/fonts/NotoSansCJKtc-*
    fi
    # remove miui font
    if [ $remove_old_font -eq "1" ]; then
        rm -fr /system/fonts/Miui*.ttf
    fi
    mount -o remount,r /system
    # change system locale
fi

setprop persist.sys.locale $lang
setprop persist.sys.local $lang
