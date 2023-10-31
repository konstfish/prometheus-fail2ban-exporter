#!/usr/bin/env python3
import re, subprocess, argparse
from prometheus_client import CollectorRegistry, Gauge, make_wsgi_app
from prometheus_client.exposition import make_server

## Modifying may break it!
## ^ hes right
parseKeys = {
    'Currently failed:': ('fail2ban_failed_current', 'Number of currently failed connections.'),
    'Total failed:':('fail2ban_failed_total', 'Total number of failed connections.'),
    'Currently banned:':('fail2ban_banned_current', 'Number of currently banned IP addresses.'),
    'Total banned:':('fail2ban_banned_total', 'Total number of banned IP addresses.')
}

## Commandline args
parser = argparse.ArgumentParser(description="Export fail2ban-client metrics for Prometheus.")
parser.add_argument('-j', '--jail', help="Jail name to be exported (all jails if omitted).")
parser.add_argument('-p', '--port', type=int, default=8042, help="Port for the HTTP server.")
args = parser.parse_args()

pattern = re.compile(r'('+ '|'.join(parseKeys.keys()) + ')\s*(\d*)')
metrics = {}

for k in parseKeys.keys():
    metrics[k] = {}

if args.jail:
    jails = [args.jail]
else:
    process = subprocess.Popen(['fail2ban-client', 'status'], stdout=subprocess.PIPE)
    response = process.communicate()[0].decode('utf-8')
    match = re.search('.+Jail list:\s+(.+)$', response)
    jails = match.group(1).split(", ")

registry = CollectorRegistry()

for metric_key, metric_val in parseKeys.items():
    metrics[metric_key] = Gauge(metric_val[0], metric_val[1], ['jail'], registry=registry)

def update_metrics():
    for jail in jails:
        process = subprocess.Popen(['fail2ban-client', 'status', jail], stdout=subprocess.PIPE)
        response = process.communicate()[0].decode('utf-8')
        match = re.findall(pattern, response)
        for m in match:
            metrics[m[0]].labels(jail).set(float(m[1]))

class CustomMetricsApp(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, environ, start_response):
        update_metrics()
        return self._app(environ, start_response)

wrapped_app = CustomMetricsApp(make_wsgi_app(registry))

httpd = make_server('', args.port, wrapped_app)
httpd.serve_forever()