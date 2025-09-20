from poker_objects import *
import copy
import sys

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

STAGE_PRIMER = 1

ACE = 14
ACE_LOW = 1

#Note: each tiebreaker method recursively goes through a matrix containing lists of equal tiebreaker values through different tiebreaking stages until each sublist has one item
class Tiebreaker:
  
  #Determines which type of hands we need to break the tie on
  def breakTie(self, tiedList):
  
    if tiedList[0].handVal == HIGH_CARD:
      self.highCard(tiedList)
      
    elif tiedList[0].handVal == PAIR:
      self.pair(tiedList)
      
    elif tiedList[0].handVal == TWO_PAIR:
      self.twoPair(tiedList)
      
    elif tiedList[0].handVal == THREE_KIND:
      self.threeKind(tiedList)
      
    elif tiedList[0].handVal == STRAIGHT:
      self.straight(tiedList)
      
    elif tiedList[0].handVal == FLUSH:
      self.flush(tiedList)
      
    elif tiedList[0].handVal == FULL_HOUSE:
      self.fullHouse(tiedList)
      
    elif tiedList[0].handVal == FOUR_KIND:
      self.fourKind(tiedList)
      
    elif tiedList[0].handVal == STRAIGHT_FLUSH:
      self.straightFlush(tiedList)
      
    elif tiedList[0].handVal == ROYAL_FLUSH:
      self.royalFlush(tiedList)
      
    else:
      print("Invalid hand value", tiedList[0].handVal, "detected.")
      exit(1)
  
  #For four of a kinds, full houses, three of a kinds, two pairs, and pairs, we need to split the hands so we can break ties among them properly
  def splitHand(self, tiedList, hand, ind, val1, val2, val3):
  
    cardLists = self.breakDownHand(hand)    
    
    for i in range(len(cardLists)):
      if len(cardLists[i]) == val1 and len(tiedList[ind].part1_hand) < val1:
        for j in range(len(cardLists[i])):
          tiedList[ind].part1_hand.append(cardLists[i][j])
        
      elif len(cardLists[i]) == val2:
        for j in range(len(cardLists[i])):
          tiedList[ind].part2_hand.append(cardLists[i][j])
        
      elif len(cardLists[i]) == val3:
        tiedList[ind].kicker = cardLists[i][0]
      
      else:
        print("Invalid partial hand size", len(cardLists[i]), "detected.")
        exit(1)
  
  #Increments the tiebreaker value based on the kicker's card value
  def valTiebreakerKicker(self, hands):
  
    for i in range(len(hands)):
      hands[i].tiebreakerVal += hands[i].kicker.val
    
    hands.sort()
    hands.reverse()

  #Increments the tiebreaker value based on the card's value from the second-highest priority section of the hand
  def valTiebreakerPart2Hand(self, ind, hands):  
    
    for i in range(len(hands)):
      hands[i].tiebreakerVal += hands[i].part2_hand[ind].val
      
    hands.sort()
    hands.reverse()
  
  #Increments the tiebreaker value based on the card's suit value 
  def suitTiebreaker(self, ind, hands):
  
    for i in range(len(hands)):
      hands[i].hand.sort()
      hands[i].hand.reverse()
      hands[i].tiebreakerVal += hands[i].hand[ind].suitVal
      
    hands.sort()
    hands.reverse()
  
  #Increments the tiebreaker value based on the card's suit value from the highest priority section of the hand
  def suitTiebreakerPart1Hand(self, ind, hands):
    
    for i in range(len(hands)):
      hands[i].tiebreakerVal += hands[i].part1_hand[ind].suitVal
      
    hands.sort()
    hands.reverse()
  
  #Increments the tiebreaker value based on the card's suit value from the second-highest priority section of the hand
  def suitTiebreakerPart2Hand(self, ind, hands):
    
    for i in range(len(hands)):
      hands[i].tiebreakerVal += hands[i].part2_hand[ind].suitVal
      
    hands.sort()
    hands.reverse()
  
  #Increments the tiebreaker value based on the kicker card's suit value from the
  def suitTiebreakerKicker(self, hands):
  
    for i in range(len(hands)):
      hands[i].tiebreakerVal += hands[i].kicker.suitVal
      
    hands.sort()
    hands.reverse()
  
  #Increments the hand's tiebreaker value based on the card's value
  def valTiebreaker(self, ind, hands):
    
    for i in range(len(hands)):
      hands[i].tiebreakerVal += hands[i].hand[ind].val
      
    hands.sort()
    hands.reverse()
  
  #Sets up royal flush tiebreaker
  def royalFlush(self, tiedList):
    
    for i in range(len(tiedList)):
      self.assignSuitVals(tiedList[i].part1_hand)
      
    self.breakTie_RoyalFlush(tiedList)
  
  #Royal flush tiebreaker
  def breakTie_RoyalFlush(self, tiedList):
    
    self.convertToSuits(tiedList)
    
    for i in range(len(tiedList)):
      tiedList[i].tiebreakerVal += tiedList[i].hand[0].suitVal
      
    tiedList.sort()
    tiedList.reverse()
  
  #Sets up straight flush tiebreaker
  def straightFlush(self, tiedList):
    
    for i in range(len(tiedList)):
      if self.isAceLowStraight(tiedList[i].hand):
        aceInd = self.getAceInd(tiedList[i].hand)
        tiedList[i].hand[aceInd].val = ACE_LOW
    
      tiedList[i].hand.sort()
      tiedList[i].hand.reverse()
      self.assignSuitVals(tiedList[i].part1_hand)
      
    self.breakTie_StraightFlush(tiedList, STAGE_PRIMER)
  
  #Straight flush tiebreaker
  def breakTie_StraightFlush(self, tiedList, stage):
    
    HAND_SIZE = 5
    
    if stage == 1:
      for i in range(len(tiedList)):
        tiedList[i].tiebreakerVal += tiedList[i].hand[0].val
        
      tiedList.sort()
      tiedList.reverse()
      
    tiedSublists = self.breakDownList(tiedList)
    
    for i in range(len(tiedSublists)):
      if len(tiedSublists[i]) > 1:
        if stage == 2:
          self.convertToSuits(tiedSublists[i])
          self.suitTiebreaker(0, tiedSublists[i])
          
        self.breakTie_StraightFlush(tiedList, stage+1)
  
  #Sets up for of a kind tiebreaker
  def fourKind(self, tiedList):
    
    val1 = 4
    val2 = 0
    val3 = 1
    
    for i in range(len(tiedList)):
      self.splitHand(tiedList, tiedList[i].hand, i, val1, val2, val3)
      self.assignSuitVals(tiedList[i].part1_hand)
      self.assignSuitVal(tiedList[i].kicker)
      
    self.breakTie_FourKind(tiedList, STAGE_PRIMER)
  
  #Four of a kind tiebreaker
  def breakTie_FourKind(self, tiedList, stage):
    
    PART1_HAND_SIZE = 4
    
    if stage == 1:
      for i in range(len(tiedList)):
        quadVal = tiedList[i].part1_hand[0].val
        tiedList[i].tiebreakerVal += quadVal
        
      tiedList.sort()
      tiedList.reverse()
      
    tiedSublists = self.breakDownList(tiedList)
    
    for i in range(len(tiedSublists)):
      if len(tiedSublists[i]) > 1:
        if stage == 2:
          self.convertToSuitsPartial(tiedSublists[i])
         
          for j in range(PART1_HAND_SIZE):
            self.suitTiebreakerPart1Hand(j, tiedSublists[i])
            
        elif stage == 3:
          self.convertToValsPartial(tiedSublists[i])
          self.valTiebreakerKicker(tiedSublists[i])
           
        elif stage == 4:
          self.convertToSuitsPartial(tiedSublists[i])
          self.suitTiebreakerKicker(tiedSublists[i])
           
        self.breakTie_FourKind(tiedSublists[i], stage+1)
        
    updatedList = []
    
    for i in range(len(tiedSublists)):
      for j in range(len(tiedSublists[i])):
        updatedList.append(tiedSublists[i][j])
        
    tiedList[:] = updatedList
  
  #Sets up full house tiebreaker  
  def fullHouse(self, tiedList):
  
    val1 = 3
    val2 = 2
    val3 = 0
    
    for i in range(len(tiedList)):
      self.splitHand(tiedList, tiedList[i].hand, i, val1, val2, val3)
      self.assignSuitVals(tiedList[i].part1_hand)
      self.assignSuitVals(tiedList[i].part2_hand)
      
    self.breakTie_FullHouse(tiedList, STAGE_PRIMER)
  
  #Full house tiebreaker
  def breakTie_FullHouse(self, tiedList, stage):
  
    PART1_HAND_SIZE = 3
    PART2_HAND_SIZE = 2
    
    if stage == 1:
      for i in range(len(tiedList)):
        trioVal = tiedList[i].part1_hand[0].val
        tiedList[i].tiebreakerVal += trioVal
        
      tiedList.sort()
      tiedList.reverse()
    
    tiedSublists = self.breakDownList(tiedList)
    
    for i in range(len(tiedSublists)):
      if len(tiedSublists[i]) > 1:        
        if stage == 2:
          self.convertToSuitsPartial(tiedSublists[i])
         
          for j in range(PART1_HAND_SIZE):
            self.suitTiebreakerPart1Hand(j, tiedSublists[i])
         
        elif stage == 3:
          self.convertToValsPartial(tiedSublists[i])
          
          self.valTiebreakerPart2Hand(0, tiedSublists[i])
          
        elif stage == 4:
          self.convertToSuitsPartial(tiedSublists[i])
          
          for j in range(PART2_HAND_SIZE):
            self.suitTiebreakerPart2Hand(j, tiedSublists[i])

        self.breakTie_FullHouse(tiedSublists[i], stage+1)
        
    updatedList = []
    
    for i in range(len(tiedSublists)):
      for j in range(len(tiedSublists[i])):
        updatedList.append(tiedSublists[i][j])
        
    tiedList[:] = updatedList
  
  #Sets up flush tiebreaker
  def flush(self, tiedList):
    
    for i in range(len(tiedList)):
      tiedList[i].hand.sort()
      tiedList[i].hand.reverse()
      self.assignSuitVals(tiedList[i].hand)
      
    self.breakTie_Flush(tiedList, STAGE_PRIMER)
  
  #Flush tiebreaker
  def breakTie_Flush(self, tiedList, stage):
  
    HAND_SIZE = 5
    
    if stage == 1:
      for i in range(HAND_SIZE):
        self.valTiebreaker(i, tiedList)
        
      tiedList.sort()
      tiedList.reverse()
        
    tiedSublists = self.breakDownList(tiedList)
    
    for i in range(len(tiedSublists)):
      if len(tiedSublists[i]) > 1:
        if stage == 2:
          self.convertToSuits(tiedList)
          
          for j in range(len(tiedSublists[i])):
            tiedList[i].tiebreakerVal += tiedList[i].hand[0].suitVal
  
  #Sets up straight tiebreaker        
  def straight(self, tiedList):
  
    for i in range(len(tiedList)):
      if self.isAceLowStraight(tiedList[i].hand):
        aceInd = self.getAceInd(tiedList[i].hand)
        tiedList[i].hand[aceInd].val = ACE_LOW
        
      tiedList[i].hand.sort()
      tiedList[i].hand.reverse()
      self.assignSuitVals(tiedList[i].hand)
      
    self.breakTie_Straight(tiedList, STAGE_PRIMER)
  
  #Straight tiebreaker
  def breakTie_Straight(self, tiedList, stage):
  
    HAND_SIZE = 5
    
    if stage == 1:
      for i in range(len(tiedList)):
        tiedList[i].tiebreakerVal += tiedList[i].hand[0].val
      
      tiedList.sort()
      tiedList.reverse()
        
    tiedSublists = self.breakDownList(tiedList)
    
    for i in range(len(tiedSublists)):
      if len(tiedSublists[i]) > 1:
        if stage == 2:
          self.convertToSuits(tiedSublists[i])
          
          for j in range(HAND_SIZE):
            self.suitTiebreaker(j, tiedSublists[i])
            
        self.breakTie_Straight(tiedSublists[i], stage+1)
        
    updatedList = []
    
    for i in range(len(tiedSublists)):
      for j in range(len(tiedSublists[i])):
        updatedList.append(tiedSublists[i][j])
        
    tiedList[:] = updatedList
  
  #Sets up three of a kind tiebreaker
  def threeKind(self, tiedList):
    
    val1 = 3
    val2 = 1 #Append each different card outside of the three-kind hand to part2 list
    val3 = 0
    
    for i in range(len(tiedList)):
      self.splitHand(tiedList, tiedList[i].hand, i, val1, val2, val3)
      self.assignSuitVals(tiedList[i].part1_hand)
      self.assignSuitVals(tiedList[i].part2_hand)
      
    self.breakTie_ThreeKind(tiedList, STAGE_PRIMER)
  
  #Three of a kind tiebreaker 
  def breakTie_ThreeKind(self, tiedList, stage):
    
    PART1_HAND_SIZE = 3
    PART2_HAND_SIZE = 2
    
    if stage == 1:
      for i in range(len(tiedList)):
        trioVal = tiedList[i].part1_hand[0].val
        tiedList[i].tiebreakerVal += trioVal
        
      tiedList.sort()
      tiedList.reverse()
    
    tiedSublists = self.breakDownList(tiedList)
    
    for i in range(len(tiedSublists)):
      if len(tiedSublists[i]) > 1:        
        if stage == 2:
          self.convertToSuitsPartial(tiedSublists[i])
         
          for j in range(PART1_HAND_SIZE):
            self.suitTiebreakerPart1Hand(j, tiedSublists[i])
         
        elif stage == 3:
          self.convertToValsPartial(tiedSublists[i])
          
          for j in range(PART2_HAND_SIZE):
            self.valTiebreakerPart2Hand(j, tiedSublists[i])
          
        elif stage == 4:
          self.convertToSuitsPartial(tiedSublists[i])
          
          for j in range(PART2_HAND_SIZE):
            self.suitTiebreakerPart2Hand(j, tiedSublists[i])

        self.breakTie_ThreeKind(tiedSublists[i], stage+1)
        
    updatedList = []
    
    for i in range(len(tiedSublists)):
      for j in range(len(tiedSublists[i])):
        updatedList.append(tiedSublists[i][j])
        
    tiedList[:] = updatedList
  
  #Sets up two pair tiebreaker
  def twoPair(self, tiedList):

    val1 = 2
    val2 = 2
    val3 = 1

    for i in range(len(tiedList)):
      self.splitHand(tiedList, tiedList[i].hand, i, val1, val2, val3)
      
      part1Val = tiedList[i].part1_hand[0].val
      part2Val = tiedList[i].part2_hand[0].val

      if part2Val > part1Val:
        temp = copy.deepcopy(tiedList[i].part2_hand)
        tiedList[i].part2_hand[:] = copy.deepcopy(tiedList[i].part1_hand)
        tiedList[i].part1_hand[:] = copy.deepcopy(temp)
        
      self.assignSuitVals(tiedList[i].part1_hand)
      self.assignSuitVals(tiedList[i].part2_hand)
      self.assignSuitVal(tiedList[i].kicker)
        
    self.breakTie_TwoPair(tiedList, STAGE_PRIMER)

  #Two pair tiebreaker
  def breakTie_TwoPair(self, tiedList, stage):
    
    PART1_HAND_SIZE = 2
    PART2_HAND_SIZE = 2
    
    if stage == 1:
      for i in range(len(tiedList)):
        pairVal = tiedList[i].part1_hand[0].val
        tiedList[i].tiebreakerVal += pairVal
        
      tiedList.sort()
      tiedList.reverse()
    
    tiedSublists = self.breakDownList(tiedList)
    
    for i in range(len(tiedSublists)):
      if len(tiedSublists[i]) > 1:        
        if stage == 2:
          self.convertToSuitsPartial(tiedSublists[i])
         
          for j in range(PART1_HAND_SIZE):
            self.suitTiebreakerPart1Hand(j, tiedSublists[i])
         
        elif stage == 3:
          self.convertToValsPartial(tiedSublists[i])
          self.valTiebreakerPart2Hand(0, tiedSublists[i])
          
        elif stage == 4:
          self.convertToSuitsPartial(tiedSublists[i])
          
          for j in range(PART2_HAND_SIZE):
            self.suitTiebreakerPart2Hand(j, tiedSublists[i])
            
        elif stage == 5:
          self.valTiebreakerKicker(tiedSublists[i])
            
        elif stage == 6:
          self.suitTiebreakerKicker(tiedSublists[i])
    
        self.breakTie_TwoPair(tiedSublists[i], stage+1)
        
    updatedList = []
    
    for i in range(len(tiedSublists)):
      for j in range(len(tiedSublists[i])):
        updatedList.append(tiedSublists[i][j])
        
    tiedList[:] = updatedList
  
  #Sets up pair tiebreaker   
  def pair(self, tiedList):
    
    val1 = 2
    val2 = 1 #Put 3 sublists of size 1 here that represent the kicker cards
    val3 = 0
    
    for i in range(len(tiedList)):
      self.splitHand(tiedList, tiedList[i].hand, i, val1, val2, val3)
      self.assignSuitVals(tiedList[i].part1_hand)
      self.assignSuitVals(tiedList[i].part2_hand)
    
    self.breakTie_Pair(tiedList, STAGE_PRIMER)
  
  #Pair tiebreaker 
  def breakTie_Pair(self, tiedList, stage):
  
    PART1_HAND_SIZE = 2
    PART2_HAND_SIZE = 3
    
    if stage == 1:
      for i in range(len(tiedList)):
        pairVal = tiedList[i].part1_hand[0].val
        tiedList[i].tiebreakerVal += pairVal
        
      tiedList.sort()
      tiedList.reverse()
    
    tiedSublists = self.breakDownList(tiedList)
    
    for i in range(len(tiedSublists)):
      if len(tiedSublists[i]) > 1:        
        if stage == 2:
          self.convertToSuitsPartial(tiedSublists[i])
         
          for j in range(PART1_HAND_SIZE):
            self.suitTiebreakerPart1Hand(j, tiedSublists[i])
         
        elif stage == 3:
          self.convertToValsPartial(tiedSublists[i])
          
          for j in range(PART2_HAND_SIZE):
            self.valTiebreakerPart2Hand(j, tiedSublists[i])
          
        elif stage == 4:
          self.convertToSuitsPartial(tiedSublists[i])
          
          for j in range(PART2_HAND_SIZE):
            self.suitTiebreakerPart2Hand(j, tiedSublists[i])

        self.breakTie_Pair(tiedSublists[i], stage+1)
        
    updatedList = []
    
    for i in range(len(tiedSublists)):
      for j in range(len(tiedSublists[i])):
        updatedList.append(tiedSublists[i][j])
        
    tiedList[:] = updatedList
  
  #Sets up high card tiebreaker
  def highCard(self, tiedList):
  
    for i in range(len(tiedList)):
      tiedList[i].hand.sort()
      tiedList[i].hand.reverse()
      self.assignSuitVals(tiedList[i].hand)
  
    self.breakTie_HighCard(tiedList, STAGE_PRIMER)
  
  #High card tiebreaker 
  def breakTie_HighCard(self, tiedList, stage):
    
    HAND_SIZE = 5
    
    if stage == 1:
      for i in range(HAND_SIZE):
        self.valTiebreaker(i, tiedList)
        
      tiedList.sort()
      tiedList.reverse()
  
    tiedSublists = self.breakDownList(tiedList)
    
    for i in range(len(tiedSublists)):
      if len(tiedSublists[i]) > 1:
        if stage == 2:
          self.convertToSuits(tiedSublists[i])
          
          for j in range(HAND_SIZE):
            self.suitTiebreaker(j, tiedSublists[i])
      
        self.breakTie_HighCard(tiedSublists[i], stage+1)
      
    updatedList = []
    
    for i in range(len(tiedSublists)):
      for j in range(len(tiedSublists[i])):
        updatedList.append(tiedSublists[i][j])
        
    tiedList[:] = updatedList
  
  #Tells the program to now sort each card by its suit value
  def sortBySuits(self, hand):
  
    for i in range(len(hand)):
      hand[i].sortBySuits = True
  
  #Tells the program to now sort each card by its value     
  def sortByVals(self, hand):
    
    for i in range(len(hand)):
      hand[i].sortBySuits = False
  
  #Gives each card a numerical suit value   
  def assignSuitVals(self, hand):
  
    suitVals = {'D':1, 'C':2, 'H':3, 'S':4}
    
    for i in range(len(hand)):
      hand[i].suitVal = suitVals[hand[i].suit]
  
  #Gives one card a numerical suit value   
  def assignSuitVal(self, card):
  
    suitVals = {'D':1, 'C':2, 'H':3, 'S':4}
    
    card.suitVal = suitVals[card.suit]
  
  #Tells the program to start sorting by suits across the whole hand      
  def convertToSuits(self, updatedList):
  
    tiedSublists = []
    sublist = []
    currVal = updatedList[0].tiebreakerVal
    
    for i in range(len(updatedList)):
      if updatedList[i].tiebreakerVal != currVal:
        tiedSublists.append(sublist)
        currVal = updatedList[i].tiebreakerVal
        sublist = []
        
      sublist.append(updatedList[i])
      
      if (i == len(updatedList) - 1):
        tiedSublists.append(sublist)
      
    for i in range(len(tiedSublists)):
      if len(tiedSublists[i]) > 1:
        for j in range(len(tiedSublists[i])):
          self.sortBySuits(tiedSublists[i][j].hand)
          self.assignSuitVals(tiedSublists[i][j].hand)
          tiedSublists[i][j].hand.sort()
          tiedSublists[i][j].hand.reverse()
    
    updatedList = []
      
    for i in range(len(tiedSublists)):
      for j in range(len(tiedSublists[i])):
        updatedList.append(tiedSublists[i][j])
  
  #Tells the program to start sorting by suits on both partial hands
  def convertToSuitsPartial(self, updatedList):
    
    tiedSublists = self.breakDownList(updatedList)
      
    for i in range(len(tiedSublists)):
      if len(tiedSublists[i]) > 1:
        for j in range(len(tiedSublists[i])):
          self.sortBySuits(tiedSublists[i][j].part1_hand)
          self.sortBySuits(tiedSublists[i][j].part2_hand)
          
          tiedSublists[i][j].part1_hand.sort()
          tiedSublists[i][j].part1_hand.reverse()
          tiedSublists[i][j].part2_hand.sort()
          tiedSublists[i][j].part2_hand.reverse()
          
    updatedList = []
      
    for i in range(len(tiedSublists)):
      for j in range(len(tiedSublists[i])):
        updatedList.append(tiedSublists[i][j]) 
   
  #Tells the program to start sorting by values on both partial hands   
  def convertToValsPartial(self, updatedList):
  
    tiedSublists = self.breakDownList(updatedList)
    
    for i in range(len(tiedSublists)):
      if len(tiedSublists[i]) > 1:
        for j in range(len(tiedSublists[i])):
          self.sortByVals(tiedSublists[i][j].part1_hand)
          self.sortByVals(tiedSublists[i][j].part1_hand)
          
          tiedSublists[i][j].part1_hand.sort()
          tiedSublists[i][j].part1_hand.reverse()
          tiedSublists[i][j].part2_hand.sort()
          tiedSublists[i][j].part2_hand.reverse()
          
    updatedList = []
      
    for i in range(len(tiedSublists)):
      for j in range(len(tiedSublists[i])):
        updatedList.append(tiedSublists[i][j]) 
        
  #Breaks down the entered list into different sublists of hands with equal tiebreaker values
  def breakDownList(self, tiedList):
  
    tiedSublists = []
    sublist = []
    currVal = tiedList[0].tiebreakerVal
    
    for i in range(len(tiedList)):
      if currVal != tiedList[i].tiebreakerVal:
        tiedSublists.append(sublist)
        currVal = tiedList[i].tiebreakerVal
        sublist = []
      
      sublist.append(tiedList[i])
      
      if i == len(tiedList) - 1:
        tiedSublists.append(sublist)
    
    return tiedSublists   
  
  #Breaks down a single hand into sublists of equal card values
  def breakDownHand(self, hand):
  
    cardSublists = []
    sublist = []
    currVal = hand[0].val
    
    for i in range(len(hand)):
      if currVal != hand[i].val:
        cardSublists.append(sublist)
        currVal = hand[i].val
        sublist = []
      
      sublist.append(hand[i])
      
      if i == len(hand) - 1:
        cardSublists.append(sublist)
    
    return cardSublists
  
  #Makes a new list of EqualHand objects  
  def createNewList(self, tiedList, tiedSublists, newList, tiesBroken):
    
    maxSize = len(tiedSublists)
    
    for i in range(maxSize):
      if i == tiedList[i].rank:
        newList.append(tiedList[i])
        maxSize += 1
        
      else:  
        newList.append(tiedSublists[i])
  
  #Checks and see if the hand is 2, 3, 4, 5, Ace     
  def isAceLowStraight(self, hand):
      
    tempList = hand
    tempList.sort()
  
    return (tempList[0].val == 2) and (tempList[1].val == 3) and (tempList[2].val == 4) and (tempList[3].val == 5) and (tempList[4].val == ACE) 
  
  #Retrieves the index of the ace in the hand. The program should only enter this method if there's an Ace in the hand  
  def getAceInd(self, hand):

    for i in range(len(hand)):
      if hand[i].val == ACE:
        return i
      
    print("Incorrectly entered getAceInd.")
    exit(1)
