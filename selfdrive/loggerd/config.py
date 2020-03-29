import os
import time
import datetime

if os.environ.get('LOGGERD_ROOT', False):
  ROOT = os.environ['LOGGERD_ROOT']
  print("Custom loggerd root: ", ROOT)
else:
  ROOT = '/data/media/0/realdata/'

if os.environ.get('DASHCAM_ROOT', False):
  DASHCAM_ROOT = os.environ['DASHCAM_ROOT']
  print("Custom dashcam root: ", DASHCAM_ROOT)
else:
  DASHCAM_ROOT = '/sdcard/dashcam/'


SEGMENT_LENGTH = 60


def get_available_percent(default=None):
    try:
      statvfs = os.statvfs(ROOT)
      available_percent = 100.0 * statvfs.f_bavail / statvfs.f_blocks
    except OSError:
      available_percent = default

    return available_percent

def get_dirs_xdays_ago(root, xdays=3):
    today_list = time.strftime("%Y-%m-%d", time.localtime(time.time())).split("-")
    today = datetime.datetime(int(today_list[0]), int(today_list[1]), int(today_list[2]))
    dirs = os.listdir(root)
    for f in dirs:
        path = os.path.join(root, f)
        ctime = time.strftime("%Y-%m-%d", time.localtime((os.stat(path)).st_ctime))
        ctlist = ctime.split("-")
        ct_day = datetime.datetime(int(ctlist[0]), int(ctlist[1]), int(ctlist[2]))
        days_diff = (today - ct_day).days
        if days_diff > xdays:
            yield path


def get_available_bytes(default=None):
    try:
      statvfs = os.statvfs(ROOT)
      available_bytes = statvfs.f_bavail * statvfs.f_frsize
    except OSError:
      available_bytes = default

    return available_bytes
