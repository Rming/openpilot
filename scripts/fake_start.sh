#!/usr/bin/env sh

if [ $# != 1 ] ; then
    echo "说明: 模拟启动 openpilot 进程，烤机模式。"
    echo "用法: $0 <flag>"
    echo "  - 开启: $0 1"
    echo "  - 关闭: $0 0"
    exit 1;
fi

d=$(dirname "$0")
flag="$1"

if [ "$flag" = "1" ];then
    sed -i 's/if msg.thermal.started:/if True:#msg.thermal.started/g' "${d}/../selfdrive/manager.py"
else
    sed -i 's/if True:#msg.thermal.started/if msg.thermal.started:/g' "${d}/../selfdrive/manager.py"
fi

