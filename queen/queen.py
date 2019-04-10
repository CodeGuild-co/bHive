from microbit import *
import radio
import os

##########################
## PRIME DEMO FUNCTIONS ##
##########################

# List of prime numbers
# Assume all numbers are prime, we'll remove the ones which aren't
primes = [i for i in range(100)]
verifiedPrimes = [2, 3, 5]
# Next number to check
nextNum = 0
testingPrimes = False

# Generate next number
def getNum():
    nextNum += 1
    return nextNum - 1

#Split the list of primes into a list of a given number of lists
def splitPrimes(number):
    # Get average length of the list of primes
    avg = len(verifiedPrimes) / float(number)
    # Start of each slice
    start = 0.0
    output = []

    # While you still can get more numbers
    while start < len(verifiedPrimes):
        output.append(verifiedPrimes[int(start):int(start + avg)])
        start += avg

    return output

### END OF PRIME DEMO FUNCTIONS ##

#List of IDs of all clients
clients = []
clientsResponded = []

#Enabling the display and radio.
display.on()
radio.on()

#Configuring the radio for group 1.
radio.config(group=1)

#Parses errors sent through.
def handleError(code, message):
    display.show("E"+str(code), wait=False)
    sleep(2000)
    display.scroll(message)

def releaseAllClients():
    for client in clients:
        radio.send(client + " release")

#Parsing received parameters.
def parseReceived(input):
    #Extracting parameters from message.
    params = str(input).split(" ")

    #Switching for different commands.
    if params[0] == "pong":
        #Adding ID, if not already in the list.
        if params[1] not in clients:
            clients.append(params[1])
            radio.send(params[1] + " hold")

    elif params[0] == "prime":
        clientsResponded.append(params[0])
        # If prime, remove from primes list
        if (not params[2]) and (params[1] in primes):
            primes.remove(params[1])

    if params[0] == "sum":
        #Sum response from a client.
        display.show(params[2], wait=False)
        sleep(5000)
        
        #Remove client from list.
        if (params[1] in clients):
            clients.remove(params[1])

    #Handle error.
    elif params[0] == "err":
        handleError(params[1], " ".join(params[2:]))

#Constantly sending worker_request.
while True:
    #Casting to check for clients.
    if button_a.is_pressed():
        radio.send("ping")

    if button_b.is_pressed():
        if len(clients) > 0:
            testingPrimes = True
            clientsResponded = clients
    
    if testingPrimes:
        # do not send out new tests until all clients have responded
        # it's best to keep this synchronised
        if len(clientsResponded) == len(clients):
            clientsResponded = []
            checkPrime = getNum()
            if (checkPrime - 1) in primes and (checPrime - 1) not in verifiedPrimes:
                # none of the fleet have discounted the previous prime, so we can verify it
                verifiedPrimes.append(checkPrime - 1)
            if checkPrime <= max(primes):
                factorPrimeLists = splitPrimes(len(clients))
                i = 0
                for client in clients:
                    radio.send(client + " testPrime " + str(checkPrime) + " " + " ".join(factorPrimeLists[i]))
                    i += 1
            else:
                testingPrimes = False
                releaseAllClients()
                display.scroll(" ".join(primes))

    #Parsing any responses.
    received = radio.receive()
    if received != None:
        parseReceived(received)

    #Showing current number of clients.
    display.clear()
    display.show(str(len(clients)), wait=False)
