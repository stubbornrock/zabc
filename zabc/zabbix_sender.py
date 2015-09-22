#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct
import simplejson
import eventlet
from eventlet.green import socket
from common import log,transfer_item_key

class ZabbixSender(object):
    zbx_header = 'ZBXD'
    zbx_version = 1

    def __init__(self, zabbix_host, zabbix_port, zabbix_proxy_name, moniter_items, zabbix_eventlet_pool):
        self.zabbix_host = zabbix_host
        self.zabbix_port = int(zabbix_port)
        self.zabbix_proxy_name = zabbix_proxy_name
        self.moniter_items = moniter_items
        self.pool = zabbix_eventlet_pool

    def get_item_data(self,sample):
        #print "Pool Gthead Num:",self.pool.running()
        item_data = {'host':'','key':'error','value':''}
        try:
            resource_id = sample['resource_id']
            counter_name = sample['counter_name']
            counter_volume = sample['counter_volume']
            #got resource_id
            if resource_id.split('-')[0] == 'instance':
                resource_id = sample['resource_metadata']['instance_id']
            #got item key
            counter_name = transfer_item_key(counter_name)
            if counter_name in self.moniter_items:
                item_data = {'host':resource_id,'key':counter_name,'value':counter_volume}
        except Exception,e:
            log.warn(str(e))
        finally:
            return item_data

    def consume_samples(self,samples):
        data = [result for result in self.pool.imap(self.get_item_data,samples) if result['key'] != 'error']
        if data:
            zbx_sender_data = {u'request': u'history data', u'host': self.zabbix_proxy_name, u'data': data}
            zbx_sender_json = simplejson.dumps(zbx_sender_data, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
            json_byte = len(zbx_sender_json)
            send_data = struct.pack("<4sBq" + str(json_byte) + "s", self.zbx_header, self.zbx_version, json_byte, zbx_sender_json)
            self.send(send_data)

    def send(self,send_data):
        try:
            so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            so.connect((self.zabbix_host, self.zabbix_port))
            #wobj = so.makefile(u'wb')
            #wobj.write(send_data)
            #wobj.close()
            #robj = so.makefile(u'rb')
            #recv_data = robj.read()
            #robj.close()
            #so.close()
            #tmp_data = struct.unpack("<4sBq" + str(len(recv_data) - struct.calcsize("<4sBq")) + "s", recv_data)
            so.sendall(send_data)
            recv_data = so.recv(1024)
            so.close()
            tmp_data = struct.unpack("<4sBq" + str(len(recv_data) - struct.calcsize("<4sBq")) + "s", recv_data)
            recv_json = simplejson.loads(tmp_data[3])
            #log.info(recv_json)
        except Exception,e:
            log.error(str(e))
