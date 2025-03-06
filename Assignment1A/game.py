from data_structures.referential_array import ArrayR
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList
from player import Player
from card import CardColor, CardLabel, Card
from random_gen import RandomGen
from constants import Constants


class Game:
    """
    Game class to play the game
    """

    def __init__(self) -> None:
        """
        Constructor for the Game class

        Args:
            self

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        self.players = None
        self.draw_pile = None
        self.discard_pile = None
        self.current_player = None
        self.current_color = None
        self.current_label = None

    def generate_cards(self) -> ArrayR[Card]:
        """
        Method to generate the cards for the game

        Args:
            self

        Returns:
            ArrayR[Card]: The array of Card objects generated

        Complexity:
            Best Case Complexity: O(N) - Where N is the number of cards in the deck
            Worst Case Complexity: O(N) - Where N is the number of cards in the deck
        """
        list_of_cards: ArrayR[Card] = ArrayR(Constants.DECK_SIZE)
        idx: int = 0

        for color in CardColor:
            if color != CardColor.CRAZY:
                # Generate 4 sets of cards from 0 to 9 for each color
                for i in range(10):
                    list_of_cards[idx] = Card(color, CardLabel(i))
                    idx += 1
                    list_of_cards[idx] = Card(color, CardLabel(i))
                    idx += 1

                # Generate 2 of each special card for each color
                for i in range(2):
                    list_of_cards[idx] = Card(color, CardLabel.SKIP)
                    idx += 1
                    list_of_cards[idx] = Card(color, CardLabel.REVERSE)
                    idx += 1
                    list_of_cards[idx] = Card(color, CardLabel.DRAW_TWO)
                    idx += 1
            else:
                # Generate the crazy and crazy draw 4 cards
                for i in range(4):
                    list_of_cards[idx] = Card(CardColor.CRAZY, CardLabel.CRAZY)
                    idx += 1
                    list_of_cards[idx] = Card(CardColor.CRAZY, CardLabel.DRAW_FOUR)
                    idx += 1

                # Randomly shuffle the cards
                RandomGen.random_shuffle(list_of_cards)

                return list_of_cards

    def initialise_game(self, players: ArrayR[Player]) -> None:
        """
        Method to initialise the game

        Args:
            self
            players (ArrayR[Player]): The array of players

        Returns:
            None

        Complexity:
            Best Case Complexity:   O(n + p * log(p)) where n is the number of cards and p is the number of players
            Worst Case Complexity:  O(n + p * log(p)) where n is the number of cards and p is the number of players
        """

        # Initialize an iterator to avoid creating a new array each time a card is transferred
        index_iterator = 0
        self.players = ArraySortedList(len(players))

        # Add players to the sorted list. A sorted list is used to simplify the play_reverse() method,
        # though it makes the next_player() method less straightforward.
        for player in players:
            self.players.add(player)

        # Generate the cards for the game
        generated_cards = self.generate_cards()

        # Distribute cards to players. Use index_iterator to ensure each player receives cards in sequence.
        for card_num in range(Constants.NUM_CARDS_AT_INIT):
            for player in self.players:
                card = generated_cards[index_iterator]
                player.add_card(card)
                index_iterator += 1

        # Initialize the draw pile as a stack, as we only need to access the top of the deck.
        self.draw_pile = ArrayStack(len(generated_cards))

        # Add the remaining cards to the draw pile
        for card in generated_cards[index_iterator:]:
            self.draw_pile.push(card)

        # Initialize discard pile and place the top card from the draw pile onto it.
        self.discard_pile = ArrayStack(Constants.DECK_SIZE)
        self.discard_pile.push(self.draw_pile.peek())
        self.draw_pile.pop()

        # Ensure the top card of the discard pile is a number card (label < 10).
        # If the top card is special, draw additional cards from the draw pile until a valid top card is found.
        while True:
            if self.discard_pile.peek().label < 10:
                break
            else:
                self.discard_pile.push(self.draw_pile.peek())
                self.draw_pile.pop()

        # Set the current color and label based on the top card of the discard pile
        self.current_color = self.discard_pile.peek().color
        self.current_label = self.discard_pile.peek().label

    def crazy_play(self, card: Card) -> None:
        """
        Method to play a crazy card

        Args:
            self
            card (Card): The card to be played

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(n + p) where n is the number of cards in the hand and p is the number of players
        """
        # Check if the played card is a "DRAW_FOUR" card
        if card.label.name == "DRAW_FOUR":
            # Identify the next player in sequence
            next_player = self.next_player()

            # Draw four cards for the next player
            for _ in range(4):
                self.draw_card(next_player, False)

            # Skip the turn of the next player
            self.play_skip()

        # Set the current color to a random value from CardColor
        self.current_color = CardColor(RandomGen.randint(0, 3))

        # Reset the current label to None, as you can only play a certain color onto the crazy card
        self.current_label = None

        return None

    def play_reverse(self) -> None:
        """
        Method to play a reverse card

        Args:
            self

        Returns:
            None

        Complexity:
            Best Case Complexity: O(p) where p is the number of players
            Worst Case Complexity: O(p) where p is the number of players
        """
        # Iterate through each player in the sorted list
        for player in self.players:
            # Update the player's position to reflect the reverse of the order
            # The new position is calculated by reversing the current position
            # Formula: (current_position - (total_players - 1)) * -1
            # e.g. current_pos = 0, total_players = 5  ||  (0 - (5-1)) * -1 = 4, and 4 is the last position
            player.position = (player.position - ((len(self.players)) - 1)) * -1

        return None

    def play_skip(self) -> None:
        """
        Method to play a skip card

        Args:
            self

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(p) where p is the number of players
        """
        # Determine the next player in the sequence, this is accounted for in play_game()
        self.current_player = self.next_player()

        # No return value needed, method only updates the state
        return None

    def draw_card(self, player: Player, playing: bool) -> Card | None:
        """
        Method to draw a card from the deck

        Args:
            self
            player (Player): The player who is drawing the card
            playing (bool): A boolean indicating if the player is able to play the card

        Returns:
            Card - When drawing a playable card, other return None

        Complexity:
            Best Case Complexity: O(log n) where n is the number of cards in the hand
            Worst Case Complexity: O(n) where n is the number of cards in the hand
        """
        # get the top card from the draw pile
        card = self.draw_pile.peek()

        # Remove the top card from the draw pile
        self.draw_pile.pop()

        # Check if the drawn card matches the current game conditions
        # Conditions: card color matches current color, or card label matches current label, or card is a "CRAZY" card
        # Also, ensure that the player is allowed to play (playing == True) (meaning it is not from a draw 2 or 4)
        if (((self.current_color == card.color) or (self.current_label == card.label) or (card.color.name == "CRAZY"))
                and playing is True):
            # If conditions are met, return the drawn card
            return card
        else:
            # If conditions are not met, add the card to the player's hand
            player.hand.add(card)
            # Return None indicating that the card is not playable
            return None

    def next_player(self) -> Player:
        """
        Method to get the next player

        Args:
            self

        Returns:
            Player: The next player

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(p) where p is the number of players
        """
        # Check if the current player is not set
        if self.current_player is None:
            # If no current player, loop through players to find the one with position 0
            for player in self.players:
                if player.position == 0:
                    return player  # Return the player with position 0 as the next player
        else:
            # Calculate the next position using modulo to wrap around the list of players
            next_position = (self.current_player.position + 1) % len(self.players)
            # Loop through players to find the one with the calculated next position
            for player in self.players:
                if player.position == next_position:
                    return player  # Return the player with the next position as the next player

    def play_game(self) -> Player:
        """
        Method to play the game

        Args:

        Returns:
            Player: The winner of the game

        Complexity:
            Best Case Complexity: O(h + n + p) where 'p' is the number of players, 'h' is the number of cards in
                the current player's hand, 'n' is the number of cards in the draw_pile

            Worst Case Complexity: O(k * (h + p + n)) where 'p' is the number of players, 'h' is the number of cards in
                the current player's hand, 'n' is the number of cards in the draw_pile, and 'k' is the number of
                iterations that the while loop executes until the winner is decided
        """
        winner = None

        def special_card_play(card: Card) -> None:
            """
            Method to play any non-number card, implemented so there is no duplicate code

            Args:
                card (Card): The card to be played

            Returns:
                None

            Complexity:
                Best Case Complexity: O(1)
                Worst Case Complexity: O(n + p) where n is the number of cards in hand and p is the number of players
            """
            if card.label.name == "REVERSE":
                self.play_reverse()  # Call play_reverse to reverse the turn order

            # Check if the card label is "SKIP"
            elif card.label.name == "SKIP":
                self.play_skip()  # Call play_skip to skip the next player's turn

            # Check if the card color is "CRAZY"
            elif card.color.name == "CRAZY":
                self.crazy_play(card)  # Call crazy_play to handle the effects of a crazy card

            # Check if the card label is "DRAW_TWO"
            elif card.label.name == "DRAW_TWO":
                next_player = self.next_player()  # Determine the next player
                for _ in range(2):
                    self.draw_card(next_player, False)  # Make the next player draw two cards
                self.play_skip()  # Skip the next player's turn after they draw two cards

            return None  # Return None at the end of the function

        def shuffle_pile():
            """
            Method to shuffle the discard pile, and add the cards to the draw pile

            Args:

            Returns:
                None

            Complexity:
                Best Case Complexity: O(n) where n is the number of cards in the discard pile
                Worst Case Complexity: O(n) where n is the number of cards in the discard pile
            """
            # Peek at the top card of the discard pile and store it
            top_of_discard_pile = self.discard_pile.peek()
            self.discard_pile.pop()  # Remove the top card from the discard pile

            # Create a list to hold the remaining cards in the discard pile
            discard_pile_shuffle = ArrayR(Constants.DECK_SIZE)

            # Iterate over the discard pile and move all cards to the shuffle list
            for idx in range(len(self.discard_pile)):
                card = self.discard_pile.peek()  # Peek at the top card of the discard pile
                self.discard_pile.pop()  # Remove the top card from the discard pile
                discard_pile_shuffle[idx] = card  # Add the card to the shuffle list

            # Randomly shuffle the cards in the discard pile
            RandomGen.random_shuffle(discard_pile_shuffle)

            # Push the shuffled cards back onto the draw pile
            for card in discard_pile_shuffle:
                self.draw_pile.push(card)

            # Push the original top card back onto the discard pile
            self.discard_pile.push(top_of_discard_pile)

            # Return None to conclude the function
            return None

        while True:
            # Check if the draw pile is empty and shuffle the discard pile back into the draw pile if needed
            if len(self.draw_pile) == 0:
                shuffle_pile()

            card_played = False  # Flag to check if a card has been played in this turn
            self.current_player = self.next_player()  # Get the next player in the game

            # Loop through the current player's hand to find a playable card
            for card in range(len(self.current_player.hand)):
                if ((self.current_color == self.current_player.hand[card].color)
                        or (self.current_label == self.current_player.hand[card].label)
                        or (self.current_player.hand[card].color.name == "CRAZY")):
                    card_played = True  # Mark that a card has been played
                    card_object = self.current_player.play_card(card)  # Play the selected card

                    # Check if the current player has no cards left and declare them as the winner
                    if len(self.current_player.hand) == 0:
                        winner = self.current_player

                    # Add the played card to the discard pile and update the current color and label
                    self.discard_pile.push(card_object)
                    self.current_color, self.current_label = card_object.color, card_object.label

                    # Handle any special actions associated with the played card
                    special_card_play(card_object)
                    break  # Exit the loop after playing a card

            # If no card was played, the player draws a card
            if card_played is False:
                card = self.draw_card(self.current_player, True)
                if card is not None:
                    # Add the drawn card to the discard pile and update the current color and label
                    self.discard_pile.push(card)
                    self.current_color, self.current_label = card.color, card.label
                    # Handle any special actions associated with the drawn card
                    special_card_play(card)

            # If there's a winner, return the winner and end the game
            if winner is not None:
                return winner


def test_case():
    players: ArrayR[Player] = ArrayR(4)
    players[0] = Player("Alice", 0)
    players[1] = Player("Bob", 1)
    players[2] = Player("Charlie", 2)
    players[3] = Player("David", 3)
    g: Game = Game()
    g.initialise_game(players)
    winner: Player = g.play_game()
    print(f"Winner is {winner.name}")


if __name__ == '__main__':
    test_case()
