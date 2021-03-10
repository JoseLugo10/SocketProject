from socket import *
import sys
import multiprocessing


def getCommand(cmd):
    finalCmd = ""
    for i in range(0, len(cmd)):
        if cmd[i] == ' ':
            break
        finalCmd = finalCmd + cmd[i]
    return finalCmd


def getCommandWIndex(cmd, index):
    finalCmd = ""
    for i in range(index, len(cmd)):
        if cmd[i] == ' ':
            break
        finalCmd = finalCmd + cmd[i]
        index = index + 1
    index = index + 1
    return finalCmd, index


def getCommandTab(cmd, index):
    finalCmd = ""
    for i in range(index, len(cmd)):
        if cmd[i] == '\t' or cmd[i] == '\n':
            break
        finalCmd = finalCmd + cmd[i]
        index = index + 1
    index = index + 1
    return finalCmd, index


def getResult(result):
    num = 0
    identifier = ""
    for i in range(0, len(result)):
        if result[i] == ':':
            break
        identifier = identifier + result[i]

    if identifier == "SUCCESS":
        num = 1
    return num


def p2pApp(clientPortNum):
    clientClientSocket.bind(('', clientPortNum))

    while True:
        msg, clientAddress = clientClientSocket.recvfrom(2048)
        decodedMsg = msg.decode()
        receivedMsg = ""

        for i in range(0, len(decodedMsg)):
            if decodedMsg[i] == '\n':
                break
            receivedMsg = receivedMsg + decodedMsg[i]

        print(receivedMsg)

        br = 0
        for i in range(0, len(decodedMsg)):
            if decodedMsg[i] == '\n':
                br = br + 1

            if br == 2:
                ind = i + 1
                for j in range(0, 6):
                    comm, ind = getCommandWIndex(decodedMsg, ind)
                comm = int(comm)
                break

        br = 0
        for i in range(0, len(decodedMsg)):
            if decodedMsg[i] == '\n':
                br = br + 1

            if br == (3 + comm):
                listIndex = int(decodedMsg[i + 1])

        userIndex = comm - listIndex

        if userIndex == 1:
            br = 0
            for i in range(0, len(decodedMsg)):
                if decodedMsg[i] == '\n':
                    br = br + 1

                if br == 3:
                    sendIndex = i + 2
                    finalName, sendIndex = getCommandTab(decodedMsg, sendIndex)
                    finalIp, sendIndex = getCommandTab(decodedMsg, sendIndex)
                    finalPort, sendIndex = getCommandTab(decodedMsg, sendIndex)
                    finalPort = int(finalPort)
                    break

            clientClientSocket.sendto(decodedMsg.encode(), (finalIp, finalPort))
        else:
            print("a")




if len(sys.argv) != 3:
    print("FAILURE: Incorrect amount of inputs")
    sys.exit()

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
clientServerSocket = socket(AF_INET, SOCK_DGRAM)

clientName = ""
clientAddress = ""
clientPort = ""
clientPortNum = 0
clientClientSocket = socket(AF_INET, SOCK_DGRAM)
registered = 0

while True:
    message = input()

    if getCommand(message) == "im-start":
        place = 0
        command1, place = getCommandWIndex(message)
        command2, place = getCommandWIndex(message)
        command3, place = getCommandWIndex(message)

        clientServerSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientServerSocket.recvfrom(2048)
        message = modifiedMessage.decode()

        if getResult(message) == 0:
            print(message)
        else:
            print(message)
            messageIM = input('Message to send to contact list: ')
            messageIM = messageIM + "\n" + message

            lineBreaks = 0
            num = ""
            for i in range(0, len(message)):
                if message[i] == '\n':
                    lineBreaks = lineBreaks + 1

                if lineBreaks == 1 and num == "":
                    for j in range(0, 6):
                        num, i = getCommandWIndex(message, i)
                    num = int(num)

                if lineBreaks == 3:
                    index = i + 1
                    sendingName, index = getCommandTab(message, index)
                    sendingIp, index = getCommandTab(message, index)
                    sendingPort, index = getCommandTab(message, index)
                    sendingPort = int(sendingPort)
                    break

            lineBreaks = 0
            for i in range(0, len(message)):
                if message[i] == '\n':
                    lineBreaks = lineBreaks + 1

                if lineBreaks == num + 1:
                    index = i + 1
                    receivingName, index = getCommandTab(message, index)
                    receivingIp, index = getCommandTab(message, index)
                    receivingPort, index = getCommandTab(message, index)
                    receivingPort = int(receivingPort)
                    break

            num = num - (num - 1)
            messageIM = messageIM + str(num)

            clientClientSocket.sendto(messageIM.encode(), (sendingIp, sendingPort))
            receivedMessage, clientAddr = clientClientSocket.recvfrom(2048)
            print(receivedMessage)

            if clientAddr == receivingIp:
                completeMsg = "im-complete " + command2 + " " + command3
                clientServerSocket.sendto(completeMsg.encode(), (serverName, serverPort))
                modifiedMessage, serverAddress = clientServerSocket.recvfrom(2048)
                message = modifiedMessage.decode()
                print(message)

    elif getCommand(message) == "register":
        clientServerSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientServerSocket.recvfrom(2048)
        message = modifiedMessage.decode()

        if getResult(message) == 0 and registered == 1:
            print("FAILURE: You have already registed")
        else:
            index = 0
            temp, index = getCommandWIndex(message, index)
            clientName, index = getCommandWIndex(message, index)

            clientAddress, index = getCommandWIndex(message, index)
            clientPort, index = getCommandWIndex(message, index)
            clientPortNum = int(clientPort)

            p1 = multiprocessing.Process(target=p2pApp, args=(clientPortNum,))
            p1.start()

    elif getCommand(message) == "exit":
        clientServerSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientServerSocket.recvfrom(2048)
        message = modifiedMessage.decode()

        if getResult(message) == 1:
            print(message)
            p1.terminate()
            break
        else:
            print(message)
    else:
        clientServerSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientServerSocket.recvfrom(2048)
        message = modifiedMessage.decode()
        print(message)

clientServerSocket.close()
clientClientSocket.close()
