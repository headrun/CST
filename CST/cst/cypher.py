#!/usr/bin/python

import time

from Crypto.Cipher import AES
from Crypto import Random
from django.conf import settings


def encode(msg):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(settings.ENCRYPTION_KEY, AES.MODE_CFB, iv)
    encoded_msg = iv + cipher.encrypt(msg)
    return encoded_msg.encode('hex')


def decode(encoded_msg):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(settings.ENCRYPTION_KEY, AES.MODE_CFB, iv)
    return cipher.decrypt(encoded_msg.decode('hex'))[len(iv):]


def encode_id(id):
    return encode('%s/%s' % (id, time.time()))


def decode_id(encoded_id):
    return decode(encoded_id).split('/')[0]
