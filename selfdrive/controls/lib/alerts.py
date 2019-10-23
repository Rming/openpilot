from cereal import car, log

# Priority
class Priority:
  LOWEST = 0
  LOW_LOWEST = 1
  LOW = 2
  MID = 3
  HIGH = 4
  HIGHEST = 5

AlertSize = log.ControlsState.AlertSize
AlertStatus = log.ControlsState.AlertStatus
AudibleAlert = car.CarControl.HUDControl.AudibleAlert
VisualAlert = car.CarControl.HUDControl.VisualAlert

class Alert():
  def __init__(self,
               alert_type,
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

    self.alert_type = alert_type
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


ALERTS = [
  # Miscellaneous alerts
  Alert(
      "enable",
      "",
      "",
      AlertStatus.normal, AlertSize.none,
      Priority.MID, VisualAlert.none, AudibleAlert.chimeEngage, .2, 0., 0.),

  Alert(
      "disable",
      "",
      "",
      AlertStatus.normal, AlertSize.none,
      Priority.MID, VisualAlert.none, AudibleAlert.chimeDisengage, .2, 0., 0.),

  Alert(
      "fcw",
      "刹车!",
      "有碰撞的风险",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGHEST, VisualAlert.fcw, AudibleAlert.chimeWarningRepeat, 1., 2., 2.),

  Alert(
      "steerSaturated",
      "接管控制",
      "弯道超过方向盘转向限制",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.steerRequired, AudibleAlert.chimePrompt, 1., 2., 3.),

  Alert(
      "steerTempUnavailable",
      "接管控制",
      "转向控制暂时失效",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.steerRequired, AudibleAlert.chimeWarning1, .4, 2., 3.),

  Alert(
      "steerTempUnavailableMute",
      "接管控制",
      "转向控制暂时失效",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.none, .2, .2, .2),

  Alert(
      "preDriverDistracted",
      "注意路况: 驾驶分心",
      "",
      AlertStatus.normal, AlertSize.small,
      Priority.LOW, VisualAlert.steerRequired, AudibleAlert.none, .0, .1, .1, alert_rate=0.75),

  Alert(
      "promptDriverDistracted",
      "注意路况",
      "驾驶分心",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarning2, .1, .1, .1),

  Alert(
      "driverDistracted",
      "立即解除",
      "驾驶分心",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGH, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, .1, .1),

  Alert(
      "preDriverUnresponsive",
      "请触碰方向盘：无驾驶监控",
      "",
      AlertStatus.normal, AlertSize.small,
      Priority.LOW, VisualAlert.steerRequired, AudibleAlert.none, .0, .1, .1, alert_rate=0.75),

  Alert(
      "promptDriverUnresponsive",
      "触碰方向盘",
      "驾驶没有反应",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarning2, .1, .1, .1),

  Alert(
      "driverUnresponsive",
      "立即解除",
      "驾驶没有反应",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGH, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, .1, .1),

  Alert(
      "driverMonitorOff",
      "驾驶监控暂时停用",
      "监控准确率：低",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.none, .4, 0., 4.),

  Alert(
      "driverMonitorOn",
      "驾驶监控已启用",
      "监控准确率：高",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.none, .4, 0., 4.),

  Alert(
      "geofence",
      "DISENGAGEMENT REQUIRED",
      "不在地理围栏区域之内",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.HIGH, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, .1, .1),

  Alert(
      "startup",
      "随时准备好接管",
      "请您将手放在方向盘上并持续注意路况",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW_LOWEST, VisualAlert.none, AudibleAlert.none, 0., 0., 15.),

  Alert(
      "startupNoControl",
      "行车记录模式",
      "请您将手放在方向盘上并持续注意路况",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW_LOWEST, VisualAlert.none, AudibleAlert.none, 0., 0., 15.),

  Alert(
      "startupNoCar",
      "行车记录模式 (尚未支援车种)",
      "请您将手放在方向盘上并持续注意路况",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW_LOWEST, VisualAlert.none, AudibleAlert.none, 0., 0., 15.),

  Alert(
      "ethicalDilemma",
      "接管控制 IMMEDIATELY",
      "Ethical Dilemma Detected",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGHEST, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, 1., 3., 3.),

  Alert(
      "steerTempUnavailableNoEntry",
      "无法使用 openpilot",
      "转向控制暂时失效",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 0., 3.),

  Alert(
      "manualRestart",
      "接管控制",
      "请自行恢复驾驶",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.none, 0., 0., .2),

  Alert(
      "resumeRequired",
      "已停止",
      "请按 RES 继续",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.none, 0., 0., .2),

  Alert(
      "belowSteerSpeed",
      "接管控制",
      "转向控制暂时失效，车速低于  ",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.none, 0., 0.4, .3),

  Alert(
      "debugAlert",
      "DEBUG ALERT",
      "",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.none, .1, .1, .1),

  # Non-entry only alerts
  Alert(
      "wrongCarModeNoEntry",
      "无法使用 openpilot",
      "主开关关闭",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 0., 3.),

  Alert(
      "dataNeededNoEntry",
      "无法使用 openpilot",
      "需要更多的数据来协助校准，请将行车记录上传后再试",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 0., 3.),

  Alert(
      "outOfSpaceNoEntry",
      "无法使用 openpilot",
      "储存空间不足",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 0., 3.),

  Alert(
      "pedalPressedNoEntry",
      "无法使用 openpilot",
      "Pedal Pressed During Attempt",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, "brakePressed", AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "speedTooLowNoEntry",
      "无法使用 openpilot",
      "车速过慢",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "brakeHoldNoEntry",
      "无法使用 openpilot",
      "驻车煞车已启用",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "parkBrakeNoEntry",
      "无法使用 openpilot",
      "电子驻车已启动",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "lowSpeedLockoutNoEntry",
      "无法使用 openpilot",
      "巡航系统错误：请重新发动车子",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "lowBatteryNoEntry",
      "无法使用 openpilot",
      "电池电量过低",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "sensorDataInvalidNoEntry",
      "无法使用 openpilot",
      "没有收到任何来自 EON 传感器的资料",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "soundsUnavailableNoEntry",
      "无法使用 openpilot",
      "找不到音效装置",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "tooDistractedNoEntry",
      "无法使用 openpilot",
      "驾驶分心次数过高",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  # Cancellation alerts causing soft disabling
  Alert(
      "overheat",
      "接管控制 IMMEDIATELY",
      "系统过热",
      AlertStatus.critical, AlertSize.full,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, 2., 2.),

  Alert(
      "wrongGear",
      "接管控制 IMMEDIATELY",
      "车子不在 D 档",
      AlertStatus.critical, AlertSize.full,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, 2., 2.),

  Alert(
      "calibrationInvalid",
      "接管控制 IMMEDIATELY",
      "校准无效：请将 EON 放于新的位置并重新校准",
      AlertStatus.critical, AlertSize.full,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, 2., 2.),

  Alert(
      "calibrationIncomplete",
      "接管控制 IMMEDIATELY",
      "正在校准相机中",
      AlertStatus.critical, AlertSize.full,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, 2., 2.),

  Alert(
      "doorOpen",
      "接管控制 IMMEDIATELY",
      "车门开启",
      AlertStatus.critical, AlertSize.full,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, 2., 2.),

  Alert(
      "seatbeltNotLatched",
      "接管控制 IMMEDIATELY",
      "安全带未繫",
      AlertStatus.critical, AlertSize.full,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, 2., 2.),

  Alert(
      "espDisabled",
      "接管控制 IMMEDIATELY",
      "ESP 关闭",
      AlertStatus.critical, AlertSize.full,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, 2., 2.),

  Alert(
      "lowBattery",
      "接管控制 IMMEDIATELY",
      "电池电量过低",
      AlertStatus.critical, AlertSize.full,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, 2., 2.),

  Alert(
      "commIssue",
      "接管控制 IMMEDIATELY",
      "程序间出现通讯问题",
      AlertStatus.critical, AlertSize.full,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, 2., 2.),

  Alert(
      "radarCanError",
      "接管控制 IMMEDIATELY",
      "雷达讯号错误：请重新发动车子",
      AlertStatus.critical, AlertSize.full,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, 2., 2.),

  Alert(
      "radarFault",
      "接管控制 IMMEDIATELY",
      "雷达讯号错误：请重新发动车子",
      AlertStatus.critical, AlertSize.full,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, 2., 2.),

  Alert(
      "posenetInvalid",
      "接管控制 IMMEDIATELY",
      "视觉错误：请检查相机",
      AlertStatus.critical, AlertSize.full,
      Priority.MID, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, .1, 2., 2.),

  # Cancellation alerts causing immediate disabling
  Alert(
      "controlsFailed",
      "接管控制 IMMEDIATELY",
      "控制发生错误",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGHEST, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, 1., 3., 4.),

  Alert(
      "controlsMismatch",
      "接管控制 IMMEDIATELY",
      "控制不匹配",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGHEST, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, 1., 3., 4.),

  Alert(
      "canError",
      "接管控制 IMMEDIATELY",
      "CAN 讯号错误：请检查接线",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGHEST, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, 1., 3., 4.),

  Alert(
      "steerUnavailable",
      "接管控制 IMMEDIATELY",
      "LKAS 错误：请重新发动车子",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGHEST, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, 1., 3., 4.),

  Alert(
      "brakeUnavailable",
      "接管控制 IMMEDIATELY",
      "巡航系统错误：请重新发动车子",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGHEST, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, 1., 3., 4.),

  Alert(
      "gasUnavailable",
      "接管控制 IMMEDIATELY",
      "油门错误：请重新发动车子",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGHEST, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, 1., 3., 4.),

  Alert(
      "reverseGear",
      "接管控制 IMMEDIATELY",
      "切换至倒车档",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGHEST, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, 1., 3., 4.),

  Alert(
      "cruiseDisabled",
      "接管控制 IMMEDIATELY",
      "巡航系统关闭",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGHEST, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, 1., 3., 4.),

  Alert(
      "plannerError",
      "接管控制 IMMEDIATELY",
      "Planner Solution 错误",
      AlertStatus.critical, AlertSize.full,
      Priority.HIGHEST, VisualAlert.steerRequired, AudibleAlert.chimeWarningRepeat, 1., 3., 4.),

  # not loud cancellations (user is in control)
  Alert(
      "noTarget",
      "openpilot 已取消",
      "没有侦测到前车",
      AlertStatus.normal, AlertSize.mid,
      Priority.HIGH, VisualAlert.none, AudibleAlert.chimeDisengage, .4, 2., 3.),

  Alert(
      "speedTooLow",
      "openpilot 已取消",
      "车速过慢",
      AlertStatus.normal, AlertSize.mid,
      Priority.HIGH, VisualAlert.none, AudibleAlert.chimeDisengage, .4, 2., 3.),

  Alert(
      "invalidGiraffeHonda",
      "Giraffe 开关错误",
      "openpilot 模式为 0111，原厂模式为 1011",
      AlertStatus.normal, AlertSize.mid,
      Priority.HIGH, VisualAlert.none, AudibleAlert.chimeDisengage, .4, 2., 3.),

  # Cancellation alerts causing non-entry
  Alert(
      "overheatNoEntry",
      "无法使用 openpilot",
      "系统过热",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "wrongGearNoEntry",
      "无法使用 openpilot",
      "车子不在 D 档",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "calibrationInvalidNoEntry",
      "无法使用 openpilot",
      "校准无效：请将 EON 放于新的位置并重新校准",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "calibrationIncompleteNoEntry",
      "无法使用 openpilot",
      "正在校准相机中",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "doorOpenNoEntry",
      "无法使用 openpilot",
      "车门未关",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "seatbeltNotLatchedNoEntry",
      "无法使用 openpilot",
      "安全带未系",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "espDisabledNoEntry",
      "无法使用 openpilot",
      "ESP 关闭",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "geofenceNoEntry",
      "无法使用 openpilot",
      "不在地理围栏区域之内",
      AlertStatus.normal, AlertSize.mid,
      Priority.MID, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "radarCanErrorNoEntry",
      "无法使用 openpilot",
      "雷达讯号错误：请重新发动车子",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "radarFaultNoEntry",
      "无法使用 openpilot",
      "雷达讯号错误：请重新发动车子",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "posenetInvalidNoEntry",
      "无法使用 openpilot",
      "视觉错误：请检查相机",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "controlsFailedNoEntry",
      "无法使用 openpilot",
      "控制发生错误",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "canErrorNoEntry",
      "无法使用 openpilot",
      "CAN 讯号错误：请检查接线",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "steerUnavailableNoEntry",
      "无法使用 openpilot",
      "LKAS 错误：请重新发动车子",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "brakeUnavailableNoEntry",
      "无法使用 openpilot",
      "巡航系统错误：请重新发动车子",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "gasUnavailableNoEntry",
      "无法使用 openpilot",
      "油门错误：请重新发动车子",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "reverseGearNoEntry",
      "无法使用 openpilot",
      "切换至倒车档",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "cruiseDisabledNoEntry",
      "无法使用 openpilot",
      "巡航系统关闭",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "noTargetNoEntry",
      "无法使用 openpilot",
      "没有侦测到前车",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "plannerErrorNoEntry",
      "无法使用 openpilot",
      "Planner Solution 错误",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeError, .4, 2., 3.),

  Alert(
      "invalidGiraffeHondaNoEntry",
      "无法使用 openpilot",
      "openpilot 模式为 0111，原厂模式为 1011",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeDisengage, .4, 2., 3.),

  Alert(
      "commIssueNoEntry",
      "无法使用 openpilot",
      "程序间出现通讯问题",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeDisengage, .4, 2., 3.),

  Alert(
      "internetConnectivityNeededNoEntry",
      "无法使用 openpilot",
      "需要网路连线",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.chimeDisengage, .4, 2., 3.),

  # permanent alerts
  Alert(
      "steerUnavailablePermanent",
      "LKAS 错误：请重新发动车子",
      "",
      AlertStatus.normal, AlertSize.small,
      Priority.LOW_LOWEST, VisualAlert.none, AudibleAlert.none, 0., 0., .2),

  Alert(
      "brakeUnavailablePermanent",
      "巡航系统错误：请重新发动车子",
      "",
      AlertStatus.normal, AlertSize.small,
      Priority.LOW_LOWEST, VisualAlert.none, AudibleAlert.none, 0., 0., .2),

  Alert(
      "lowSpeedLockoutPermanent",
      "巡航系统错误：请重新发动车子",
      "",
      AlertStatus.normal, AlertSize.small,
      Priority.LOW_LOWEST, VisualAlert.none, AudibleAlert.none, 0., 0., .2),

  Alert(
      "calibrationIncompletePermanent",
      "正在校准相机中: ",
      "车速请高于 ",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOWEST, VisualAlert.none, AudibleAlert.none, 0., 0., .2),

  Alert(
      "invalidGiraffeHondaPermanent",
      "Giraffe 开关错误",
      "openpilot 模式为 0111，原厂模式为 1011",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW_LOWEST, VisualAlert.none, AudibleAlert.none, 0., 0., .2),

  Alert(
      "invalidGiraffeToyotaPermanent",
      "未支援的 Giraffe 设置",
      "请查阅 comma.ai/tg",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW_LOWEST, VisualAlert.none, AudibleAlert.none, 0., 0., .2),

  Alert(
      "internetConnectivityNeededPermanent",
      "需要网路连线",
      "请先检查更新才能启用",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW_LOWEST, VisualAlert.none, AudibleAlert.none, 0., 0., .2),

  Alert(
      "sensorDataInvalidPermanent",
      "没有收到任何来自 EON 传感器的资料",
      "请重启您的 EON",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW_LOWEST, VisualAlert.none, AudibleAlert.none, 0., 0., .2),

  Alert(
      "soundsUnavailablePermanent",
      "找不到音效装置",
      "请重启您的 EON",
      AlertStatus.normal, AlertSize.mid,
      Priority.LOW_LOWEST, VisualAlert.none, AudibleAlert.none, 0., 0., .2),

  Alert(
      "vehicleModelInvalid",
      "车子参数识别失败",
      "",
      AlertStatus.normal, AlertSize.small,
      Priority.LOWEST, VisualAlert.steerRequired, AudibleAlert.none, .0, .0, .1),
]
