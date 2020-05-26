#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import os
import threading
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

log_key = False

mu = threading.Lock()

def logInfo(word):
    '''
    普通日志输出
    :param log:
    :param word:
    :return:
    '''
    wordLast = '{0} {1} {2} \n'.format(getTimeForLog(), '-INFO -', word)
    log_file = 'log_{0}'.format(getTimeDay())
    saveToFileWithLock(log_file, wordLast)


def logError(word):
    '''
    报错日志输出
    :param log:
    :param word:
    :return:
    '''
    wordLast = '{0} {1} {2} \n'.format(getTimeForLog(), '-Error -', word)
    log_file = 'log_{0}'.format(getTimeDay())
    saveToFileWithLock(log_file, wordLast)


def logWarning(word):
    '''
    告警日志输出
    :param log:
    :param word:
    :return:
    '''
    wordLast = '{0} {1} {2} \n'.format(getTimeForLog(), '-Warn -', word)
    log_file = 'log_{0}'.format(getTimeDay())
    saveToFileWithLock(log_file, wordLast)


def saveToFile(log_file, word):
    '''
    保存日志到本地
    :param log_file:
    :param word:
    :return:
    '''
    log_path = os.path.dirname(os.path.abspath(__file__))
    print(log_path)
    file = open('{0}/{1}'.format(log_path, log_file), 'a+')
    try:
        file.write(str(word))
        file.flush()
    finally:
        file.close()


def saveToFileWithLock(log_file, word):
    if mu.acquire(True):
        saveToFile(log_file, word)
        mu.release()

def getTimeDay():
    return time.strftime("%Y%m%d", time.localtime())

def getTimeForLog():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())