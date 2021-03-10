from socket import *
import sys
import multiprocessing

# This function is used to separate substrings within a command given to from the client. It returns the string
# for the substring.
def getCommand(cmd):
    finalCmd = ""
    for i in range(0, len(cmd)):
        if cmd[i] == ' ':
            break
        finalCmd = finalCmd + cmd[i]
    return finalCmd

# This function uses two parameters, cmd and index to separate substrings within a command given to from
# a client. If called once, it returns a string, and an int. Useful for checking legitimacy of commands given
# to the server.
def getCommandWIndex(cmd, index):
    finalCmd = ""
    for i in range(index, len(cmd)):
        if cmd[i] == ' ':
            break
        finalCmd = finalCmd + cmd[i]
        index = index + 1
    index = index + 1
    return finalCmd, index

# This function uses two parameters, cmd and index to separate substrings within a command given to from
# a client. If called once, it returns a string, and an int. Unlike the previous function, this seperates
# commands based off of \t and \n instead of ' '.
def getCommandTab(cmd, index):
    finalCmd = ""
    for i in range(index, len(cmd)):
        if cmd[i] == '\t' or cmd[i] == '\n':
            break
        finalCmd = finalCmd + cmd[i]
        index = index + 1
    index = index + 1
    return finalCmd, index

# This function is used to get the string that is returned from the server. Particularly, the substring that contains
# either 'SUCCESS' or 'FAILURE'. If it is 'SUCCESS', 1 is returned. This is useful for determining if certain commands
# can be completed by the client.
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

# This function acts as the P2P side of the entire project. This function is only called as a separate process.
# The function takes in 2 parameters, which correspond to the port number of the client, and the actual socket
# of the client, which communicates with other clients.
def p2pApp(clientPortNum, clientClientSocket):
    clientClientSocket.bind(('', clientPortNum))

    # This while loop will go on until the process is terminated. This will only happen if the client leaves the server
    # entirely. Otherwise, a blocking recvfrom() function is called and blocks until it has received packets
    # from another client.
    while True:
        msg, clientAddress = clientClientSocket.recvfrom(2048)
        decodedMsg = msg.decode()

        # Since the decodedMsg will contain not only the message sent by the client, but also the list of all of the
        # other users in the contact list, we need to separate the message sent from the client. In order to do this, a
        # string named receivedMsg is made that will contain it.
        receivedMsg = ""

        br = 0
        for i in range(0, len(decodedMsg)):
            if decodedMsg[i] == '\n':
                br = br + 1

        for i in range(0, len(decodedMsg)):
            if decodedMsg[i] == '\n':
                break
            receivedMsg = receivedMsg + decodedMsg[i]

        receivedMsg = receivedMsg + '\n'

        if br > 1:
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

            listIndex = int(decodedMsg[len(decodedMsg) - 1])

            userIndex = comm - listIndex

            finalSentMsg = ""
            for i in range(0, (len(decodedMsg) - 1)):
                finalSentMsg = finalSentMsg + decodedMsg[i]

            finalSentMsg = finalSentMsg + str(listIndex + 1)

            if (listIndex + 1) >= comm:
                print(receivedMsg)
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

                clientClientSocket.sendto(receivedMsg.encode(), (finalIp, finalPort))
            else:
                print(receivedMsg)
                br = 0
                for i in range(0, len(decodedMsg)):
                    if decodedMsg[i] == '\n':
                        br = br + 1

                    if br == (listIndex + 4):
                        sendIndex = i + 2
                        nextName, sendIndex = getCommandTab(decodedMsg, sendIndex)
                        nextIp, sendIndex = getCommandTab(decodedMsg, sendIndex)
                        nextPort, sendIndex = getCommandTab(decodedMsg, sendIndex)
                        nextPort = int(nextPort)
                        break

                clientClientSocket.sendto(finalSentMsg.encode(), (nextIp, nextPort))
        else:
            print(receivedMsg)

# The program checks to see if the proper amount of inputs have been made to connect to the server. If not
# the program will exit.
if len(sys.argv) != 3:
    print("FAILURE: Incorrect amount of inputs")
    sys.exit()

# The server information that the client wants to connect to is gathered from the user input.
serverName = sys.argv[1]
serverPort = int(sys.argv[2])
clientServerSocket = socket(AF_INET, SOCK_DGRAM)

# Variables for the P2P client socket are created here.
clientName = ""
clientAddress = ""
clientPort = ""
clientPortNum = 0
clientClientSocket = socket(AF_INET, SOCK_DGRAM)

# This variable determines if a client is already registered in the server.
registered = 0

while True:
    # The input of the user is gathered here.
    message = input()

    # If the user wants to start an IM, the program will go here.
    if getCommand(message) == "im-start":
        # command1, command2, and command3 contain 'im-start', the name of the contact list, and the name of the client
        # respectively.
        place = 0
        command1, place = getCommandWIndex(message, place)
        command2, place = getCommandWIndex(message, place)
        command3, place = getCommandWIndex(message, place)

        # The message is sent to the server.
        clientServerSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientServerSocket.recvfrom(2048)
        message = modifiedMessage.decode()

        # If the 'im-start' command is unsuccessful, the message from the server is printed.
        if getResult(message) == 0:
            print(message)
        else:
            # Now that the server has green-lighted the 'im-start' command, the client can begin messaging. The
            # string messageIM will contain the message that will be sent to all other clients in the contact list.
            print(message)
            messageIM = input('Message to send to contact list: ')
            messageIM = messageIM + " \n" + message

            # This for loop will go through the message sent from the server, in order to find the client that this
            # particular client must send to. Since the first client that needs the message sent to is the second on the
            # list, the program skips lines until it reaches that client.
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
                    index = i + 2
                    sendingName, index = getCommandTab(message, index)
                    sendingIp, index = getCommandTab(message, index)
                    sendingPort, index = getCommandTab(message, index)
                    sendingPort = int(sendingPort)
                    break

            # By adding num to the end of the messageIM, we can keep track of who on the list needs the message sent to
            # next. It acts as an index to determine which person on the list should be receiving the message next.
            num = num - (num - 1)
            messageIM = messageIM + str(num)

            # The messageIM is sent to the first client.
            clientClientSocket.sendto(messageIM.encode(), (sendingIp, sendingPort))

            # Once the message this client sent is received back from the last client on the list, we automatically
            # send the 'im-complete' command to the server, thus finishing the message.
            completeMsg = "im-complete " + command2 + " " + command3
            clientServerSocket.sendto(completeMsg.encode(), (serverName, serverPort))
            modifiedMessage, serverAddress = clientServerSocket.recvfrom(2048)
            message = modifiedMessage.decode()
            print(message)

    # If the client wants to register into the server, the program will go here.
    elif getCommand(message) == "register":
        # The message is sent to the server
        clientServerSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientServerSocket.recvfrom(2048)
        message = modifiedMessage.decode()

        # If the user has already registered with the server, a failure message is printed.
        if getResult(message) == 0 or registered == 1:
            print("FAILURE: You have already registed")
        else:
            print(message)
            registered = 1
            index = 0
            temp, index = getCommandWIndex(message, index)

            # We use the getCommandWIndex() function to get the parameters of the clients info. Such as IP and port num.
            clientName, index = getCommandWIndex(message, index)
            clientAddress, index = getCommandWIndex(message, index)
            clientPort, index = getCommandWIndex(message, index)
            clientPortNum = int(clientPort)

            # A separate process is started that will initiate the P2P side of the client. A separate process is started
            # with the given parameters of the registration, so that it can receive messages from other clients.
            p1 = multiprocessing.Process(target=p2pApp, args=(clientPortNum, clientClientSocket,))
            p1.start()

    # Should the client want to exit the application, the program will go here.
    elif getCommand(message) == "exit":
        # The message is sent to the server.
        clientServerSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientServerSocket.recvfrom(2048)
        message = modifiedMessage.decode()

        # If the client has successfully exited the server, a message is printed, the p1 (P2P socket) is terminated, and
        # we exit out of the while loop to close all of the sockets.
        if getResult(message) == 1:
            print(message)
            p1.terminate()
            break
        else:
            print(message)
    else:
        # The program will default here if none of the commands given by the user correlate to any of the ones above.
        clientServerSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientServerSocket.recvfrom(2048)
        message = modifiedMessage.decode()
        print(message)

# All of the sockets are closed.
clientServerSocket.close()
clientClientSocket.close()
