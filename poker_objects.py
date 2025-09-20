#Card classs
class Card:
    val = None
    suit = None
    name = None
    suitVal = None
    sortBySuits = False

    def __lt__(card1, card2):
      
      if card1.sortBySuits and card2.sortBySuits:
        return card1.suitVal < card2.suitVal
        
      return card1.val < card2.val
      
    def __repr__(c):
      
      return c.name

#Default Hand object class
class Hand:
    hand = []
    handVal = None
    removedCard = None

    def __lt__(hand1, hand2):
        return hand1.handVal < hand2.handVal
    
    def __repr__(h):
        text = ""

        for i in range(len(h.hand)):
            text += h.hand[i].name + " "

        return text

#Object specifically designed for breaking hand ties
class EqualHand:
  
  def __init__(self):
    self.tiebreakerVal = 0
    self.handVal = None
    self.hand = []
    self.part1_hand = []
    self.part2_hand = []
    self.kicker = None
    self.removedCard = None
    
  def __lt__(hand1, hand2):
  
    return hand1.tiebreakerVal < hand2.tiebreakerVal
    
  def __repr__(h):
    
    text = ""

    for i in range(len(h.hand)):
      text += h.hand[i].name + " "

    return text
