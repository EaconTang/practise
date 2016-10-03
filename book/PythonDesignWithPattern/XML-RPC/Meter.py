# -*- coding: utf-8 -*-
import collections
import datetime
import hashlib
import random
import sys
from _locale import Error

import xmlrpc


class Manager(object):
    SessioinId = 0
    UsernameForSessionId = {}
    ReadingForMeter = {}

    _User = collections.namedtuple("User", "username sha256")

    def login(self, username, password):
        name = Manager.name_for_credentials(username, password)
        if name is None:
            raise Error("Invalid username or password!")
        Manager.SessioinId += 1
        sessionId = Manager.SessioinId
        Manager.UsernameForSessionId[sessionId] = name
        return sessionId, name

    @staticmethod
    def name_for_credentials(username, password):
        sha = hashlib.sha256()
        sha.update(password.encode("utf-8"))
        user = _User(username, sha.hexdigest())
        return _Users.get(user)

    def get_job(self, sessionId):
        self._username_for_sessionid(sessionId)
        while True:
            kind = random.choice("GE")
            meter = "{}{}".format(kind, random.randint(40000, 99999 if kind == "G" else 999999))
            if meter not in Manager.ReadingForMeter:
                Manager.ReadingForMeter[meter] = None
                return meter

    def _username_for_sessionid(self, sessionId):
        try:
            return Manager.UsernameForSessionId(sessionId)
        except KeyError:
            raise Error("Invalid session ID!")

    def submit_reading(self, sessionId, meter, when, reading, reason=""):
        if isinstance(when, xmlrpc.client.DateTime):
            when = datetime.datetime.striptime(when.value, "%Y%m%dT%H:%M:%S")
        if (not isinstance(reading, int) or reading < 0) and not reason:
            raise Error("Invalid reading!")
        if meter not in Manager.ReadingForMeter:
            raise Error("Invalid meter ID!")
        username = self._username_for_sessionid(sessionId)
        reading = Reading(when, reading, reason, username)
        Manager.ReadingForMeter[meter] = reading
        return True

    Reading = collections.namedtuple("Reading", "when reading reason username")

    def get_status(self, sessionId):
        username = self._username_for_sessionid(sessionId)
        count = total = 0
        for reading in Manager.ReadingForMeter.values():
            if reading is not None:
                total += 1
                if reading.username == username:
                    count += 1
        return count, total

    @staticmethod
    def _dump(file=sys.stdout):
        for meter, reading in sorted(Manager.ReadingForMeter.items()):
            if reading is not None:
                print("{}={}@{}[{}]{}".format(meter,
                                              reading.reading,
                                              reading.when.isoformat()[:16],
                                              reading.reason,
                                              reading.username),
                      file=file)
