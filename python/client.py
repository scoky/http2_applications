import nghttp2, ssl, logging

logging.basicConfig(
  format = "%(levelname) -10s %(asctime)s %(module)s:%(lineno) -7s %(message)s",
  level = logging.DEBUG
)

class Handler(nghttp2.BaseResponseHandler):
  def on_headers(self):
    print('Headers')
    for k,v in self.headers:
       print(k.decode('utf-8')+'\t:\t'+v.decode('utf-8'))

  def on_data(self, data):
    print(data.decode('utf-8'))

  def on_response_done(self):
    print('Response done')
    print(self.stream_id)

  def on_push_promise(self, push_promise):
    print('Push received')
    nhandler = Handler()
    self.accept_push(push_promise, nhandler)
    for k,v in nhandler.headers:
       print(k.decode('utf-8')+'\t:\t'+v.decode('utf-8'))

context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

client = nghttp2.HTTP2Client(('localhost', 8443), ssl=context)
client.send_request(method='GET', url='/', headers=[], handler=Handler())
client.run_forever()
