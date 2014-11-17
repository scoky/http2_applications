import logging
import argparse
import sys
import traceback
import os
import ssl
import nghttp2, spdylay, requests
from urllib.parse import urlparse

class H2Handler(nghttp2.BaseResponseHandler):
  def __init__(self, client, *args, **kwargs):
    super(Handler, self).__init__(*args, **kwargs):
    self.client = client

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
    self.reject_push(push_promise)

class SpdyHandler(spdylay.BaseSPDYStreamHandler):
    def on_header(self, nv):
        sys.stdout.write('Stream#{}\n'.format(self.stream_id))
        for k, v in nv:
            sys.stdout.write('{}: {}\n'.format(k, v))

    def on_data(self, data):
        sys.stdout.write('Stream#{}\n'.format(self.stream_id))
        sys.stdout.buffer.write(data)

    def on_close(self, status_code):
        sys.stdout.write('Stream#{} closed\n'.format(self.stream_id))

def fetch_h2(url):
  context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)

  location = urlparse(url).netloc
  try:
    hostname,port = location.split(':', 1)
  except:
    hostname = location
    port = 443

  client = nghttp2.HTTP2Client((hostname, port), ssl=context)
  client.send_request(method='GET', url=url, headers=[], handler=H2Handler(client))
  client.run_forever()

def fetch_spdy(url):
  spdylay.urlfetch(url, SpdyHandler)

def fetch_h1(url):
  requests.get(url)

def main():
  if (args.protocol == 'h2'):
    fetch_h2(args.url)
  elif (args.protocol == 'http1.1'):
    fetch_h1(args.url)
  elif (args.protocol == 'spdy'):
    fetch_spdy(args.url)

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Load a page using either HTTP/1.1, SPDY, or HTTP2')
   parser.add_argument('url', help='url to root object')
   parser.add_argument('-p', '--protocol', choices=['http1.1', 'spdy', 'h2'], default='h2', help='protocol to use')
   args = parser.parse_args()

    # set up logging
    level = logging.INFO
    logging.basicConfig(
        format = "%(levelname) -10s %(asctime)s %(module)s:%(lineno) -7s %(message)s",
        level = level
    )

    main()
