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

#Parsing received parameters.
def parseReceived(input):
    #Extracting parameters from message.
    params = str(input).split(" ")

    #Switching for different commands.
    if params[0] == "pong":
        #Adding ID, if not already in the list.
        if params[1] not in clients:
            clients.append(params[1])

#Constantly sending worker_request.
while True:
    #Casting to check for clients.
    if button_a.is_pressed():
        radio.send("ping")

    if button_b.is_pressed():
        radio.send(clients[0] + " sum 2 3")
        display.scroll(clients[0] + " sum 2 3")

    #Parsing any responses.
    received = radio.receive()
    if received != None:
        parseReceived(received)

    #Showing current number of clients.
    display.clear()
    display.show(str(len(clients)), wait=False)