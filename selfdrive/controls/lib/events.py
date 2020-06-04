# This Python file uses the following encoding: utf-8
# -*- coding: utf-8 -*-
from cereal import log, car

from selfdrive.config import Conversions as CV

from selfdrive.locationd.calibration_helpers import Filter

AlertSize = log.ControlsState.AlertSize
AlertStatus = log.ControlsState.AlertStatus
VisualAlert = car.CarControl.HUDControl.VisualAlert
AudibleAlert = car.CarControl.HUDControl.AudibleAlert
EventName = car.CarEvent.EventName

# Alert priorities
class Priority:
  LOWEST = 0
  LOWER = 1
  LOW = 2
  MID = 3
  HIGH = 4
  HIGHEST = 5

# Event types
class ET:
  ENABLE = 'enable'
  PRE_ENABLE = 'preEnable'
  NO_ENTRY = 'noEntry'
  WARNING = 'warning'
  USER_DISABLE = 'userDisable'
  SOFT_DISABLE = 'softDisable'
  IMMEDIATE_DISABLE = 'immediateDisable'
  PERMANENT = 'permanent'

# get event name from enum
EVENT_NAME = {v: k for k, v in EventName.schema.enumerants.items()}

class Events:
  def __init__(self):
    self.events = []
    self.static_events = []

  @property
  def names(self):
    return self.events

  def __len__(self):
    return len(self.events)

  def add(self, event_name, static=False):
    if static:
      self.static_events.append(event_name)
    self.events.append(event_name)

  def clear(self):
    self.events = self.static_events.copy()

  def any(self, event_type):
    for e in self.events:
      if event_type in EVENTS.get(e, {}).keys():
        return True
    return False

  def create_alerts(self, event_types, callback_args=[]):
    ret = []
    for e in self.events:
      types = EVENTS[e].keys()
      for et in event_types:
        if et in types:
          alert = EVENTS[e][et]
          if not isinstance(alert, Alert):
            alert = alert(*callback_args)
          alert.alert_type = EVENT_NAME[e]
          ret.append(alert)
    return ret

  def add_from_msg(self, events):
    for e in events:
      self.events.append(e.name.raw)

  def to_msg(self):
    ret = []
    for event_name in self.events:
      event = car.CarEvent.new_message()
      event.name = event_name
      for event_type in EVENTS.get(event_name, {}).keys():
        setattr(event, event_type , True)
      ret.append(event)
    return ret

class Alert:
  def __init__(self,
               alert_text_1,
               alert_text_2,
               alert_status,
               alert_size,
               alert_priority,
               visual_alert,
               audible_alert,
               duration_sound,
               duration_hud_alert,
               duration_text,
               alert_rate=0.):

    self.alert_type = ""
    self.alert_text_1 = alert_text_1
    self.alert_text_2 = alert_text_2
    self.alert_status = alert_status
    self.alert_size = alert_size
    self.alert_priority = alert_priority
    self.visual_alert = visual_alert
    self.audible_alert = audible_alert

    self.duration_sound = duration_sound
    self.duration_hud_alert = duration_hud_alert
    self.duration_text = duration_text

    self.start_time = 0.
    self.alert_rate = alert_rate

    # typecheck that enums are valid on startup
    tst = car.CarControl.new_message()
    tst.hudControl.visualAlert = self.visual_alert

  def __str__(self):
    return self.alert_text_1 + "/" + self.alert_text_2 + " " + str(self.alert_priority) + "  " + str(
      self.visual_alert) + " " + str(self.audible_alert)

  def __gt__(self, alert2):
    return self.alert_priority > alert2.alert_priority

class NoEntryAlert(Alert):
  def __init__(self, alert_text_2, audible_alert=AudibleAlert.chimeError,
               visual_alert=VisualAlert.none, duration_hud_alert=2.):
    super().__init__("系统不可用", alert_text_2, AlertStatus.normal,
                     AlertSize.mid, Priority.LOW, visual_alert,
                     audible_alert, .4, duration_hud_alert, 3.)


class SoftDisableAlert(Alert):
  def __init__(self, alert_text_2):
    super().__init__("立即接管", alert_text_2,
                     AlertStatus.critical, AlertSize.full,
                     Priority.MID, VisualAlert.steerRequired,
                     AudibleAlert.chimeWarningRepeat, .1, 2., 2.),


class ImmediateDisableAlert(Alert):
  def __init__(self, alert_text_2, alert_text_1="立即接管"):
    super().__init__(alert_text_1, alert_text_2,
                     AlertStatus.critical, AlertSize.full,
                     Priority.HIGHEST, VisualAlert.steerRequired,
                     AudibleAlert.chimeWarningRepeat, 2.2, 3., 4.),

class EngagementAlert(Alert):
  def __init__(self, audible_alert=True):
    super().__init__("", "",
                     AlertStatus.normal, AlertSize.none,
                     Priority.MID, VisualAlert.none,
                     audible_alert, .2, 0., 0.),

def below_steer_speed_alert(CP, sm, metric):
  speed = CP.minSteerSpeed * (CV.MS_TO_KPH if metric else CV.MS_TO_MPH)
  unit = "km/h" if metric else "mph"
  return Alert(
    "请求接管",
    "自动转向暂不可用，车速低于 %d %s" % (speed, unit),
    AlertStatus.userPrompt, AlertSize.mid,
    Priority.MID, VisualAlert.steerRequired, AudibleAlert.none, 0., 0.4, .3)

def calibration_incomplete_alert(CP, sm, metric):
  speed = int(Filter.MIN_SPEED * (CV.MS_TO_KPH if metric else CV.MS_TO_MPH))
  unit = "km/h" if metric else "mph"
  return Alert(
    "正在校准摄像头: %d%%" % sm['liveCalibration'].calPerc,
    "车速请高于 %d %s" % (speed, unit),
    AlertStatus.normal, AlertSize.mid,
    Priority.LOWEST, VisualAlert.none, AudibleAlert.none, 0., 0., .2)

EVENTS = {
  # ********** events with no alerts **********

  EventName.gasPressed: {ET.PRE_ENABLE: None},

  # ********** events only containing alerts displayed in all states **********

  EventName.debugAlert: {
    ET.PERMANENT: Alert(
      "调试警告",
      "",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.none, .1, .1, .1),
  },

  EventName.startup: {
    ET.PERMANENT: Alert(
      "准备好随时接管",
      "请手扶方向盘并时刻注意路况",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., 15.),
  },

  EventName.startupWhitePanda: {
    ET.PERMANENT: Alert(
      "警告: 白熊猫即将停止支持",
      "请升级为 Comma 2 或 黑熊猫",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., 15.),
  },

  EventName.startupMaster: {
    ET.PERMANENT: Alert(
      "警告: 该分支未经测试",
      "请手扶方向盘并时刻注意路况",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., 15.),
  },

  EventName.startupNoControl: {
    ET.PERMANENT: Alert(
      "行车记录模式",
      "请手扶方向盘并时刻注意路况",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., 15.),
  },

  EventName.startupNoCar: {
    ET.PERMANENT: Alert(
      "行车记录模式 (暂不支持的车型)",
      "请手扶方向盘并时刻注意路况",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., 15.),
  },

  EventName.invalidGiraffeToyota: {
    ET.PERMANENT: Alert(
      "Giraffe 配置不可用",
      "请查看 comma.ai/tg",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
  },

  EventName.whitePandaUnsupported: {
    ET.PERMANENT: Alert(
      "白熊猫已停止支持",
      "请升级为 Comma 2 或 黑熊猫",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
    ET.NO_ENTRY: NoEntryAlert("白熊猫已停止支持"),
  },

  EventName.invalidLkasSetting: {
    ET.PERMANENT: Alert(
      "原车 LKAS 已启用",
      "关闭原车 LKAS 后启动",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
  },

  EventName.communityFeatureDisallowed: {
    # LOW priority to overcome Cruise Error
    ET.PERMANENT: Alert(
      "",
      "检测到社区功能",
      "请在开发者设置中启用社区功能",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
  },

  EventName.carUnrecognized: {
    ET.PERMANENT: Alert(
      "行车记录模式",
      "未识别车型",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
  },

  EventName.stockAeb: {
    ET.PERMANENT: Alert(
      "刹车!",
      "原车 AEB: 碰撞预警",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGHEST, VisualAlert.fcw, AudibleAlert.none, 1., 2., 2.),
  },

  EventName.stockFcw: {
    ET.PERMANENT: Alert(
      "刹车!",
      "原车 FCW: 碰撞预警",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGHEST, VisualAlert.fcw, AudibleAlert.none, 1., 2., 2.),
  },

  EventName.fcw: {
    ET.PERMANENT: Alert(
      "刹车!",
      "碰撞预警",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGHEST, VisualAlert.fcw, AudibleAlert.chimeWarningRepeat, 1., 2., 2.),
  },

  EventName.ldw: {
    ET.PERMANENT: Alert(
      "请求接管",
      "车道偏离警告",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.steerRequired, AudibleAlert.chimePrompt, 1., 2., 3.),
  },

  EventName.canErrorPersistent: {
    ET.PERMANENT: Alert(
      "CAN 总线故障：请检查数据线连接",
      "",
      AlertStatus.normal, AlertSize.small,
      Priority.LOW, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
  },

  # ********** events only containing alerts that display while engaged **********

  EventName.vehicleModelInvalid: {
    ET.WARNING: Alert(
      "车型参数获取失败",
      "",
      AlertStatus.normal, AlertSize.small,
      Priority.LOWEST, VisualAlert.steerRequired, AudibleAlert.none, .0, .0, .1),
  },

  EventName.steerTempUnavailableMute: {
    ET.WARNING: Alert(
      "请求接管",
      "自动转向暂时不可用",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.none, .2, .2, .2),
  },

  EventName.preDriverDistracted: {
    ET.WARNING: Alert(
      "注意路况: 注意力不集中",
      "",
      AlertStatus.normal, AlertSize.small,
      Priority.LOW, VisualAlert.steerRequired, AudibleAlert.none, .0, .1, .1, alert_rate=0.75),
  },

  EventName.promptDriverDistracted: {
    ET.WARNING: Alert(
      "注意路况",
      "注意力不集中",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarning2Repeat, .1, .1, .1),
  },

  EventName.driverDistracted: {
    ET.WARNING: Alert(
      "系统退出",
      "注意力不集中",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGH, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, .1, .1),
  },

  EventName.preDriverUnresponsive: {
    ET.WARNING: Alert(
      "请手扶方向盘：没有检测到驾驶员",
      "",
      AlertStatus.normal, AlertSize.small,
      Priority.LOW, VisualAlert.steerRequired, AudibleAlert.none, .0, .1, .1, alert_rate=0.75),
  },

  EventName.promptDriverUnresponsive: {
    ET.WARNING: Alert(
      "请手扶方向盘",
      "驾驶员没有响应",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarning2Repeat, .1, .1, .1),
  },

  EventName.driverUnresponsive: {
    ET.WARNING: Alert(
      "系统退出",
      "驾驶员没有响应",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGH, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, .1, .1),
  },

  EventName.driverMonitorLowAcc: {
    ET.WARNING: Alert(
      "没有检测到驾驶员",
      "驾驶员监控模型输出不明确",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.steerRequired, AudibleAlert.none, .4, 0., 1.),
  },

  EventName.manualRestart: {
    ET.WARNING: Alert(
      "请求接管",
      "请手动恢复行驶",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
  },

  EventName.resumeRequired: {
    ET.WARNING: Alert(
      "已停车",
      "请按 RES 键继续行驶",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
  },

  EventName.belowSteerSpeed: {
    ET.WARNING: below_steer_speed_alert,
  },

  EventName.preLaneChangeLeft: {
    ET.WARNING: Alert(
      "往左打方向盘开始切换车道",
      "请注意其他车辆",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.steerRequired, AudibleAlert.none, .0, .1, .1, alert_rate=0.75),
  },

  EventName.preLaneChangeRight: {
    ET.WARNING: Alert(
      "往右打方向盘开始切换车道",
      "请注意其他车辆",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.steerRequired, AudibleAlert.none, .0, .1, .1, alert_rate=0.75),
  },

  EventName.laneChange: {
    ET.WARNING: Alert(
      "切换车道中",
      "请注意其他车辆",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.steerRequired, AudibleAlert.none, .0, .1, .1),
  },

  EventName.steerSaturated: {
    ET.WARNING: Alert(
      "请求接管",
      "超出方向盘转向限制",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.steerRequired, AudibleAlert.chimePrompt, 1., 2., 3.),
  },

  # ********** events that affect controls state transitions **********

  EventName.pcmEnable: {
    ET.ENABLE: EngagementAlert(AudibleAlert.chimeEngage),
  },

  EventName.buttonEnable: {
    ET.ENABLE: EngagementAlert(AudibleAlert.chimeEngage),
  },

  EventName.pcmDisable: {
    ET.USER_DISABLE: EngagementAlert(AudibleAlert.chimeDisengage),
  },

  EventName.buttonCancel: {
    ET.USER_DISABLE: EngagementAlert(AudibleAlert.chimeDisengage),
  },

  EventName.brakeHold: {
    ET.USER_DISABLE: EngagementAlert(AudibleAlert.chimeDisengage),
    ET.NO_ENTRY: NoEntryAlert("制动保持已启动"),
  },

  EventName.parkBrake: {
    ET.USER_DISABLE: EngagementAlert(AudibleAlert.chimeDisengage),
    ET.NO_ENTRY: NoEntryAlert("停车制动已启动"),
  },

  EventName.pedalPressed: {
    ET.USER_DISABLE: EngagementAlert(AudibleAlert.chimeDisengage),
    ET.NO_ENTRY: NoEntryAlert("刹车踏板已踩下",
                              visual_alert=VisualAlert.brakePressed),
  },

  EventName.wrongCarMode: {
    ET.USER_DISABLE: EngagementAlert(AudibleAlert.chimeDisengage),
    ET.NO_ENTRY: NoEntryAlert("主开关已关闭",
                              duration_hud_alert=0.),
  },

  EventName.steerTempUnavailable: {
    ET.WARNING: Alert(
      "请求接管",
      "自动转向暂时不可用",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.steerRequired, AudibleAlert.chimeWarning1, .4, 2., 3.),
    ET.NO_ENTRY: NoEntryAlert("自动转向暂时不可用",
                              duration_hud_alert=0.),
  },

  EventName.posenetInvalid: {
    ET.WARNING: Alert(
      "请求接管",
      "视觉模型输出不明确",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.steerRequired, AudibleAlert.chimeWarning1, .4, 2., 3.),
    ET.NO_ENTRY: NoEntryAlert("视觉模型输出不明确"),
  },

  EventName.outOfSpace: {
    ET.NO_ENTRY: NoEntryAlert("存储空间不足",
                              duration_hud_alert=0.),
  },

  EventName.belowEngageSpeed: {
    ET.NO_ENTRY: NoEntryAlert("车速过慢"),
  },

  EventName.sensorDataInvalid: {
    ET.PERMANENT: Alert(
      "设备传感器数据缺失",
      "请重启设备",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
    ET.NO_ENTRY: NoEntryAlert("设备传感器数据缺失"),
  },

  EventName.soundsUnavailable: {
    ET.PERMANENT: Alert(
      "找不到音效装置",
      "请重启设备",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
    ET.NO_ENTRY: NoEntryAlert("找不到音效装置"),
  },

  EventName.tooDistracted: {
    ET.NO_ENTRY: NoEntryAlert("注意力高度不集中"),
  },

  EventName.overheat: {
    ET.SOFT_DISABLE: SoftDisableAlert("系统过热"),
    ET.NO_ENTRY: NoEntryAlert("系统过热"),
  },

  EventName.wrongGear: {
    ET.SOFT_DISABLE: SoftDisableAlert("请切换到 D 档"),
    ET.NO_ENTRY: NoEntryAlert("请切换到 D 档"),
  },

  EventName.calibrationInvalid: {
    ET.SOFT_DISABLE: SoftDisableAlert("校准失败：请调整设备的位置后重新校准"),
    ET.NO_ENTRY: NoEntryAlert("校准失败：请调整设备的位置后重新校准"),
  },

  EventName.calibrationIncomplete: {
    ET.SOFT_DISABLE: SoftDisableAlert("正在校准摄像头"),
    ET.PERMANENT: calibration_incomplete_alert,
    ET.NO_ENTRY: NoEntryAlert("正在校准摄像头"),
  },

  EventName.doorOpen: {
    ET.SOFT_DISABLE: SoftDisableAlert("车门未关好"),
    ET.NO_ENTRY: NoEntryAlert("车门未关好"),
  },

  EventName.seatbeltNotLatched: {
    ET.SOFT_DISABLE: SoftDisableAlert("安全带未系好"),
    ET.NO_ENTRY: NoEntryAlert("安全带未系好"),
  },

  EventName.espDisabled: {
    ET.SOFT_DISABLE: SoftDisableAlert("ESP 未打开"),
    ET.NO_ENTRY: NoEntryAlert("ESP 未打开"),
  },

  EventName.lowBattery: {
    ET.SOFT_DISABLE: SoftDisableAlert("电池电量过低"),
    ET.NO_ENTRY: NoEntryAlert("电池电量过低"),
  },

  EventName.commIssue: {
    ET.SOFT_DISABLE: SoftDisableAlert("进程通信异常"),
    ET.NO_ENTRY: NoEntryAlert("进程通信异常",
                              audible_alert=AudibleAlert.chimeDisengage),
  },

  EventName.radarCommIssue: {
    ET.SOFT_DISABLE: SoftDisableAlert("雷达通信异常"),
    ET.NO_ENTRY: NoEntryAlert("雷达通信异常",
                              audible_alert=AudibleAlert.chimeDisengage),
  },

  EventName.radarCanError: {
    ET.SOFT_DISABLE: SoftDisableAlert("雷达总线故障：请重新启动车辆"),
    ET.NO_ENTRY: NoEntryAlert("雷达总线故障：请重新启动车辆"),
  },

  EventName.radarFault: {
    ET.SOFT_DISABLE: SoftDisableAlert("雷达系统故障：请重新启动车辆"),
    ET.NO_ENTRY : NoEntryAlert("雷达系统故障：请重新启动车辆"),
  },

  EventName.lowMemory: {
    ET.SOFT_DISABLE: SoftDisableAlert("剩余内存不足: 请重启设备"),
    ET.PERMANENT: Alert(
      "剩余内存不足",
      "请重启设备",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
    ET.NO_ENTRY : NoEntryAlert("剩余内存不足: 请重启设备",
                               audible_alert=AudibleAlert.chimeDisengage),
  },

  EventName.controlsFailed: {
    ET.IMMEDIATE_DISABLE: ImmediateDisableAlert("车辆控制故障"),
    ET.NO_ENTRY: NoEntryAlert("车辆控制故障"),
  },

  EventName.controlsMismatch: {
    ET.IMMEDIATE_DISABLE: ImmediateDisableAlert("车辆控制不符"),
  },

  EventName.canError: {
    ET.IMMEDIATE_DISABLE: ImmediateDisableAlert("CAN 总线故障：请检查数据线连接"),
    ET.NO_ENTRY: NoEntryAlert("CAN 总线故障：请检查数据线连接"),
  },

  EventName.steerUnavailable: {
    ET.IMMEDIATE_DISABLE: ImmediateDisableAlert("LKAS 故障：请重新启动车辆"),
    ET.PERMANENT: Alert(
      "LKAS 故障：请重新启动车辆后启用",
      "",
      AlertStatus.normal, AlertSize.small,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
    ET.NO_ENTRY: NoEntryAlert("LKAS 故障：请重新启动车辆"),
  },

  EventName.brakeUnavailable: {
    ET.IMMEDIATE_DISABLE: ImmediateDisableAlert("巡航系统故障：请重新启动车辆"),
    ET.PERMANENT: Alert(
      "巡航系统故障：请重新启动车辆后启用",
      "",
      AlertStatus.normal, AlertSize.small,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
    ET.NO_ENTRY: NoEntryAlert("巡航系统故障：请重新启动车辆"),
  },

  EventName.gasUnavailable: {
    ET.IMMEDIATE_DISABLE: ImmediateDisableAlert("油门故障：请重新启动车辆"),
    ET.NO_ENTRY: NoEntryAlert("油门故障：请重新启动车辆"),
  },

  EventName.reverseGear: {
    ET.IMMEDIATE_DISABLE: ImmediateDisableAlert("当前在 R 档"),
    ET.NO_ENTRY: NoEntryAlert("当前在 R 档"),
  },

  EventName.cruiseDisabled: {
    ET.IMMEDIATE_DISABLE: ImmediateDisableAlert("巡航系统未打开"),
  },

  EventName.plannerError: {
    ET.IMMEDIATE_DISABLE: ImmediateDisableAlert("路径规划失败"),
    ET.NO_ENTRY: NoEntryAlert("路径规划失败"),
  },

  EventName.relayMalfunction: {
    ET.IMMEDIATE_DISABLE: ImmediateDisableAlert("Harness 故障"),
    ET.PERMANENT: Alert(
      "Harness 故障",
      "请检查硬件设备",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
    ET.NO_ENTRY: NoEntryAlert("Harness 故障"),
  },

  EventName.noTarget: {
    ET.IMMEDIATE_DISABLE: Alert(
      "系统已退出",
      "没有检测到前车",
      AlertStatus.normal, AlertSize.mid,
      Priority.HIGH, VisualAlert.none, AudibleAlert.chimeDisengage, .4, 2., 3.),
    ET.NO_ENTRY : NoEntryAlert("没有检测到前车"),
  },

  EventName.speedTooLow: {
    ET.IMMEDIATE_DISABLE: Alert(
      "系统已退出",
      "车速过慢",
      AlertStatus.normal, AlertSize.mid,
      Priority.HIGH, VisualAlert.none, AudibleAlert.chimeDisengage, .4, 2., 3.),
  },

  EventName.speedTooHigh: {
    ET.WARNING: Alert(
      "车速过快",
      "请减速后重新启用",
      AlertStatus.normal, AlertSize.mid,
      Priority.HIGH, VisualAlert.steerRequired, AudibleAlert.chimeWarning2Repeat, 2.2, 3., 4.),
    ET.NO_ENTRY: Alert(
      "车速过快",
      "请减速后重新启用",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),
  },

  EventName.internetConnectivityNeeded: {
    ET.PERMANENT: Alert(
      "需要连接到网络",
      "检查更新后才能启用",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
    ET.NO_ENTRY: NoEntryAlert("需要连接到网络",
                              audible_alert=AudibleAlert.chimeDisengage),
  },

  EventName.lowSpeedLockout: {
    ET.PERMANENT: Alert(
      "巡航系统故障：请重新启动车辆",
      "",
      AlertStatus.normal, AlertSize.small,
      Priority.LOWER, VisualAlert.none, AudibleAlert.none, 0., 0., .2),
    ET.NO_ENTRY: NoEntryAlert("巡航系统故障：请重新启动车辆"),
  },

}
