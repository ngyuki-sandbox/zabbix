#!/usr/bin/env python
# coding: utf-8

'''
- when で正規表現とかワイルドカードとかは使えない版
'''

import sys
import re
import binascii
import json
import yaml
import os

def dump(data):
    print json.dumps(data, ensure_ascii=False, indent=2)

def main():
    input = sys.stdin.read()
    addr, values = parseTrap(input)
    config = loadConfig(os.path.splitext(__file__)[0] + '.yml')
    process(config, addr, values)

def parseTrap(input):

    lines = input.split("\n")

    m = re.match("\w+:\s*\[([^]]+)\]", lines[1])
    if m:
        addr = m.group(1)
    else:
        addr = '0.0.0.0'

    values = {}
    quote = False

    for line in lines[2:]:
        if len(line) == 0:
            continue
        if not quote:
            oid, line = line.split(" ", 1)
            if line[0] == '"':
                quote = True
                buf = ""
                line = line.lstrip('"')
            else:
                values[oid] = line

        if quote:
            if line[-1] == '"':
                buf += line.rstrip('"')
                values[oid] = binascii.unhexlify(buf.replace(" ", ""))
                quote = False;
                buf = ""
            else:
                buf += line

    return addr, values

def loadConfig(path):
    config = yaml.load(open(path, "r"))
    return config

def process(config, addr, values):
    for cfg in config:
        shell, environment = processOne(cfg, addr, values)
        if not shell:
            continue
        executeCommand(shell, environment)

def processOne(cfg, addr, values):

    hosts = cfg['hosts']
    if not hosts.has_key(addr):
        return None, None

    hostname = hosts[addr]

    trap = cfg['trap']
    if values['.1.3.6.1.6.3.1.1.4.1.0'] != trap:
        return None, None

    when = cfg['when']
    for k,v in when.items():
        if values[k] != str(v):
            return None, None

    values = values.copy()

    enum = cfg['enum']
    for oid,kv in enum.items():
        if not values.has_key(oid):
            continue
        val = values[oid]
        if not kv.has_key(val):
            continue
        values[oid] = kv[val]

    environment_vars = {
        "hostname": hostname
    }

    environment = cfg['environment']
    for k,v in environment.items():
        environment_vars[k] = values[v] if values.has_key(v) else ""

    shell = cfg['shell']
    return shell, environment_vars

def executeCommand(shell, environment):
    pid = os.fork()
    if pid == 0:
        try:
            os.environ.update(environment)
            os.system(shell)
        finally:
            sys.exit()

if __name__ == '__main__':
    main()

'''
sudo snmptrap -v1 -c oreore 192.168.33.10 \
    SNMPv2-SMI::enterprises.99999 192.0.2.123 6 99 '' \
    SNMPv2-SMI::enterprises.99999.1 s おれですおれおれおれおれおれおれおれおれおれおれおれおれおれおれおれおれ \
    SNMPv2-SMI::enterprises.99999.2 i 100 \
    SNMPv2-SMI::enterprises.99999.3 i 4
'''
