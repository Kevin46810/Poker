#Card classs
class Card:
    sortBySuits = False

    def __init__(self, val, suit, name):
      self.val = val
      self.suit = suit
      self.name = name
      self.suitVal = 0

    def __lt__(self, other):
      
      if self.sortBySuits and other.sortBySuits:
        return self.suitVal < other.suitVal
        
      return self.val < other.val
      
    def __repr__(c):
      
      return c.name

#Default Hand object class
class Hand:
    breakingTies = False

    def __init__(self, hand, handVal, removedCard):
      self.hand = hand
      self.handVal = handVal
      self.removedCard = removedCard
      self.tiebreakerVal = 0

    def __lt__(self, other):
        if self.breakingTies:
          return self.tiebreakerVal < other.tiebreakerVal

        return self.handVal < other.handVal
    
    def __repr__(h):
        text = ""

        for i in range(len(h.hand)):
            text += h.hand[i].name + " "

        return text
