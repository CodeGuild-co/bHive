from microbit import *
import radio
import os

primes = []
clients = []

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

#Parsing received parameters.
def parseReceived(input):
    #Extracting parameters from message.
    params = str(input).split(" ")

    #Switching for different commands.
    if params[0] == "pong":
        #Adding ID, if not already in the list.
        if params[1] not in clients:
            clients.append(params[1])

    if params[0] == "sum":
        #Sum response from a client.
        display.show(params[2])
        #Remove client from list.
        clients.remove(params[1])

    #Handle error.
    elif params[0] == "err":
        handleError(params[1], params[2])

#Constantly sending worker_request.
while True:
    #Casting to check for clients.
    if button_a.is_pressed():
        radio.send("ping")

    if button_b.is_pressed():
        radio.send(clients[0] + " sum 2 3")

    #Parsing any responses.
    received = radio.receive()
    if received != None:
        parseReceived(received)

    #Showing current number of clients.
    display.clear()
    display.show(str(len(clients)), wait=False)