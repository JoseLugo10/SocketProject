from socket import *
import sys

if len(sys.argv) != 3:
    print("FAILURE")
    sys.exit()

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
clientSocket = socket(AF_INET, SOCK_DGRAM)
for i in range(0, 3):
    message = input("Input message:\n")
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
clientSocket.close()