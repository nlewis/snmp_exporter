import easysnmp
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from SocketServer import ForkingMixIn

import yaml
from prometheus_client import CONTENT_TYPE_LATEST

from collector import collect_snmp


class ForkingHTTPServer(ForkingMixIn, HTTPServer):
  pass


class SnmpExporterHandler(BaseHTTPRequestHandler):
  def __init__(self, config_path, *args, **kwargs):
    self._config_path = config_path
    BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

  def do_GET(self):
    url = urlparse.urlparse(self.path)
    if url.path == '/metrics':
      params = urlparse.parse_qs(url.query)
      if 'address' not in params:
        self.send_response(400)
        self.end_headers()
        self.wfile.write("Missing 'address' from parameters")
        return

      port = 161
      address = params['address'][0]
      if 'port' in params:
        port = params['port'][0]
      elif ':' in address:
        address, port = address.split(':')

      with open(self._config_path) as f:
        config = yaml.safe_load(f)
      try:
        output = collect_snmp(config, address, port)
      except (ValueError, easysnmp.EasySNMPError) as e:
        self.send_response(502)
        self.end_headers()
        self.wfile.write('Error collecting metrics from remote host: %s' % (e))
        return

      self.send_response(200)
      self.send_header('Content-Type', CONTENT_TYPE_LATEST)
      self.end_headers()
      self.wfile.write(output)
    elif url.path == '/':
      self.send_response(200)
      self.end_headers()
      self.wfile.write("""<html>
      <head><title>SNMP Exporter</title></head>
      <body>
      <h1>SNMP Exporter</h1>
      <p>Usage:<br>
      <code>/metrics?address=1.2.3.4</code><br>
      <code>/metrics?address=1.2.3.4&port=123</code><br>
      <code>/metrics?address=1.2.3.4:123</code></p>
      </body>
      </html>""")
    else:
      self.send_response(404)
      self.end_headers()


def start_http_server(config_path, port):
  handler = lambda *args, **kwargs: SnmpExporterHandler(config_path, *args, **kwargs)
  server = ForkingHTTPServer(('', port), handler)
  server.serve_forever()
