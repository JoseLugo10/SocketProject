from socket import *
import sys

users = []
contactList = []
query = []
initiatedIM = []

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

def hasAbilities(name):
    ability = 0
    for i in range(0, len(users)):
        if users[i][0] == name:
            if users[i][3] == 1:
                ability = 1
                break
            else:
                break
    return ability

def startedIM(list, name):
    started = 0
    for i in range(0, len(initiatedIM)):
        if initiatedIM[i][0] == list and initiatedIM[i][1] == name:
            started = 1
            break
    return started

if len(sys.argv) != 2:
    print("FAILURE: Incorrect amount of inputs")
    sys.exit()

serverPort = int(sys.argv[1])
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive!")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    decodedMessage = message.decode()
    sentMsg = ""

    print("The server received: " + decodedMessage)

    spaces = 0
    for i in range(0, len(decodedMessage)):
        if decodedMessage[i] == ' ':
            spaces = spaces + 1

    index = 0
    command1, index = getCommand(decodedMessage, index)

    if command1 == "register" and spaces == 3:
        command2, index = getCommand(decodedMessage, index)

        if realUser(command2) == 1:
            sentMsg = "FAILURE: This user is already registered"
        else:
            command3, index = getCommand(decodedMessage, index)
            command4, index = getCommand(decodedMessage, index)

            newUser = [command2, command3, command4, 0]
            users.append(newUser)
            sentMsg = "SUCCESS: " + command2 + " has been registered"

    elif command1 == "create" and spaces == 1:
        command2, index = getCommand(decodedMessage, index)
        if realContactList(command2) == 1:
            sentMsg = "FAILURE: Contact list already exists"
        else:
            contactList.append(command2)
            newQuery = [command2, []]
            query.append(newQuery)
            sentMsg = "SUCCESS: Contact list " + command2 + " has been created"

    elif command1 == "query-lists" and spaces == 0:
        if len(query) == 0:
            sentMsg = "Number of Contact Lists: 0"
        else:
            sentMsg = "Number of Contact Lists: " + str(len(query)) + "\n\n"
            for i in range(0, len(query)):
                sentMsg = sentMsg + query[i][0] + ":\n"
                for j in range(0, len(query[i][1])):
                    sentMsg = sentMsg + "\t" + query[i][1][j][0]
                    sentMsg = sentMsg + "\t" + query[i][1][j][1]
                    sentMsg = sentMsg + "\t" + query[i][1][j][2]
                    sentMsg = sentMsg + "\n"
                sentMsg = sentMsg + "\n"

    elif command1 == "join" and spaces == 2:
        command2, index = getCommand(decodedMessage, index)
        command3, index = getCommand(decodedMessage, index)

        if realUser(command3) == 0:
            sentMsg = "FAILURE: User does not exist"
        elif realContactList(command2) == 0:
            sentMsg = "FAILURE: Contact list does not exist"
        else:
            if hasAbilities(command3) == 1:
                sentMsg = "FAILURE: You are currently part of an ongoing IM"
            else:
                for i in range(0, len(query)):
                    if query[i][0] == command2:
                        if inQuery(query[i][1], command3) == 1:
                            sentMsg = "FAILURE: " + command3 + " is already in contact list " + command2
                            break
                        else:
                            for j in range(0, len(users)):
                                if users[j][0] == command3:
                                    newQueryMember = []
                                    newQueryMember.append(users[j][0])
                                    newQueryMember.append(users[j][1])
                                    newQueryMember.append(users[j][2])
                                    query[i][1].append(newQueryMember)
                                    sentMsg = "SUCCESS: " + command3 + " has joined the " + command2 + " contact list"
                                    break
                            
    elif command1 == "leave" and spaces == 2:
        command2, index = getCommand(decodedMessage, index)
        command3, index = getCommand(decodedMessage, index)

        if realUser(command3) == 0:
            sentMsg = "FAILURE: User does not exist"
        elif realContactList(command2) == 0:
            sentMsg = "FAILURE: Contact list does not exist"
        else:
            if hasAbilities(command3) == 1:
                sentMsg = "FAILURE: You are currently part of an ongoing IM"
            else:
                for i in range(0, len(query)):
                    if query[i][0] == command2:
                        if inQuery(query[i][1], command3) == 1:
                            for j in range(0, len(query[i][1])):
                                if query[i][1][j][0] == command3:
                                    query[i][1].remove(query[i][1][j])
                                    sentMsg = "SUCCESS: " + command3 + " has been removed from the " + command2 + " contact list"
                                    break
                        else:
                            sentMsg = "FAILURE: " + command3 + " is not in the " + command2 + " contact list"

    elif command1 == "exit" and spaces == 1:
        print("f")
    elif command1 == "im-start" and spaces == 2:
        command2, index = getCommand(decodedMessage, index)
        command3, index = getCommand(decodedMessage, index)

        if realContactList(command2) == 0:
            sentMsg = "FAILURE: Contact list does not exit"
        elif realUser(command3) == 0:
            sentMsg = "FAILURE: User does not exist"
        else:
            for i in range(0, len(query)):
                if query[i][0] == command2:
                    if inQuery(query[i][1], command3) == 0:
                        sentMsg = "FAILURE: User does not exist in contact list " + command2
                        break
                    else:
                        sentMsg = "SUCCESS:\n"
                        sentMsg = sentMsg + "Number of contacts in " + query[i][0] + ": " + str(len(query[i][1])) + "\n"

                        for j in range(0, len(query[i][1])):
                            if query[i][1][j][0] == command3:
                                sentMsg = sentMsg + "\t" + query[i][1][j][0]
                                sentMsg = sentMsg + "\t" + query[i][1][j][1]
                                sentMsg = sentMsg + "\t" + query[i][1][j][2] + "\n"
                                break

                        for j in range(0, len(query[i][1])):
                            if query[i][1][j][0] != command3:
                                sentMsg = sentMsg + "\t" + query[i][1][j][0]
                                sentMsg = sentMsg + "\t" + query[i][1][j][1]
                                sentMsg = sentMsg + "\t" + query[i][1][j][2] + "\n"

                        for j in range(0, len(query[i][1])):
                            for k in range(0, len(users)):
                                if query[i][1][j][0] == users[k][0]:
                                    users[k][3] = 1
                                    break

                        imStarter = [command2, command3]
                        initiatedIM.append(imStarter)
                        break

    elif command1 == "im-complete" and spaces == 2:
        command2, index = getCommand(decodedMessage, index)
        command3, index = getCommand(decodedMessage, index)

        if startedIM(command2, command3) == 0:
            sentMsg = "FAILURE: You did not initiate an IM for this particular contact list"
        else:
            for i in range(0, len(query)):
                if query[i][0] == command2:
                    for j in range(0, len(query[i][1])):
                        for k in range(0, len(users)):
                            if query[i][1][j][0] == users[k][0]:
                                users[k][3] = 0
                                break
                    break
            sentMsg = "SUCCESS: IM has been completed"

    elif command1 == "save" and spaces == 1:
        command2, index = getCommand(decodedMessage, index)

        textFile = open(command2 + ".txt", "w")
        textFile.write("The Number of Active Users: " + str(len(users)) + "\n")
        for i in range(0, len(users)):
            textFile.write("\t" + users[i][0])
            textFile.write("\t" + users[i][1])
            textFile.write("\t" + users[i][2] + "\n")

        textFile.write("\nThe Number of Contact Lists: " + str(len(query)) + "\n")
        for i in range(0, len(query)):
            textFile.write(query[i][0] + ": " + str(len(query[i][1])) + " members\n")
            for j in range(0, len(query[i][1])):
                textFile.write("\t" + query[i][1][j][0])
                textFile.write("\t" + query[i][1][j][1])
                textFile.write("\t" + query[i][1][j][2] + "\n")
            textFile.write("\n")

        textFile.close()
        sentMsg = "SUCCESS: " + command2 + ".txt has been saved"
    else:
        sentMsg = "FAILURE: Invalid command"

    serverSocket.sendto(sentMsg.encode(), clientAddress)