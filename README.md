<a href="#fork-preview"><img width="500" align="center" id="fork-preview" src="https://doc.sdut.me/files/afa_op.jpg"></a>

Fork of openpilot
=======================
本 fork 是基于官方 openpilot 代码修改而来，新增、修改过程中会遵循以下原则：

- 尽可能保持版本稳定
- 尽可能不使用选项开关
- 尽可能保留官方功能不被修改

Branches
=======================

| 分支 | 说明 |推荐|
| :---: | --- | --- |
| `afa-{版本号}`  | 官方版本 + 简体中文界面 + 本田车型优化|推荐 CRV、Accord、Inspire 等车型使用|
| `afa-latest`  | 总是跟随最新版本的 `afa-{版本号}` 更新 |推荐需要版本升级推送的车主，<br>可以在启动时跳过升级，默认 10 秒跳过|


| 分支 | 说明 |推荐|
| :---: | --- | --- |
| `{版本号}-zhs`  | 官方版本 + 简体中文界面 |推荐喜欢简洁官方版本的车主使用|
| `latest-zhs`  | 总是跟随最新版本的 `{版本号}-zhs` 更新 |推荐需要版本升级推送的车主，<br>需要定期联网检查更新，强制版本升级|


Features
=======================
 * 简体中文界面
 * 新增部分已知车型指纹
 * 移除请连网更新的提示
 * 移除系统时间必须大于 2019 年的限制
 * 首次使用会自动刷写 panda 固件
 * 支持本田车型踩油门时不退出系统
 * 支持丰田车型踩油门时不退出系统
 * 支持本田、丰田车型使用运动档、手动档
 * 支持本田车型使用换档拨片
 * 本田 Bosch 车型全部警告声都从原车提示
 * 车道偏离警告只在原车仪表盘提示
 * 转向超出扭矩限制警告只在原车仪表盘提示
 * EON 电池充电控制在 60% ~ 80%
 * EON 界面使用渐变色显示行驶轨迹线
 * EON 界面显示刹车状态、转向灯状态
 * EON 界面显示前车距离显示和车距过近图标提示
 * 优化本田原厂 ACC SnG 恢复功能
 * 自动删除三天以前的驾驶记录（车辆启动时）
 * 如果剩余空间小于 8G，开始删旧的驾驶记录日志
 * 如果剩余空间小于 5G，开始删旧的行车录像
 * 可配置的 EON 警告提示音量，默认完全静音
 * 可配置的 EON 摄像头配置偏移，默认左偏 6 厘米
 * 可配置的 EON 基础屏幕亮度，在此基础上支持光感
 * 可配置的 EON 低电量关机电量比例
 * 车辆启动后可以在 EON 界面开启/关闭行车录像
 * 检测不到人脸时忽略驾驶员监控，支持直接遮挡摄像头
 * 可以在 EON 界面选择车型，有效减少未识别车型报错
 * 可配置无电池模式，禁用充电控制、忽略电池温度检测
 * 打开设置页面可查看 IP 地址
 * 使用 sentry 上报错误异常，记录调试信息

Usage
=======================
安装、使用过程中需要的软件、资料，或者疑问请参考：

- [Openpilot 中文 Wiki](https://doc.sdut.me/)
- [Openpilot 软件下载站](https://d.sdut.me/)
- [Openpilot 国内镜像](https://doc.sdut.me/mirror.html)
- [[Bilibili] Openpilot-China](https://space.bilibili.com/9843793)
- [[YouTube] Openpilot China](https://www.youtube.com/channel/UC79hb9uL4o3YsqFLnFZVzbA)


Donation
=======================

感谢所有对项目进行捐助支持的朋友们～

捐助款项将全部用于 openpilot 相关的 服务器费用、运营支持。

| Wechat |
| :------: |
| <a href="#donation"><img width="150" src="https://doc.sdut.me/files/zan.jpg"> </a>|

捐助名单（按时间顺序）：


| 捐助日期 | 捐助者 | 捐助金额 |友情链接|
| --- | --- | --- | --- |
| 2020-05-13 | Allemanda🍀 | ￥1 |
| 2020-04-11 | 追过梦想又怎样 | ￥1 |
| 2020-03-24 | 陈逸帅 | ￥200 |
| 2020-03-05 | 笨木匠 | ￥199.99 |
| 2020-03-02 | PahPahPah | ￥66.66 |
| 2020-01-21 | 李鑫 | ￥66 |
| 2020-01-20 | 王平 | ￥99.99 |
| 2020-01-20 | 佛佛 | ￥66 |
| 2020-01-20 | G斌 | ￥106 |
| 2020-01-20 | 小石头 | ￥106 |
| 2020-01-20 | KT | ￥1 |
| 2020-01-20 | cnlinux | ￥66 |
| 2020-01-19 | 买买熊 | 乐视3 pro 1个<br>harness 1个<br>black panda 1个|
| 2020-01-18 | Liu Sitong | ￥66.66 |
| 2020-01-04 | 小伍 | ￥16 |
| 2020-01-04 | TaTa | ￥16 |
| 2020-01-04 | x+ | ￥6 |
| 2020-01-04 | 黑框 | ￥106 |
| 2019-12-17 | 柯达 | ￥200 |
| 2019-11-28 | 不曾靠岸的船 | ￥50 |
| 2019-08-27 | 悬镜 | ￥100 |


Acknowledgments
=======================
* [commaai/openpilot](https://github.com/commaai/openpilot)
* [kegman/openpilot](https://github.com/kegman/openpilot)
* [arne182/openpilot](https://github.com/arne182/openpilot)
* [Gernby/openpilot](https://github.com/gernby/openpilot)
* [dragonpilot-community/dragonpilot](https://github.com/dragonpilot-community/dragonpilot)

#### 站在巨人的肩膀上

开发过程中，大部分功能参考了上述分支代码的功能实现，感谢开源。

Licensing
=======================

openpilot is released under the MIT license. Some parts of the software are released under other licenses as specified.

Any user of this software shall indemnify and hold harmless comma.ai, Inc. and its directors, officers, employees, agents, stockholders, affiliates, subcontractors and customers from and against all allegations, claims, actions, suits, demands, damages, liabilities, obligations, losses, settlements, judgments, costs and expenses (including without limitation attorneys’ fees and costs) which arise out of, relate to or result from any use of this software by user.

**THIS IS ALPHA QUALITY SOFTWARE FOR RESEARCH PURPOSES ONLY. THIS IS NOT A PRODUCT.
YOU ARE RESPONSIBLE FOR COMPLYING WITH LOCAL LAWS AND REGULATIONS.
NO WARRANTY EXPRESSED OR IMPLIED.**

---

<img src="https://d1qb2nb5cznatu.cloudfront.net/startups/i/1061157-bc7e9bf3b246ece7322e6ffe653f6af8-medium_jpg.jpg?buster=1458363130" width="75"></img> <img src="https://cdn-images-1.medium.com/max/1600/1*C87EjxGeMPrkTuVRVWVg4w.png" width="225"></img>
