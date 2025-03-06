from enum import auto, IntEnum


class CardColor(IntEnum):
    """
    Enum class for the color of the card
    """
    RED = 0
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    CRAZY = auto()


class CardLabel(IntEnum):
    """
    Enum class for the value of the card
    """
    ZERO = 0
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    SKIP = auto()
    REVERSE = auto()
    DRAW_TWO = auto()
    CRAZY = auto()
    DRAW_FOUR = auto()


class Card:
    def __init__(self, color: CardColor, label: CardLabel) -> None:
        """
        Constructor for the Card class

        Args:
            color (CardColor): The color of the card
            label (CardLabel): The label of the card

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        self.color = color
        self.label = label

    def __lt__(self, other) -> bool:
        """
        Method to compare two cards' colors and labels

        Args:
            self
            other -> Card: the other card's Card object

        Returns:
            bool: True if self_color and self_label is lower than other_color and other_label, False otherwise

        Complexity:
            O(1)
        """
        return (self.color < other.color) or \
            (self.color == other.color and self.label < other.label)

    def __gt__(self, other) -> bool:
        """
        Method to compare two cards' colors and labels

        Args:
            self
            other -> Card: the other card's Card object

        Returns:
            bool: True if self_color and self_label is higher than other_color and other_label, False otherwise

        Complexity:
            O(1)
        """
        return (self.color > other.color) or \
            (self.color == other.color and self.label > other.label)

    def __ge__(self, other) -> bool:
        """
        Method to compare two cards' colors and labels

        Args:
            self
            other -> Card: the other card's Card object

        Returns:
            bool: True if self_color and self_label is higher than or equal to other_color and other_label, False otherwise

        Complexity:
            O(1)
        """
        return (self.color > other.color) or \
            (self.color == other.color and self.label >= other.label)

    def __str__(self) -> str:
        """
        Method to return a string when print(Card) is called

        Args:
            self

        Returns:
            str: String representation of the cards color and label

        Complexity:
            O(1)
        """
        return self.color.name + " " + self.label.name
