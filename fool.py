#Design a class to represent a playing card and another one to represent a deck of cards. 
#Using these two classes, implement your favorite card game.

import random

class Card():

    cardsPower = {
        "six": 1,
        "seven": 2,
        "eight": 3,
        "nine": 4,
        "ten": 5,
        "jack": 6,
        "maiden": 7,
        "king": 8,
        "ace": 9,
    }

    def __init__(self, kind, suit, isTrump):
        self.kind = kind
        self.suit = suit
        self.isTrump = isTrump

    def isHandEmpty(self, hand):
        handLength = len(hand)
        if not handLength:
            return False

    def takeCardOnHand(self, card, hand):
        hand.append(card)

    def chooseCard(self, hand):
        for pos, card in enumerate(hand, start=0):
            print(f"{pos} {card.kind} {card.suit} {card.isTrump}")

        try:
            cardNum = int(input("Choose card "))
            chosenCard = hand[cardNum]
            print(f"{chosenCard.kind} {chosenCard.suit} {chosenCard.isTrump}")
        
            return hand[cardNum]
        except Exception as e:
            print("Card was not chosen")
            self.chooseCard(Card, hand)

    def playCard(self, attackerCard, defenderCard):
        attackerPower = self.cardsPower.get(attackerCard.kind)
        defenderPower = self.cardsPower.get(defenderCard.kind)
        
        if attackerCard.isTrump:
            if (defenderPower > attackerPower) and defenderCard.isTrump:
                return (attackerCard, defenderCard)
            else:
                return False
        elif defenderCard.isTrump:
            return (attackerCard, defenderCard)
        else:
            if (defenderCard.suit == attackerCard.suit) and \
                (defenderPower > attackerPower):
                    return (attackerCard, defenderCard)
            else:
                return False

    def playRound(self, attackerHand, defenderHand):
        print("ATTACKER\n")
        attackerCard = self.chooseCard(Card, attackerHand)

        print("DEFENDER\n")
        isTaken = str(input("Should you take the attacker card?\n"))
        if isTaken == "y":
            self.takeCardOnHand(Card, attackerCard, defenderHand)
            attackerHand.remove(attackerCard)
            
            if attackerHand:
                Card.playRound(Card, attackerHand, defenderHand)
            else:
                return
        else:
            defenderCard = self.chooseCard(Card, defenderHand)
            returnedCards = self.playCard(Card, attackerCard, defenderCard)
            if returnedCards:
                aCard, dCard = returnedCards
                attackerHand.remove(aCard)
                defenderHand.remove(dCard)
            else:
                print("Defender card was not correct. Round will be repeated\n")
                Card.playRound(Card, attackerHand, defenderHand)

class Deck():
    cardsInDeck = {
        "bubi": ["six", "seven", "eight", "nine", "ten", "jack", "maiden", "king", "ace"],
        "hearts": ["six", "seven", "eight", "nine", "ten", "jack", "maiden", "king", "ace"],
        "crosses": ["six", "seven", "eight", "nine", "ten", "jack", "maiden", "king", "ace"],
        "spades": ["six", "seven", "eight", "nine", "ten", "jack", "maiden", "king", "ace"],
    }

    def __init__(self, cardsInDeck=cardsInDeck):
        self.cardsInDeck = cardsInDeck

    def getTrump(self):
        cardsSuits = [k for k in self.cardsInDeck]
        trump = random.choice(cardsSuits)
        return trump

    def createDeck(self, trump=""):
        if trump:
            self.deck = set()
            for suit, kindList in self.cardsInDeck.items():
                for kind in kindList:
                    if trump == suit:
                        c = Card(kind, suit, True)
                        self.deck.add(c)
                    else:
                        c = Card(kind, suit, False)
                        self.deck.add(c)
        else:
            print("trump is not set")
            exit(1)

    def complementHand(self, deck, hand):
        handLength = len(hand)
        if not deck:
            print("Deck is empty")
        elif handLength < 6:
            print("You have to complement your hand")
            for _ in range(6 - handLength):
                if len(deck) > 0:
                    hand.append(deck.pop())
        else:
            print("Your hand is full")

    def checkEndGame(self, aHand, dHand):
        if not aHand and not dHand:
            return "Draw"
        elif not aHand:
            return "Attacker won"
        elif not dHand:
            return "Defender won"


d = Deck()
d.createDeck(trump=d.getTrump())
cardDeck = d.deck

attackerHand, defenderHand = [], []
for _ in range(6):
    attackerHand.append(cardDeck.pop())
    defenderHand.append(cardDeck.pop())

endGame = ""

while not endGame:
    ###attacker turn
    Card.playRound(Card, attackerHand, defenderHand)
    d.complementHand(cardDeck, attackerHand)
    d.complementHand(cardDeck, defenderHand)
    endGame = d.checkEndGame(attackerHand, defenderHand)
    if endGame:
        break

    ###defender turn
    Card.playRound(Card, defenderHand, attackerHand)
    d.complementHand(cardDeck, defenderHand)
    d.complementHand(cardDeck, attackerHand)
    endGame = d.checkEndGame(attackerHand, defenderHand)

    print(len(cardDeck))

print(endGame)
