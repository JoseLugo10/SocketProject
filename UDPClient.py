from socket import *
import sys

if len(sys.argv) != 3:
    print("FAILURE")
    sys.exit()

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
clientSocket = socket(AF_INET, SOCK_DGRAM)
for i in range(0, 50):
    message = input()
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    message = modifiedMessage.decode()
    print(message)
clientSocket.close()