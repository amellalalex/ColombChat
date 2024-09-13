class Peer:
    def __init__(self, conn_addr_pair=(None, '0.0.0.0')):
        self.conn = conn_addr_pair[0]
        self.addr = conn_addr_pair[1]