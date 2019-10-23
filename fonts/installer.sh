#!/usr/bin/bash

# Anndroid system locale, zh-TW = Traditional Chinese, zh-CN = Simplified Chinese
lang=zh-CN

update_font_reg=0
update_font_bold=0
remove_old_font=0

# check regular font
if [ ! -f "/system/fonts/Miui-Regular.ttf" ]; then
    update_font_reg=1
fi

# check bold font
if [ ! -f "/system/fonts/Miui-Bold.ttf" ]; then
    update_font_bold=1
fi

# check droidsans font
if ls /system/fonts/DroidSansFallback*.ttf 1> /dev/null 2>&1; then
    remove_old_font=1
fi

if [ $update_font_reg -eq "1" ] || [ $update_font_bold -eq "1" ] || [ $remove_old_font -eq "1" ]; then
    # sleep 3 secs in case, make sure the /system is remountable
    sleep 3
    mount -o remount,rw /system
    if [ $update_font_reg -eq "1" ] || [ $update_font_bold -eq "1" ]; then
        # download regular font
        if [ $update_font_reg -eq "1" ]; then
            yes | cp -rf /data/openpilot/fonts/Miui-Regular.ttf /system/fonts/Miui-Regular.ttf
        fi
        # download bold font
        if [ $update_font_bold -eq "1" ]; then
            yes | cp -rf /data/openpilot/fonts/Miui-Bold.ttf /system/fonts/Miui-Bold.ttf
        fi
        # dont new font mapping
        yes | cp -rf /data/openpilot/fonts/fonts.xml /system/etc/fonts.xml
        chmod 644 /system/etc/fonts.xml
        chmod 644 /system/fonts/Miui-*
    fi
    # remove driodsans font
    if [ $remove_old_font -eq "1" ]; then
        rm -fr /system/fonts/DroidSansFallback*.ttf
    fi
    mount -o remount,r /system
    # change system locale
fi

setprop persist.sys.locale $lang
setprop persist.sys.local $lang
