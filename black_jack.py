"""BlackJack game by Kulyk Zorian."""
import random
from random import randint
from itertools import combinations

# default balance
balance = 5000
# deck and length of the deck
deck, deck_length = [], 52
player_cards, dealer_cards = [], []

# first dealer card hidden and result of counting points of players
backside, result = True, False

# conditions for continuation of possibility "stand" or "double"
stand_counter, double = 0, True

# dealer and player points
dealer_value, player_value = 0, 0

game = "start"


def reset():
    """Reset all game changes"""
    global player_cards, dealer_cards, backside, double, deck, \
        deck_length, stand_counter, balance
    deck, deck_length = [], 52
    player_cards, dealer_cards = [], []
    backside, double = True, True
    stand_counter = 0


def get_deck():
    """Return a list of (rank, suit) tuples for all 52 cards."""
    global deck
    for suit in ("♥", "♦", "♠", "♣"):
        for rank in range(2, 11):
            deck.append((str(rank), suit))  # Add the numbered cards.
        for rank in ("J", "Q", "K", "A"):
            deck.append((rank, suit))  # Add the face and ace cards.
    random.shuffle(deck)


def card_interpretation(player):
    """Get player's list of current cards.
       Return list of strings for cards interpretation"""
    global backside
    interpretations = []
    strings = 3
    for card in player:
        if backside:
            rank, suit = "#", "#"
            backside = 0
        else:
            rank, suit = card[0], card[1]

        if rank == "10":
            suit += " "

        card_as_string = [f"|{rank}‾‾| ", f"| {suit} | ", f"|__{rank}| "]
        interpretations.extend(card_as_string)

    inter_length = len(interpretations)

    for index in range(strings):
        for string in range(index, inter_length):
            if (string - index) % 3 == 0 and string != index:
                interpretations[index] += interpretations[string]

    return interpretations[:strings]


def get_card(player):
    """Get player's list of current cards and add one"""
    global deck, deck_length
    if len(deck) == 0:
        get_deck()
        deck_length = 52
    card = randint(0, deck_length - 1)
    deck_length -= 1
    player.append(deck[card])
    deck.pop(card)
    return player


def card_value():
    """Return dictionary with cards values"""
    value_dict = dict()
    for value in range(2, 11):
        value_dict[str(value)] = value
    for value in ("J", "Q", "K"):
        value_dict[value] = 10
    value_dict["A"] = [1, 11]
    return value_dict


def count_points(player):
    """Get player's list of current cards.
        Return player's value of points sum"""
    p_points, ace_counter = [], 0
    value_dict = card_value()
    ace_values = []
    for card in player:
        if card[0] == "A":
            ace_counter += 1
        else:
            p_points.append(value_dict[card[0]])
    no_ace = sum(p_points)

    p_points = []
    for value in range(ace_counter):
        ace_values.extend(value_dict["A"])

    for ace_combination in combinations(ace_values, ace_counter):
        points = no_ace + sum(ace_combination)
        if points not in p_points:
            p_points.append(points)

    return p_points


def print_cards_points(cards1, cards2, points1, points2):
    """Get players' lists of current card and points.
        Print points and cards of players"""
    print(f"Dealer: {points1}")
    dealer_cards_reflection = card_interpretation(cards1)
    for string in dealer_cards_reflection:
        print(string)
    print(f"Player: {points2}")
    player_cards_reflection = card_interpretation(cards2)
    for string in player_cards_reflection:
        print(string)


def start():
    """Return first hand for two players"""
    player, dealer = [], []
    initial_hand = 2
    for generate_card in range(initial_hand):
        player = get_card(player)
        dealer = get_card(dealer)
    return dealer, player


def max_value(player):
    """Get player's list of current cards.
        Return max points of player"""
    points = max(player)
    player.remove(points)
    if points > 21 and len(player) != 0:
        return max(player)
    return points


get_deck()

while True:
    """Outside cycle of the game. Stage before active game."""

    if game == "start":
        print(f"How much do you bet? (1-{balance})\n-->")

    try:
        bet = int(input())
    except ValueError:
        print("-->")
        continue
    else:
        if bet > balance or bet < 1:
            print("-->")
            continue
        else:
            # initial hand
            print(f"Bet: {bet}")
            dealer_cards, player_cards = start()

    player_points = count_points(player_cards)

    # hide dealer points if first hand
    if backside:
        dealer_points = "???"
    else:
        dealer_points = count_points(dealer_cards)

    print_cards_points(dealer_cards, player_cards, dealer_points, player_points)

    while True:
        """Inner cycle of the game. Active game."""

        print("Hit, Stand, Double down (press h, s or d)")
        move = input()
        dealer_value, player_value = max_value(count_points(dealer_cards)),\
            max_value(count_points(player_cards))

        if move == "h":
            """Hit action"""
            if dealer_value < 17:
                dealer_cards = get_card(dealer_cards)
            else:
                if dealer_value <= player_value:
                    stand_counter += 1
            player_cards = get_card(player_cards)
        elif move == "s":
            """Stand action"""
            if stand_counter != 2:
                if dealer_value < 17:
                    dealer_cards = get_card(dealer_cards)
                dealer_value = max_value(count_points(dealer_cards))
                if player_value >= dealer_value >= 17:
                    stand_counter = 2
                elif dealer_value >= 17:
                    stand_counter += 1

        elif move == "d" and double:
            """Double action"""
            if bet * 2 > balance:
                continue
            else:
                bet *= 2
                print(f"Bet: {bet}")
        else:
            continue

        """Count points and print players' cards."""
        dealer_points, player_points = count_points(dealer_cards), \
            count_points(player_cards)

        print_cards_points(dealer_cards, player_cards, dealer_points, player_points)

        dealer_value, player_value = max_value(dealer_points), max_value(player_points)

        """Check results."""
        if dealer_value <= 21 and player_value <= 21 and stand_counter != 2:
            double = False
            continue
        elif dealer_value > 21 or dealer_value < player_value <= 21:
            result = True
        elif player_value > 21 or player_value < dealer_value <= 21:
            result = False
        elif dealer_value == player_value:
            result = 2

        """State results."""
        if result == 2:
            print("Draw!")
            print(f"Your balance {balance}")
        elif result:
            print("You win! Congratulations.")
            balance += bet
            print(f"Your balance {balance}")
        elif not result:
            print("You lose! Luck next time.")
            balance -= bet
            print(f"Your balance {balance}")
        else:
            continue

        break

    if balance == 0:
        print("Sorry, but you are bankrupt. Thanks for playing!")
        balance = 5000

    game = input("Do you wanna continue? (yes | no)\n-->")
    if game == "yes":
        game = "start"
        reset()
        get_deck()
        continue
    else:
        print("Thanks for playing!")
        print("Game was created by Kulyk Zorian.")
        break
