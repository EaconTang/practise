from urllib import unquote, quote
from base64 import b64decode, b64encode


# url encode
def my_urlencode(url_list):
    assert isinstance(url_list, list) is True
    if len(url_list) == 0:
        return
    print '\n[URL encode results]:'
    for each in url_list:
        print quote(each)


# url decode
def my_urldecode(encoded_url_list):
    if len(encoded_url_list) == 0:
        return
    print '\n[URL decode results]:'
    for each in encoded_url_list:
        print unquote(each)


# base64 encode
def my_base64_encode(origin_list):
    if len(origin_list) == 0:
        return
    print '\n[Base64 encode results]:'
    for each in origin_list:
        print b64encode(each)

# base64 decode
def my_base64_decode(b64_encoded_list):
    if len(b64_encoded_list) == 0:
        return
    print '\n[Base64 decode results]:'
    for each in b64_encoded_list:
        print b64decode(each)