import nghttp2, ssl

class Handler(nghttp2.BaseResponseHandler):
  def on_headers(self):
    for k,v in self.headers:
       print(k.decode('utf-8')+'\t:\t'+v.decode('utf-8'))

  def on_data(self, data):
#    print(data.decode('utf-8'))
    pass

  def on_push_promise(self, headers):
    return Handler()

context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
#context.check_hostname = False
#context.verify_mode = ssl.CERT_NONE

client = nghttp2.HTTP2Client(('google.com', 443), ssl=context)
client.send_request(method='GET', url='/', headers=[], handler=Handler())
client.run_forever()
