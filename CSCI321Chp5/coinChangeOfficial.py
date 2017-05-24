import sys

"""
Implementation of book algorithm with O(money) storage (10 minutes)
"""

def dp_change(money, coins):
    """Determine miniumum number of coins to make change

    Uses a dynamic programming algorithm with O(money * len(coins)) time
    complexity, and O(money) space complexity

    Args:
        money: Integer amount to make change for
        coins: Sequence of integer coin denominations

    Returns: Integer number of coins, or sys.maxsize, if change can't be made
    """
    min_num_coins = [sys.maxsize] * (money + 1)
    min_num_coins[0] = 0   # Base case
    for m in range(1, money + 1):
        for coin in coins:
            if m >= coin:
                num_coins = min_num_coins[m - coin] + 1  # Recursive case
                if num_coins < min_num_coins[m]:
                    min_num_coins[m] = num_coins
    return min_num_coins[money]

# http://stackoverflow.com/questions/4151320/efficient-circular-buffer
class CircularBuffer:
    """Simple circular buffer

    Attributes:
        size: The integer size for the buffer
    """
    def __init__(self, size):
        self.size = size
        self.data = []
        self.index = 0

    def append(self, value):
        """Append value to circular buffer"""
        if len(self.data) < self.size:
            self.data.append(value)
        else:
            self.data[self.index] = value
        self.index = (self.index + 1) % self.size

    def __getitem__(self, relative_index):
        """Get item at relative_index from current head of buffer"""
        if len(self.data) < self.size:
            return self.data[relative_index]
        else:
            return self.data[(self.index + relative_index) % self.size]

    def __repr__(self):
        """Return string representation"""
        return self.data.__repr__()

"""
Solves "Stop and Think" on page 241
"""

def dp_change2(money, coins):
    """Determine miniumum number of coins to make change

    Uses a dynamic programming algorithm with O(money * len(coins)) time
    complexity, and O(max(coins)) space complexity

    Args:
        money: Integer amount to make change for
        coins: Sequence of integer coin denominations

    Returns: Integer number of coins, or sys.maxsize, if change can't be made
    """
    min_num_coins = CircularBuffer(max(coins))
    min_num_coins.append(0)   # Base case
    for m in range(1, money + 1):
        min_coins = sys.maxsize
        for coin in coins:
            if m >= coin:
                num_coins = min_num_coins[-coin] + 1  # Recursive case
                if num_coins < min_coins:
                    min_coins = num_coins
        min_num_coins.append(min_coins)
    return min_num_coins[-1]


if __name__ == "__main__":
    with open(sys.argv[1], "r") as file:
        money = int(file.readline())
        coins = [int(c) for c in file.readline().split(',')]
        print(dp_change2(money, coins))
