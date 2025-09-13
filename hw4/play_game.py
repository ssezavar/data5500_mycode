# Sara Sezavar Dokhtfaroughi -- A02422030 -- DATA6500 -- Fall 2025
# HW4
# play_game.py

from DeckOfCards import *

# calculate the total score of a hand (treating Aces as 1 or 11)
def hand_score(cards):
    total = sum(c.val for c in cards)
    aces = sum(1 for c in cards if c.face == "Ace")
    # reduce total by 10 for each Ace if score goes over 21
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

# print all user cards with numbering
def print_user_cards(cards):
    for i, c in enumerate(cards, 1):
        print(f"Card number {i} is: {c.face} of {c.suit}")

# print dealer's first two cards only
def print_dealer_first_two(cards):
    print(f"Dealer card number 1 is: {cards[0].face} of {cards[0].suit}")
    print(f"Dealer card number 2 is: {cards[1].face} of {cards[1].suit}")

# play a single round of Blackjack
def play_round(deck: DeckOfCards):
    # print deck before and after shuffling (required by assignment)
    print("\ndeck before shuffled:")
    deck.print_deck()

    deck.shuffle_deck()
    print("\ndeck after shuffled:")
    deck.print_deck()

    # deal two cards to the user
    user_cards = [deck.get_card(), deck.get_card()]
    print()
    print_user_cards(user_cards)
    user_total = hand_score(user_cards)
    print(f"\nYour total score is: {user_total}")

    # let the user hit until they stand or bust
    while user_total <= 21:
        hit = input("Would you like a hit?(y/n) ").strip().lower()
        if hit != "y":
            break
        new_c = deck.get_card()
        user_cards.append(new_c)
        print(f"\nCard number {len(user_cards)} is: {new_c.face} of {new_c.suit}")
        user_total = hand_score(user_cards)
        print(f"Your total score is: {user_total}")

    if user_total > 21:
        print("\nYou busted, you lose!")
        return

    # dealer’s turn: hit until reaching at least 17
    dealer_cards = [deck.get_card(), deck.get_card()]
    print()
    print_dealer_first_two(dealer_cards)

    dealer_total = hand_score(dealer_cards)
    while dealer_total < 17:
        new_c = deck.get_card()
        dealer_cards.append(new_c)
        print(f"\nDealer hits, card number {len(dealer_cards)} is: {new_c.face} of {new_c.suit}")
        dealer_total = hand_score(dealer_cards)

    print(f"\nDealer score is: {dealer_total}")

    # determine the winner
    if dealer_total > 21 and user_total <= 21:
        print("\nDealer Busted, you win!!!")
    elif user_total <= 21 and user_total > dealer_total:
        print("\nYour score is higher, you win!")
    else:
        if dealer_total == user_total:
            print("\nDealer score is equal or higher, you lose!")
        else:
            print("\nDealer score is higher, you lose!")

# entry point of the program
def main():
    print("Welcome to Black Jack!")
    deck = DeckOfCards()

    # loop until user chooses not to play another game
    while True:
        play_round(deck)
        again = input("\nanother game?(y/n): ").strip().lower()
        if again != "y":
            break

# run the game
if __name__ == "__main__":
    main()
