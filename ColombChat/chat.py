import socket 
import time
import logging
import threading
import sys
import signal

from peer import Peer
from settings import *

peers = list()
globstatus = True
listen_socket = socket.socket()
hostname = socket.gethostname()

def interrupt(signal, frame):
    logging.debug('Interrupt detected. Shutting down...')
    shutdown()

def accept_incoming():
    global listen_socket
    global globstatus
    global hostname
    
    logging.debug('Listening for incoming connections...')
    # Setup listening socket
    listen_socket = socket.socket()
    try:
        listen_socket.bind(('0.0.0.0', PORT))
    except OSError:
        logging.error('Could not bind port '+str(PORT)+'. It may already be in use or you are missing necessary permissions.')
        shutdown()
        sys.exit(1)
    listen_socket.listen()
    # Listen forever
    while globstatus:
        try:
            # Accept incoming peer connection
            conn, addr = listen_socket.accept()
            peer = Peer(hostname, (conn, addr))
            logging.debug('Received peer connection: '+str(peer.conn)+','+str(peer.addr))
            # Add peer to list of peers
            peers.append(peer)
            # Create peer monitoring thread 
            thread = threading.Thread(target=monitor_peer_for_incoming_msg, args=(peers[-1],))
            peers[-1].handle = thread
            peers[-1].handle.start()
        except OSError:
            logging.debug('OSError, encountered on the listen_socket.')
    # end while True
        
def monitor_peer_for_incoming_msg(peer):
    logging.debug('Monitoring peer '+str(peer.addr)+' for incoming messages...')
    logging.info('Peer '+peer.name.decode()+' has connected to you!')
    while True:
        msg = peer.get()
        if msg != None:
            logging.info(peer.name.decode()+': '+msg.decode())
            logging.debug(str(peer.name)+'('+str(peer.addr)+'): '+str(msg))
        else:
            logging.info(peer.name.decode()+' has disconnected.')
            logging.debug(str(peer.name)+'('+str(peer.addr)+' returned None. Removing them.')
            break
    # end while True
    peers.remove(peer)
    
def close_all_peers():
    for peer in peers:
        peer.close()

def shutdown():
    global globstatus
    globstatus = False
    close_all_peers()
    listen_socket.close()

def process_msg_as_cmd(msg):
    if len(msg) > 1 and msg[0] == '/':
        run_cmd(msg)
        return True 
    else:
        return False
    
def print_help():
    logging.info("""ColombChat Help:
    0. Commands vs Messages:
        - All commands in ColombChat start with a '/' character.
        - Examples of this include '/connect' and '/quit' for starters.
        - Anything without a '/' as the first character will be sent as a normal message to every connected Peer.
    
    1. Sending Messages:
        - Write messages and hit [Enter] at any time.
        - You will need to be connected to at least one Peer to exchange messages with another client.
        
    2. Connecting to a Peer: /connect <IP> [:port]
        - Get to know the IP address of the Peer.
        - If they've optionally chosen to specify a custom listening port, you'll need that, too.
        - In your chat window, call the /connect command with the IP of the Peer and the port if needed.
        - Hint: you can either enter the port after the IP as space-separated or with a colon (so as 'IP port' or 'IP:port'). Both are fine :-).
        
    3. Closing Peer connections: /close
        - This command closes off all actively connected Peers.
        - They will need to reconnect to you, or, you will need to reconnect to them.
        
    4. Quitting: /quit or /exit
        - Closes all Peer connections and shuts the chat down.
    """)

def run_cmd(msg):
    global globstatus
    global PORT

    tokens = msg.split(' ')
    
    # TODO: Combine both if statements for /connect together
    
    if tokens[0] == '/connect' and len(tokens) >= 3:
        ip = tokens[1]
        PORT = int(tokens[2])

        logging.debug('Connecting to peer '+str((ip, PORT))+'.')
        s = socket.socket()
        s.connect((ip, PORT)) # fmt = /connect <ip> <PORT>

        peer = Peer(hostname, (s, (ip, PORT)))
        logging.info("You've connected to peer "+peer.name.decode()+"!")

        peers.append(peer)
        peers[-1].handle = threading.Thread(target=monitor_peer_for_incoming_msg, args=(peers[-1],))
        peers[-1].handle.start()
    # endif tokens[0] == '/connect' and len(tokens) >= 3
    elif tokens[0] == '/connect' and len(tokens) == 2:
        split_addr = tokens[1].split(':')
        # Check whether port was actually specified with a colon
        if len(split_addr) >= 2: # port specified
            PORT = int(split_addr[1])
        ip = split_addr[0]

        logging.debug('Connecting to peer '+str(tokens[1])+'.')
        s = socket.socket()
        s.connect((ip, PORT))

        peer = Peer(hostname, (s, (ip, PORT)))
        logging.info('Connected to peer '+peer.name.decode()+'!')

        peers.append(peer)
        peers[-1].handle = threading.Thread(target=monitor_peer_for_incoming_msg, args=(peers[-1],))
        peers[-1].handle.start()
        
    # endif tokens[0] == '/connect' and len(tokens) == 2
    elif tokens[0] == '/close':
        close_all_peers()
    # endif tokens[0] == '/close'
    elif tokens[0] == '/quit' or tokens[0] == '/exit':
        shutdown()
    elif tokens[0] == '/help' or tokens[0] == '/?':
        print_help()
    # endif tokens[0] == '/quit' or tokens[0] == '/close' or tokens[0] == '/exit'

if __name__ == '__main__':
    # Setup logging
    format = "(%(asctime)s) %(message)s"
    logging.basicConfig(
        format=format,
        level=logging.INFO,
        datefmt="%H:%M:%S"
    )
    
    # Override default PORT is command line arg present 
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    
    # Start accepting incoming connections on thread 
    accept_incoming_thread = threading.Thread(target=accept_incoming)
    accept_incoming_thread.start()

    # Set interrupt signal to shutdown
    signal.signal(signal.SIGINT, interrupt)
    
    # Welcome Message
    logging.info('Welcome to ColombChat. Type /help for guidance.') 
    
    while globstatus:
        try:
            msg = input('')
            print('\r', end='')
            logging.info(hostname+': '+msg)
            if not process_msg_as_cmd(msg):
                for peer in peers:
                    peer.send(msg)
        except EOFError:
            logging.debug('Input cut unexpectedly short.')

    accept_incoming_thread.join()