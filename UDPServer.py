from socket import *
import sys

users = []
contactList = []
query = []

def realUser(name):
    inList = 0
    for i in range(0, len(users)):
        if users[i][0] == name:
            inList = 1
            break
    return inList

def realContactList(list):
    aList = 0
    for i in range(0, len(contactList)):
        if contactList[i] == list:
            aList = 1
            break
    return aList

def getCommand(cmd, index):
    finalCmd = ""
    for i in range(index, len(cmd)):
        if cmd[i] == ' ':
            break
        finalCmd = finalCmd + cmd[i]
        index = index + 1
    index = index + 1
    return finalCmd, index

def inQuery(list, name):
    exist = 0
    for i in range(0, len(list)):
        if list[i][0] == name:
            exist = 1
            break
    return exist

if len(sys.argv) != 2:
    print("FAILURE")
    sys.exit()

serverPort = int(sys.argv[1])
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    decodedMessage = message.decode()

    spaces = 0
    for i in range(0, len(decodedMessage)):
        if decodedMessage[i] == ' ':
            spaces = spaces + 1

    index = 0
    command1, index = getCommand(decodedMessage, index)

    if command1 == "register" and spaces == 3:
        command2, index = getCommand(decodedMessage, index)

        if realUser(command2) == 1:
            print("FAILURE")
        else:
            command3, index = getCommand(decodedMessage, index)
            command4, index = getCommand(decodedMessage, index)

            newUser = [command2, command3, command4]
            users.append(newUser)

    elif command1 == "create" and spaces == 1:
        command2, index = getCommand(decodedMessage, index)
        if realContactList(command2) == 1:
            print("FAILURE")
        else:
            contactList.append(command2)
            newQuery = [command2, []]
            query.append(newQuery)

    elif command1 == "query-lists" and spaces == 0:
        if len(query) == 0:
            print(0)
        else:
            print(len(query))
            for i in range(0, len(query)):
                print(query[i][0] + ":")
                for j in range(0, len(query[i][1])):
                    print(query[i][1][j])

    elif command1 == "join" and spaces == 2:
        command2, index = getCommand(decodedMessage, index)
        command3, index = getCommand(decodedMessage, index)

        if realUser(command3) == 0 or realContactList(command2) == 0:
            print("FAILURE")
        else:
            for i in range(0, len(query)):
                if query[i][0] == command2:
                    if inQuery(query[i][1], command3) == 1:
                        print("FAILURE")
                        break
                    else:
                        for j in range(0, len(users)):
                            if users[j][0] == command3:
                                newQueryMember = []
                                newQueryMember.append(users[j][0])
                                newQueryMember.append(users[j][1])
                                newQueryMember.append(users[j][2])
                                query[i][1].append(newQueryMember)
                            
    elif command1 == "leave" and spaces == 2:
        print("e")
    elif command1 == "exit" and spaces == 1:
        print("f")
    elif command1 == "im-start" and spaces == 2:
        print("g")
    elif command1 == "im-complete" and spaces == 2:
        print("h")
    elif command1 == "save" and spaces == 1:
        print("i")
    else:
        print("FAILURE")

    print(decodedMessage)
    serverSocket.sendto(decodedMessage.encode(), clientAddress)