# Prometheus Fail2ban Exporter
This exporter uses `fail2ban-client` to get the number of current and total failed connections and banned IPs on a host.

Exposes metrics on :8042
 
## Usage
### Docker
```bash
docker build -t fail2ban-exporter:latest .
# or use pre-built image
docker pull ghcr.io/konstfish/fail2ban-exporter:latest

docker run -d --name fail2ban-exporter \
              -v /var/run/fail2ban/fail2ban.sock:/var/run/fail2ban/fail2ban.sock \
              -v /var/lib/fail2ban:/var/lib/fail2ban \
              -p 8042:8042 \
              ghcr.io/konstfish/fail2ban-exporter:latest
```

### docker-compose
```yaml
version: '3'

services:
  fail2ban-exporter:
    image: ghcr.io/konstfish/fail2ban-exporter:latest
    ports:
      - "8042:8042"
    volumes:
      - /var/run/fail2ban/fail2ban.sock:/var/run/fail2ban/fail2ban.sock
      - /var/lib/fail2ban:/var/lib/fail2ban
```

### Regular
```
usage: fail2ban-exporter.py [-h] [-j JAIL] [-f FILE]

Export fail2ban-client metrics for Prometheus Node Exporter.

optional arguments:
  -h, --help            show this help message and exit
  -j JAIL, --jail JAIL  Jail name to be exported (all jails if omitted).
  -p PORT, --port PORT  Port for the HTTP server.
```

## Example Output
```
# HELP fail2ban_failed_current Number of currently failed connections.
# TYPE fail2ban_failed_current gauge
fail2ban_failed_current{jail="asterisk"} 4.0
fail2ban_failed_current{jail="postfix-sasl"} 1.0
fail2ban_failed_current{jail="proftpd"} 0.0
fail2ban_failed_current{jail="sshd"} 1.0
# HELP fail2ban_failed_total Total number of failed connections.
# TYPE fail2ban_failed_total gauge
fail2ban_failed_total{jail="asterisk"} 699.0
fail2ban_failed_total{jail="postfix-sasl"} 6.0
fail2ban_failed_total{jail="proftpd"} 0.0
fail2ban_failed_total{jail="sshd"} 925.0
# HELP fail2ban_banned_current Number of currently banned IP addresses.
# TYPE fail2ban_banned_current gauge
fail2ban_banned_current{jail="asterisk"} 0.0
fail2ban_banned_current{jail="postfix-sasl"} 0.0
fail2ban_banned_current{jail="proftpd"} 0.0
fail2ban_banned_current{jail="sshd"} 0.0
# HELP fail2ban_banned_total Total number of banned IP addresses.
# TYPE fail2ban_banned_total gauge
fail2ban_banned_total{jail="asterisk"} 31.0
fail2ban_banned_total{jail="postfix-sasl"} 1.0
fail2ban_banned_total{jail="proftpd"} 0.0
fail2ban_banned_total{jail="sshd"} 4.0
```

## Credits
* Hannes Lindner, for writing the [original version](https://github.com/HannesLindner/fail2ban-export)
* Jan Grewe, for writing the [original fork](https://github.com/jangrewe/prometheus-fail2ban-exporter)
