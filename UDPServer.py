from socket import *
import sys

# These lists will contain the 'database' of the sever for all of the users
users = []
contactList = []
query = []
initiatedIM = []

# This function is used to determine if an inputted name of a client is a member of the application.
# If they are a member of the application, 1 is returned.
def realUser(name):
    inList = 0
    for i in range(0, len(users)):
        if users[i][0] == name:
            inList = 1
            break
    return inList

# This function is used to determine if an inputted contact list name is a part of the application.
# If it is a contact list in the server, 2 is returned.
def realContactList(list):
    aList = 0
    for i in range(0, len(contactList)):
        if contactList[i] == list:
            aList = 1
            break
    return aList

# This function uses two parameters, cmd and index to separate substrings within a command given to from
# a client. If called once, it returns a string, and an int. Useful for checking legitimacy of commands given
# to the server.
def getCommand(cmd, index):
    finalCmd = ""
    for i in range(index, len(cmd)):
        if cmd[i] == ' ':
            break
        finalCmd = finalCmd + cmd[i]
        index = index + 1
    index = index + 1
    return finalCmd, index

# This function uses two parameters, list and name to check to see if a specified user is in a specified
# contact list. If they are, 1 is returned.
def inQuery(list, name):
    exist = 0
    for i in range(0, len(list)):
        if list[i][0] == name:
            exist = 1
            break
    return exist

# This function is used to determine if a client is in the middle of an IM. It checks to see if a specified
# user's 'ability' value is equal to 1. If it is, 1 is returned, and the users available commands to use
# in the server are limited.
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

# This function takes in two parameters, list and name to determine if a specified user in a specified contact
# list was the one who initiated an IM. If they did, then 1 is returned.
def startedIM(list, name):
    started = 0
    for i in range(0, len(initiatedIM)):
        if initiatedIM[i][0] == list and initiatedIM[i][1] == name:
            started = 1
            break
    return started

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

# The program checks to see if the proper amount of inputs have been made to start the server.
# If there isn't enough inputs, then the program exits.
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("FAILURE: Incorrect amount of inputs")
    sys.exit()

# If the user inputs a text file before starting the server, the server will be able to alreadt
# have all of the users, and the contact lists that they are in
if len(sys.argv) == 3:
    file = open(sys.argv[2], "r")
    text = file.read()
    file.close()

    # The loop iterates through the entire text of the opened file and parses all of the information about the users
    # and the contact lists that they are in, and stores them into lists.
    for i in range(0, len(text)):
        if text[i] == '\n':
            numUsers = int(text[i - 2])
            for j in range(0, numUsers):
                i = i + 1
                temp, i = getCommandTab(text, i)
                info1, i = getCommandTab(text, i)
                info2, i = getCommandTab(text, i)
                info3, i = getCommandTab(text, i)
                oldUser = [info1, info2, info3, 0]
                users.append(oldUser)
            break
    breaks = 0
    for i in range(0, len(text)):
        if text[i] == '\n':
            breaks = breaks + 1

        if breaks == (2 + numUsers):
            numLists = int(text[i - 2])
            for j in range(0, numLists):
                listName = ""
                for k in range(i + 1, len(text)):
                    if text[k] == ':':
                        i = k
                        break
                    listName = listName + text[k]
                memberNum = int(text[i + 2])
                for k in range(i, len(text)):
                    if text[k] == '\n':
                        i = k
                        break
                contactList.append(listName)
                newQ = [listName, []]
                query.append(newQ)
                i = i + 1
                for k in range(0, memberNum):
                    temp, i = getCommandTab(text, i)
                    info1, i = getCommandTab(text, i)
                    info2, i = getCommandTab(text, i)
                    info3, i = getCommandTab(text, i)
                    newMember = [info1, info2, info3]
                    query[j][1].append(newMember)
            break

# We create a socket based off of the port number that was given through input.
serverPort = int(sys.argv[1])
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive!")

# This while loop will go on until the user explicitly exits out of the program. It will now take in
# commands from multiple clients in the application.
while True:
    # The server receives packets from an arbitrary client, and decodes the message.
    message, clientAddress = serverSocket.recvfrom(2048)
    decodedMessage = message.decode()

    # The sentMsg variable is what we will return to the client. What the string contains is
    # based on what the client wants the server to do for it.
    sentMsg = ""
    print("The server received: " + decodedMessage)

    # The program counts the amount of spaces in the input so that the server can be sure that a valid
    # command has been sent by the client. For example: the 'register' command has in total 3 spaces,
    # so if 'register' is sent by the client but does not have 3 spaces, then the server can reject the command.
    spaces = 0
    for i in range(0, len(decodedMessage)):
        if decodedMessage[i] == ' ':
            spaces = spaces + 1

    # We get the first substring of the client's command using the getCommand() function. command1 will contain
    # the main command that the client wants to do, such as register, exit, join, etc.
    index = 0
    command1, index = getCommand(decodedMessage, index)

    if command1 == "register" and spaces == 3:
        # command2 will contain the name of the client
        command2, index = getCommand(decodedMessage, index)

        # If the name of the user sent by the client already exists in the database, a failure message is sent to
        # the client.
        if realUser(command2) == 1:
            sentMsg = "FAILURE: This user is already registered"
        elif len(users) == 7:
            sentMsg = "FAILURE: The max amount of users has been reached"
        else:
            # command3 and command4 will contain the ip address and port number of the client respectively.
            command3, index = getCommand(decodedMessage, index)
            command4, index = getCommand(decodedMessage, index)

            # The server registers the new user by putting their information in a list, and appending that list
            # into the users list which contains all of the users in the server.
            newUser = [command2, command3, command4, 0]
            users.append(newUser)
            sentMsg = "SUCCESS: " + command2 + " " + command3 + " " + command4 + " has been registered"

    elif command1 == "create" and spaces == 1:
        # command2 will contain the name of the contact list the client wants to create.
        command2, index = getCommand(decodedMessage, index)

        # If the contact list the user puts in already exists, then a failure message is sent by using the
        # realContactList() function.
        if realContactList(command2) == 1:
            sentMsg = "FAILURE: Contact list already exists"
        elif len(contactList) == 3:
            sentMsg = "FAILURE: The max amount of contact lists has been reached"
        else:
            # The program adds the contact list into the contactList list, and creates a new list with two parameters:
            # the name of the contact list, and a list for all of the members that will join.
            contactList.append(command2)
            newQuery = [command2, []]

            # We add this contact list and all of the members (0 for now) into the query list which holds
            # every single contact list, and the members of each list.
            query.append(newQuery)
            sentMsg = "SUCCESS: Contact list " + command2 + " has been created"

    elif command1 == "query-lists" and spaces == 0:
        # If there are no contact lists created yet, the server will send the client 0 lists.
        if len(query) == 0:
            sentMsg = "Number of Contact Lists: 0"
        else:
            # Using the query list, the program iterates though all of the contact lists created, and iterates through
            # each member and prints their information.
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
        # command2 and command3 get the contact list and name of the client respectively.
        command2, index = getCommand(decodedMessage, index)
        command3, index = getCommand(decodedMessage, index)

        # The program will check to see if not only the inputted user exists, but also if the inputted
        # contact list exists.
        if realUser(command3) == 0:
            sentMsg = "FAILURE: User does not exist"
        elif realContactList(command2) == 0:
            sentMsg = "FAILURE: Contact list does not exist"
        else:
            # Since users who are in an IM message have limited abilities, the hasAbilities() function will check to
            # see if the specified user is able to join a contact list at the moment.
            if hasAbilities(command3) == 1:
                sentMsg = "FAILURE: You are currently part of an ongoing IM"
            else:
                # The nested for loops are used to find the particular contact list in the query list.
                for i in range(0, len(query)):
                    if query[i][0] == command2:
                        # If the user is already in the specified contact list, then a failure message is sent.
                        if inQuery(query[i][1], command3) == 1:
                            sentMsg = "FAILURE: " + command3 + " is already in contact list " + command2
                            break
                        else:
                            # The for loop iterates through the users list so that it can find the information of the
                            # user, and insert it into the contact list the the client wants to join.
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
        # command2 and command3 get the contact list and name of the client respectively.
        command2, index = getCommand(decodedMessage, index)
        command3, index = getCommand(decodedMessage, index)

        # The program will check to see if not only the inputted user exists, but also if the inputted
        # contact list exists.
        if realUser(command3) == 0:
            sentMsg = "FAILURE: User does not exist"
        elif realContactList(command2) == 0:
            sentMsg = "FAILURE: Contact list does not exist"
        else:
            # Since users who are in an IM message have limited abilities, the hasAbilities() function will check to
            # see if the specified user is able to leave a contact list at the moment.
            if hasAbilities(command3) == 1:
                sentMsg = "FAILURE: You are currently part of an ongoing IM"
            else:
                # The nested for loops are used to find the particular contact list in the query list.
                for i in range(0, len(query)):
                    if query[i][0] == command2:
                        if inQuery(query[i][1], command3) == 1:
                            for j in range(0, len(query[i][1])):
                                # Once the user has been found, the program will remove the user from the
                                # specified contact list in the query list.
                                if query[i][1][j][0] == command3:
                                    query[i][1].remove(query[i][1][j])
                                    sentMsg = "SUCCESS: " + command3 + " has been removed from the " + command2 + " contact list"
                                    break
                        else:
                            # If the specified user is not in the contact list, then a failure message is sent
                            sentMsg = "FAILURE: " + command3 + " is not in the " + command2 + " contact list"

    elif command1 == "exit" and spaces == 1:
        # command2 gets the name of the specified user
        command2, index = getCommand(decodedMessage, index)

        # If the specified user is not in the server, a failure message is sent.
        if realUser(command2) == 0:
            sentMsg = "FAILURE: " + command2 + " is not an active user"
        else:
            # Since users who are in an IM message have limited abilities, the hasAbilities() function will check to
            # see if the specified user is able to leave the server at the moment.
            if hasAbilities(command2) == 1:
                sentMsg = "FAILURE: You are currently part of an ongoing IM"
            else:
                # The program removes the user from all of the contact lists that they might have been in.
                for i in range(0, len(query)):
                    for j in range(0, len(query[i][1])):
                        if query[i][1][j][0] == command2:
                            query[i][1].remove(query[i][1][j])
                            break
                # The program removes the user from the users list, ultimately removing them entirely from the server.
                for i in range(0, len(users)):
                    if users[i][0] == command2:
                        users.remove(users[i])
                        break

                sentMsg = "SUCCESS: " + command2 + " has left the application"

    elif command1 == "im-start" and spaces == 2:
        # command2 and command3 get the contact list and name of the client respectively.
        command2, index = getCommand(decodedMessage, index)
        command3, index = getCommand(decodedMessage, index)

        # The program will check to see if not only the inputted user exists, but also if the inputted
        # contact list exists.
        if realContactList(command2) == 0:
            sentMsg = "FAILURE: Contact list does not exit"
        elif realUser(command3) == 0:
            sentMsg = "FAILURE: User does not exist"
        else:
            # The nested for loops are used to find the particular contact list in the query list.
            for i in range(0, len(query)):
                if query[i][0] == command2:
                    # If the specified user is not in the contact list, a failure message is sent.
                    if inQuery(query[i][1], command3) == 0:
                        sentMsg = "FAILURE: User does not exist in contact list " + command2
                        break
                    else:
                        # Once the user has been found in the contact list, a string containing all of the members
                        # of that contact list is generated. Along with it is the number of users in the list.
                        sentMsg = "SUCCESS: \n"
                        sentMsg = sentMsg + "Number of contacts in " + query[i][0] + ": " + str(len(query[i][1])) + " \n"

                        # Since the information of the client who initiated the 'im-start' command needs to be first
                        # on the list, we use this for loop to place it in the string.
                        for j in range(0, len(query[i][1])):
                            if query[i][1][j][0] == command3:
                                sentMsg = sentMsg + "\t" + query[i][1][j][0]
                                sentMsg = sentMsg + "\t" + query[i][1][j][1]
                                sentMsg = sentMsg + "\t" + query[i][1][j][2] + " \n"
                                break

                        # This for loop will put the information of the remaining members of the contact list into
                        # the string. Notice how the loop filters out the name of the client who initiated the
                        # 'im-start' command so that their information is not printed out twice.
                        for j in range(0, len(query[i][1])):
                            if query[i][1][j][0] != command3:
                                sentMsg = sentMsg + "\t" + query[i][1][j][0]
                                sentMsg = sentMsg + "\t" + query[i][1][j][1]
                                sentMsg = sentMsg + "\t" + query[i][1][j][2] + " \n"

                        # Since an IM is being started, we need to make sure that the members of the contact list are
                        # not able to do specific commands. Therefore, we make the 4th parameter of each user equal to 1
                        # so that the program has a way of telling which users can do what.
                        for j in range(0, len(query[i][1])):
                            for k in range(0, len(users)):
                                if query[i][1][j][0] == users[k][0]:
                                    users[k][3] = 1
                                    break

                        # We add to the initiatedIM list another list containing the name of the contact list, and
                        # the name of the user who initiated the 'im-start' command. This will be useful for when
                        # someone other than the user tries to end the IM.
                        imStarter = [command2, command3]
                        initiatedIM.append(imStarter)
                        break

    elif command1 == "im-complete" and spaces == 2:
        # command2 and command3 get the contact list and name of the client respectively.
        command2, index = getCommand(decodedMessage, index)
        command3, index = getCommand(decodedMessage, index)

        # If the user who initiate the 'im-complete' command is not the one who started it, then a failure
        # message is sent.
        if startedIM(command2, command3) == 0:
            sentMsg = "FAILURE: You did not initiate an IM for this particular contact list"
        else:
            # Now that the IM has finished for a particular contact list, the program sets the member's 4th parameter
            # back to 0, so that they will be able to do all of the commands available on the server.
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
        # command2 contains the name for the .txt file.
        command2, index = getCommand(decodedMessage, index)

        # The program opens a .txt file that will contain the information for all of the users and contact lists on
        # the server.
        textFile = open(command2 + ".txt", "w")

        # All of the users are written onto the file.
        textFile.write("The Number of Active Users: " + str(len(users)) + " \n")
        for i in range(0, len(users)):
            textFile.write("\t" + users[i][0])
            textFile.write("\t" + users[i][1])
            textFile.write("\t" + users[i][2] + " \n")

        # All of the contact lists and their members are written onto the file.
        textFile.write("The Number of Contact Lists: " + str(len(query)) + " \n")
        for i in range(0, len(query)):
            textFile.write(query[i][0] + ": " + str(len(query[i][1])) + " members \n")
            for j in range(0, len(query[i][1])):
                textFile.write("\t" + query[i][1][j][0])
                textFile.write("\t" + query[i][1][j][1])
                textFile.write("\t" + query[i][1][j][2] + " \n")
            textFile.write("\n")

        # The file is closed and is now available.
        textFile.close()
        sentMsg = "SUCCESS: " + command2 + ".txt has been saved"
    else:
        # If the command inputted by a client is invalid, misspelled, or doesn't contain enough spaces, a failure
        # message is sent.
        sentMsg = "FAILURE: Invalid command"

    # The sentMsg string is sent back to the client who initiated any command.
    serverSocket.sendto(sentMsg.encode(), clientAddress)
