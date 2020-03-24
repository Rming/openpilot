#!/usr/bin/env python3
from selfdrive.loggerd.uploaders.qiniu import Auth, put_file, etag

class FakeResponse():
  def __init__(self, code):
    self.status_code = code

class QiniuUploader():
  def __init__(self, ak, sk):
    self.name = "qiniu"
    self.bucket = "openpilot"
    self.handler = Auth(ak, sk)

  def put(self, key, fn):
    token = self.handler.upload_token(self.bucket, key, 3600)
    ret, info = put_file(token, key, fn)
    if ret['hash'] == etag(fn):
      return FakeResponse(200)
    else:
      return FakeResponse(500)
