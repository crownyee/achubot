import random

# 生成一副牌
def generate_deck():
    card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    card_suits = ['♥', '♠', '♣', '♦']
    deck = [(i, j) for i in card_values for j in card_suits]
    random.shuffle(deck)
    return deck

# 計算手牌分數
def calculate_score(hand):
    score = 0
    aces = 0
    for card in hand:
        if card[0] in ['J', 'Q', 'K']:
            score += 10
        elif card[0] == 'A':
            aces += 1
            score += 11
        else:
            score += int(card[0])
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

# 主體
def blackjack():
    deck = generate_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    
    while True:
        print("玩家的手牌 :", player_hand, "點數為: ", calculate_score(player_hand))
        print("莊家的手牌:", dealer_hand,  "點數為: ", calculate_score(dealer_hand))
        if calculate_score(player_hand) > 21:
            print("你爆了!")
            return

        action = input("是否繼續加牌 ? (Y/N)")
        if action.lower() == "y":
            player_hand.append(deck.pop())

        elif action.lower() == "n":
            if calculate_score(dealer_hand) > calculate_score(player_hand):
                print("莊家的手牌: ", dealer_hand, "點數為: ", calculate_score(dealer_hand))
                print("你輸了")
                return
            else:
                while calculate_score(dealer_hand) < 18:
                    dealer_hand.append(deck.pop())

            print("莊家的手牌: ", dealer_hand, "點數為: ", calculate_score(dealer_hand))
            if calculate_score(dealer_hand) > 21 or calculate_score(player_hand) > calculate_score(dealer_hand):
                print("你贏了")
            else:
                print("你輸了")
            return
        
        
blackjack()