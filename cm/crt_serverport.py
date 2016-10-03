# $language = "python"
# $interface = "1.0"

def Main():
    show = '''
(1)md (2)ms (3)ud (4)da (5)pop3 (6)imap (7)session\n
(8)admin (9)webproxy (10)scequery (11)mta (12)search (13)arch (14)mscache
	'''

    svr = crt.Dialog.Prompt(show, "Input a server name(or type the number)")

    if svr in ('1', 'md'):
        svr_port = '6120'
    if svr in ('2', 'ms'):
        svr_port = '6162'
    if svr in ('3', 'ud'):
        svr_port = '6122'
    if svr in ('4', 'da'):
        svr_port = '6142'
    if svr in ('5', 'pop3'):
        svr_port = '6192'
    if svr in ('6', 'imap'):
        svr_port = '6232'
    if svr in ('7', 'session'):
        svr_port = '6152'
    if svr in ('8', 'admin'):
        svr_port = '6132'
    if svr in ('9', 'webproxy'):
        svr_port = '6212'
    if svr in ('10', 'scequery'):
        svr_port = '6172'
    if svr in ('11', 'mta'):
        svr_port = '6182'
    if svr in ('12', 'search'):
        svr_port = '6242'
    if svr in ('13', 'arch'):
        svr_port = '6202'
    if svr in ('14', 'mscache'):
        svr_port = '6642'

    crt.Screen.Send('telnet 0 %s' % svr_port + chr(13))


Main()
