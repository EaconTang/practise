import sys
from rsocks.pool import ServerPool
from rsocks.server import ReverseProxyServer


def socks_server(host, port, server_name, upstream_address, upstream_port):
    proxy = 'socks4://localhost:1080'
    pool = ServerPool()

    with pool.new_server(
        name=server_name,
        server_class=ReverseProxyServer,
        upstream=(upstream_address, int(upstream_port)),
        use_ssl=True
    ) as server:
        server.set_proxy(proxy)
        server.listen((host, int(port)))

    pool.loop()


if __name__ == '__main__':
    # try:
    #     host = sys.argv[1]
    #     port = sys.argv[2]
    #     server_name = sys.argv[3]
    #     upstream_address = sys.argv[4]
    #     upstream_port = sys.argv[5]
    #     socks_server(host, port, server_name, upstream_address, upstream_port)
    # except IndexError, e:
    #     print 'Usage: python %prog <host> <ip> <server_name> <upstream> <upstream_port>'
    #     sys.exit()
    socks_server('0.0.0.0', 5993, 'IMAP_CM', '223.252.214.65', 143)

