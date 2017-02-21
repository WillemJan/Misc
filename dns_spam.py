#!/usr/bin/env python

seen = []
with open('spam_hosts') as fh:
    for line in fh.read().split():
        if not line in seen:
            if not line == 'localhost':
                print('zone "%s" { type master; notify no; file "/etc/bind/null.zone.file"; };' % line)
            seen.append(line)
