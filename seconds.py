#!/usr/bin/env python3

def to_seconds(hours, minutes, seconds):
    return 3600*hours+60*minutes+seconds

print("Welcome to the Time Converter!")

cont = "y"
while(cont.lower() == "y"):
    hours = int(input("Please enter in the number of hours: "))
    minutes = int(input("Please enter in the number of minutes: "))
    seconds = int(input("Please enter the number of seconds: "))

    print("That's {} seconds".format(to_seconds(hours, minutes, seconds)))
    print()
    cont = input("Do you want to do another conversion? [y to continue]")

print("Good Bye!")    
