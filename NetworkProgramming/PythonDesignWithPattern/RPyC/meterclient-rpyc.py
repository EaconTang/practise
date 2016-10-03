# -*- coding: utf-8 -*-
def main():
    username, password = login()
    if username is not None:
        try:
            service = rpyc.connect(HOST, PORT)