from socket import *
import sys

def getCommand(cmd, index):
    finalCmd = ""
    for i in range(index, len(cmd)):
        if cmd[i] == ' ':
            break
        finalCmd = finalCmd + cmd[i]
        index = index + 1
    index = index + 1
    return finalCmd, index

def getResult(result):
    num = 0
    identifier = ""
    for i in range(0, len(result)):
        if result[i] == ' ':
            break
        identifier = identifier + result[i]

    if identifier == "SUCCESS":
        num = 1
    return num

if len(sys.argv) != 3:
    print("FAILURE: Incorrect amount of inputs")
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