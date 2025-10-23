#This version of python did not support match case statements

import random
import sys
from poker_objects import *

HIGH_CARD = 1
PAIR = 2
TWO_PAIR = 3
THREE_KIND = 4
STRAIGHT = 5
FLUSH = 6
FULL_HOUSE = 7
FOUR_KIND = 8
STRAIGHT_FLUSH = 9
ROYAL_FLUSH = 10

HAND_SIZE = 6
DECK_SIZE = 52
NUM_SUITS = 4
NUM_VALS = 13

JACK = 11
QUEEN = 12
KING = 13
ACE = 14
ACE_LOW = 1

WIDTH = 3

#Checks if it's a straight of 10, Jack, Queen, King, and Ace
def isRoyalStraight(straight, list):

    if not straight:
        return False

    tempList = list

    tempList.sort()

    return (tempList[0].val == 10)

#Checks to see if it's a straight
def isStraight(list):

    tempList = list
    tempList.sort()
     
    if isAceOneStraight(tempList):
      list[getAceInd(list)].val = ACE_LOW  
      return True

    for i in range(len(tempList)-1):
        if tempList[i+1].val - tempList[i].val != 1:
            return False

    return True

def getAceInd(list):

    for i in range(len(list)):
        if list[i].val == ACE:
            return i
        
    print("Entered getAceInd incorrectly.")
    exit(1)

#Checks to see if it's a straight of Ace, 2, 3, 4, and 5
def isAceOneStraight(list):
   
  tempList = list
  tempList.sort()
  
  return (tempList[0].val == 2) and (tempList[1].val == 3) and (tempList[2].val == 4) and (tempList[3].val == 5) and (tempList[4].val == ACE)

#Checks if all the 5-hand card's suits are the same
def isFlush(list):

    lastSuit = list[-1].suit
    numSuits = 1

    for i in range(len(list)-1):
        if list[i].suit == lastSuit:
            numSuits += 1

    return (numSuits >= HAND_SIZE-1)

#Looks for how many duplicate values are in each hand. Allows there to be 2 unique duplicate values
def findDupValues(dupCounters, hand):

    values = []

    for i in range(len(hand)):
        values.append(hand[i].val)

    values.sort()

    #Create lists of lists that contain each common number
    lists = []
    sublist = []
    currNum = values[0]

    for i in range(len(values)):
        if currNum != values[i]:  #If we've moved onto a new number, append the sublist to the master list and reset the sublist
            lists.append(sublist)
            currNum = values[i]
            sublist = []

        sublist.append(values[i])

        if i == len(values) - 1:
            lists.append(sublist)

    bannedInd = -1
    dupCounter1 = 0
    dupCounter2 = 0

    for i in range(len(lists)):
        if len(lists[i]) > dupCounter1:
            dupCounter1 = len(lists[i]) - 1
            bannedInd = i

    for i in range(len(lists)):
        if len(lists[i]) > dupCounter2 and i != bannedInd:
            dupCounter2 = len(lists[i]) - 1

    dupCounters.append(dupCounter1)
    dupCounters.append(dupCounter2)

#Creates a list of all the hand combinations and stores it in a sort of 2D matrix (each hand object contains a hand field)
def createHandList(hand, hands):
  
    for i in range(len(hand)):
        tempHand = []
        for j in range(len(hand)):
            if j != i:
                tempHand.append(hand[j])
            else:
                removedCard = hand[j]

        dupCounters = []
        findDupValues(dupCounters, tempHand)
        dupCounter1 = dupCounters[0]
        dupCounter2 = dupCounters[1]
        flush = isFlush(tempHand)
        straight = isStraight(tempHand)
        royalStraight = isRoyalStraight(straight, tempHand)

        #Assigns the hand's type
        if royalStraight and flush:
            handVal = ROYAL_FLUSH

        elif straight and flush:
            handVal = STRAIGHT_FLUSH

        elif dupCounter1 == 3 or dupCounter2 == 3:
            handVal = FOUR_KIND

        elif (dupCounter1 == 2 and dupCounter2 == 1) or (dupCounter1 == 1 and dupCounter2 == 2):
            handVal = FULL_HOUSE

        elif flush:
            handVal = FLUSH

        elif straight:
            handVal = STRAIGHT

        elif dupCounter1 == 2 or dupCounter2 == 2:
            handVal = THREE_KIND

        elif dupCounter1 == 1 and dupCounter2 == 1:
            handVal = TWO_PAIR

        elif dupCounter1 == 1 or dupCounter2 == 1:
            handVal = PAIR

        else:
            handVal = HIGH_CARD

        h = Hand(tempHand, handVal, removedCard)
        h.removedCard = removedCard

        hands.append(h)

    hands.sort()
    hands.reverse()

#Makes the list of hands into a sort of 3D matrix, where each equivalent hand object is sorted into its own sublist
def breakDownHandList(handSublists, hands):
    
    sublist = []
    currVal = hands[0].handVal

    for i in range(len(hands)):
        if currVal != hands[i].handVal:
            handSublists.append(sublist)
            currVal = hands[i].handVal
            sublist = []

        sublist.append(hands[i])

        if (i == len(hands) - 1):
            handSublists.append(sublist)

#Enters the Tiebreaker class and breaks ties among any hand equal hand object
def breakTies(handSublists, newList):
  
    for i in range(len(handSublists)):
        if len(handSublists[i]) > 1:
            Hand.breakingTies = True
            tiedList = handSublists[i]

            for j in range(len(tiedList)):
               for k in range(len(tiedList[j].hand)):
                    tiedList[j].tiebreakerVal += tiedList[j].hand[k].val * 100000 

            for j in range(len(tiedList)):
                assignSuitVals(tiedList[j].hand)
                for k in range(len(tiedList[j].hand)):
                    tiedList[j].tiebreakerVal += tiedList[j].hand[k].suitVal * 100
            
            tiedList.sort()
            tiedList.reverse()

            for j in range(len(tiedList)):
                h = Hand(tiedList[j].hand, tiedList[j].handVal, tiedList[j].removedCard)
                newList.append(h)

            Hand.breakingTies = False
            
        else:
            newList.append(handSublists[i][0])

def assignSuitVals(hand):

    suitVals = {'D': 1, 'C': 2, 'H': 3, 'S': 4}

    for i in range(len(hand)):
        hand[i].suitVal = suitVals[hand[i].suit]

#Prints out the hand rankings after it's been establisehd           
def printHandOrder(hands):
  
   print("***High Hand Order***")
   for i in range(len(hands)):
        for j in range(len(hands[i].hand)):
            print(hands[i].hand[j].name.rjust(WIDTH), end=" ")

        print('|', end=" ")
        print(hands[i].removedCard.name.rjust(WIDTH), "--", end=" ")

        if hands[i].handVal == HIGH_CARD:
            print("High card")

        elif hands[i].handVal == PAIR:
            print("Pair")

        elif hands[i].handVal == TWO_PAIR:
            print("Two pair")

        elif hands[i].handVal == THREE_KIND:
            print("Three of a kind")

        elif hands[i].handVal == STRAIGHT:
            print("Straight")

        elif hands[i].handVal == FLUSH:
            print("Flush")

        elif hands[i].handVal == FULL_HOUSE:
            print("Full house")

        elif hands[i].handVal == FOUR_KIND:
            print("Four of a kind")

        elif hands[i].handVal == STRAIGHT_FLUSH:
            print("Straight flush")

        elif hands[i].handVal == ROYAL_FLUSH:
            print("Royal flush")

        else:
            print("Invalid hand ranking.")
            exit(1)

#Starter method for printing out the ranked hands
def rankHands(hand):

    hands = []
    createHandList(hand, hands)

    handSublists = []
    breakDownHandList(handSublists, hands)
    
    newList = []
    breakTies(handSublists, newList)
    hands = newList
    
    printHandOrder(hands)

#Prints the given hand
def showHand(hand):

    print("***This is the Hand***")
    
    for i in range(len(hand)):
      print(hand[i], end = " ")
    
    print()
    print()

#Prints out all the possible 5-card combinations
def showHandCombos(hand):

    print("***Hand Combinations***")

    for i in range(len(hand)):
        tempHand = []
        removedCard = None
        for j in range(len(hand)):
            if j != i:
                tempHand.append(hand[j])

            else:
                removedCard = hand[j]

        for j in range(len(tempHand)):
            print(tempHand[j].name.rjust(WIDTH), end=" ")

        print('|', removedCard.name.rjust(WIDTH))

    print()

#If an extra argument was entered on the command line, the hand is retrieved from the text file
def setHandFromFile(hand):

    filename = None

    if len(sys.argv) == 2:
        filename = sys.argv[1]

    else:
        print("Invalid args. There must be 2 args.")
        exit(1)

    with open(filename, 'r') as file:
        line = file.readline()
        line = line.replace(" ", "")
        line = line.replace('\n', "")
        handList = line.split(',')

        for i in range(len(handList)):
            
            val = getCardVal(handList[i])
            if val < HIGH_CARD or val > ACE:
              print("Invalid card value", val)
              exit(1)
              
            suit = getCardSuit(handList[i])
            if suit != 'D' and suit != 'C' and suit != 'H' and suit != 'S':
              print("Invalid card suit", suit)
              exit(1)
            
            name = handList[i]

            card = Card(val, suit, name)
            hand.append(card)
            
    if duplicateFound(hand):
      print("Duplicate card found in hand", end = " ")
      
      for i in range(len(hand)):
        print(hand[i].name, end = " ")
        
      print()
      
      exit(1)
      
#Checks for duplicates. If one is found, the program ends
def duplicateFound(hand):

  for i in range(len(hand)):
    bannedName = hand[i].name
    
    for j in range(len(hand)):
      if hand[j].name == bannedName and j != i:
        return True
        
  return False

#Retrieves the card's suit from its name's last character
def getCardSuit(card):

    if card[-1] == 'D' or card[-1] == 'C' or card[-1] == 'H' or card[-1] == 'S':
        return card[-1]

    else:
        print("Invalid card suit", card[-1])
        exit(1)

    return ''

#Retrieves the card's value from its name's string besides its last character
def getCardVal(card):

    cardVal = None

    if len(card) <= 2:
        cardVal = card[0]

    else:
        cardVal = card[0:2]

    if cardVal.isdigit():
        return int(cardVal)

    else:
        if cardVal == 'J':
            return JACK

        elif cardVal == 'Q':
            return QUEEN

        elif cardVal == 'K':
            return KING

        elif cardVal == 'A':
            return ACE

    return -1

#Randomly generates a 52-card deck
def createDeck(deck):

    suits = []

    for i in range(13):
        suits.append('D')
        suits.append('S')
        suits.append('H')
        suits.append('C')

    vals = []
    currVal = 2

    for i in range(DECK_SIZE):
        vals.append(currVal)
        currVal += 1

        if currVal > ACE:
            currVal = 2

    for i in range(DECK_SIZE):
        val = vals[i]
        suit = suits[i]
        name = ""

        if val < JACK:
            name += str(val)

        else:
            if val == JACK:
              name += 'J'
              
            elif val == QUEEN:
              name += 'Q'
        
            elif val == KING:
              name += 'K'
              
            elif val == ACE: 
              name += 'A'
              
            else: 
              print("Invalid card value", val)
              exit(1)

        name += suit

        card = Card(val, suit, name)

        deck.append(card)

    random.shuffle(deck)

#Prints the deck of cards
def printDeck(deck):

    print("***Shuffled", DECK_SIZE, "card deck***")

    for i in range(len(deck)):
        if i > 0 and i % NUM_VALS == 0:
            text = '\n' + deck[i].name
            print(text.ljust(WIDTH), end = " ")

        else:
            print(deck[i].name.ljust(WIDTH), end = " ")
    
    print()
    print()

#If no file is entered on the command line, take the first 6 cards from the deck
def setHand(hand, deck):

    for i in range(HAND_SIZE):
        hand.append(deck[i])

#Driver method
def playCards():
    
    deck = []
    hand = []
    
    if len(sys.argv) > 1:
      setHandFromFile(hand)
      
    else:
      createDeck(deck)
      printDeck(deck)
      setHand(hand, deck)
        
    showHand(hand)
    showHandCombos(hand)
    rankHands(hand)
  
playCards()
