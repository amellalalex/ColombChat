# ColombChat

LAN chat client written in Python.

```
(23:01:48) KeelanSupreme: As long as U have RAM you can have Colombs
(23:01:54) HaydensLaptop: thi
(23:01:56) HaydensLaptop: this is nice
Thanks boi
(23:02:02) KeelanSupreme: Thanks boi
(23:02:09) HaydensLaptop: it's cozy in here
Still can't send pics ;-(
(23:02:19) KeelanSupreme: Still can't send pics ;-(
Stay tuned for future releases
(23:02:29) KeelanSupreme: Stay tuned for future releases
(23:02:38) HaydensLaptop: how do we get carter on here
He needs ColombChat to be running
(23:02:45) KeelanSupreme: He needs ColombChat to be running
```

## Usage
Run `chat.py` using installed Python interpreter or install one of the releases for your system.

### Command Line Arguments
#### Setting a custom port
Passing a port number to the script as a command-line argument will result in changing the listen port for incoming Peer connections to whatever is passed. So long as the port is not already bound by another process and the necessary permissions to use it are present, ColombChat will listen and operate under the default assumption that this is the chat port to use.

```
python chat.py 42070
```

This also means that when connecting to other peers, NOT specifying their listen port will result in the use of this port number _rather_ than the typical default port for ColombChat.

### Windows
Extract `ColombChat.zip` and run `ColombChat.exe`.
