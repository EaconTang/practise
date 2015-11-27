import unittest
from encode_decode import *


class TestEncodeDecode(unittest.TestCase):

    def test_urlencode(self):
        """
        URL encode
        """
        url_list = [
            # Input the urls to be encoded here
        ]
        my_urlencode(url_list)


    def test_urldecode(self):
        """
        URL decode
        """
        encoded_url_str = [
            'activity=history_rate%3D9745%26rate%3D2015-11-25%25252001%25253A59%25253A02%253D19491',
        ]
        my_urldecode(encoded_url_str)

    def test_b64encode(self):
        """
        Base64 encode
        """
        origin_list = [
            'admin',
        ]
        my_base64_encode(origin_list)

    def test_b64decode(self):
        """
        Base64 decode
        """
        b64_encoded_list = [
            # 'YWRtaW4=',
        ]
        my_base64_decode(b64_encoded_list)