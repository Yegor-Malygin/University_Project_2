from card import Card
from constants import Constants
from data_structures.array_sorted_list import ArraySortedList

class Player:
    """
    Player class to store the player details
    """
    def __init__(self, name: str, position: int) -> None:

        """
        Constructor for the Player class

        Args:
            name (str): The name of the player
            position (int): The position of the player

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        self.name = name
        self.position = position
        self.hand = ArraySortedList(Constants.NUM_MAX_VALS)

    def add_card(self, card: Card) -> None:
        """
        Method to add a card to the player's hand

        Args:
            card (Card): The card to be added to the player's hand

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        self.hand.add(card)

        return None

    def play_card(self, index: int) -> Card:
        """
        Method to play a card from the player's hand

        Args:
            index (int): The index of the card to be played

        Returns:
            Card: The card at the given index from the player's hand

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        card = self.hand[index]
        self.hand.delete_at_index(index)
        return card

    def __len__(self) -> int:
        """
        Method to get the number of cards in the player's hand

        Args:
            self

        Returns:
            int: The number of cards in the player's hand

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """

        return len(self.hand)

    def __getitem__(self, index: int) -> Card:
        """
        Method to get the card at the given index from the player's hand

        Args:
            index (int): The index of the card to be fetched

        Returns:
            Card: The card at the given index from the player's hand

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        card = self.hand[index]
        return card

    def __lt__(self, other) -> bool:
        """
        Method to compare two player's positions

        Args:
            self
            other -> Player: the other player's Player object

        Returns:
            bool: True if self_position is lower than other_position, False otherwise

        Complexity:
            O(1)
        """
        return self.position < other.position

    def __gt__(self, other) -> bool:
        """
        Method to compare two player's positions

        Args:
            self
            other -> Player: the other player's Player object

        Returns:
            bool: True if self_position is higher than other_position, False otherwise

        Complexity:
            O(1)
        """
        return self.position > other.position

    def __le__(self, other) -> bool:
        """
        Method to compare two player's positions

        Args:
            self
            other -> Player: the other player's Player object

        Returns:
            bool: True if self_position is lower than or equal to other_position, False otherwise

        Complexity:
            O(1)
        """
        return self.position <= other.position

    def __str__(self) -> str:
        """
        Method to return a string when print(Player) is called

        Args:
            self

        Returns:
            str: String representation of the players name and position

        Complexity:
            O(1)
        """
        return self.name + " " + str(self.position)
