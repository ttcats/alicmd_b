#!/usr/bin/env python
# coding: utf-8

import logging

import tornado.websocket

from daemon import Bridge
from data import ClientData



class WSHandler(tornado.websocket.WebSocketHandler):
    clients = dict()

    def get_client(self):
        return self.clients.get(self._id(), None)

    def put_client(self):
        bridge = Bridge(self)
        self.clients[self._id()] = bridge

    def remove_client(self):
        bridge = self.get_client()
        if bridge:
            bridge.destroy()
            del self.clients[self._id()]

    @staticmethod
    def _is_init_data(data):
        return data.get_type() == 'init'

    def _id(self):
        return id(self)

    def open(self):
        self.put_client()

    def on_message(self, message):
        bridge = self.get_client()
        client_data = ClientData(message)
	logging.info(client_data.data)
        if self._is_init_data(client_data):
            bridge.open(client_data.data)
            logging.info('connection established from: %s' % self._id())
        else:
            if bridge:
                bridge.trans_forward(client_data.data)

    def on_close(self):
        self.remove_client()
        logging.info('client close the connection: %s' % self._id())

