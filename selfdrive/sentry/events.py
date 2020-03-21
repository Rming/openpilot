import selfdrive.crash as crash

def event_openpilot_running():
  crash.capture_info("openpilot_running")

def event_fingerprinted(candidate):
  crash.capture_info("fingerprinted %s" % candidate)

def event_fingerprinted_error(fingerprints, fw):
  crash.capture_warning("car doesn't match any fingerprints: %s" % fingerprints)
  crash.capture_warning("car doesn't match any fw: %s" % fw)

def event_afa_car_model(fingerprints, fw, model):
  crash.capture_info("afa_car_model fingerprints: %s" % fingerprints)
  crash.capture_info("afa_car_model fw: %s" % fw)
  crash.capture_info("afa_car_model val: %s" % model)
