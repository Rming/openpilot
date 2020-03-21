import threading
import requests
import time
import selfdrive.sentry.events as events
from common.travis import is_in_travis

def dispatch(event, args=()):
  if not is_in_travis:
    def dispatcher(event, event_args):
      while True:
        if has_internet():
          getattr(events, "event_%s" % event)(*event_args)
          break
        time.sleep(3)
    x = threading.Thread(target=dispatcher, args=(event, args))
    x.start()

def has_internet(timeout=5):
    try:
        requests.head("https://sentry.io", timeout=timeout)
        return True
    except:
        return False

