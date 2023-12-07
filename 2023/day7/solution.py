from typing import List
from lib.parse import parse_strings
from enum import Enum
from collections import defaultdict

NON_JOKER_CARDS = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

CARD_RANKS = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
}

def get_card_rank(card: str, wild_enabled: bool = False) -> int:
    if card == "J":
        if wild_enabled:
            return 1
        else:
            return CARD_RANKS["J"]
    elif card in CARD_RANKS:
        return CARD_RANKS[card]
    else:
        return int(card)

class HandType(Enum):
    FIVE_OF_KIND = 7
    FOUR_OF_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1
    UNSET = 0

def get_hand_type(cards: List[str]) -> HandType:
    counts = defaultdict(int)
    for c in cards:
        counts[c] += 1

    freqs = sorted(counts.values())
    if len(counts.keys()) == 1:
        return HandType.FIVE_OF_KIND
    elif len(counts.keys()) == 2:
        
        if freqs == [1, 4]:
            return HandType.FOUR_OF_KIND
        elif freqs == [2, 3]:
            return HandType.FULL_HOUSE
        else:
            raise Exception(f"unknown hand: {cards}")
    elif len(counts.keys()) == 3:
        if freqs == [1, 1, 3]:
            return HandType.THREE_OF_KIND
        elif freqs == [1, 2, 2]:
            return HandType.TWO_PAIR
        else:
            raise Exception(f"unknown hand: {cards}")
    elif len(counts.keys()) == 5:
        return HandType.HIGH_CARD
    else:
        return HandType.ONE_PAIR

def get_wild_hand_type(cards: List[str]) -> HandType:
    counts = defaultdict(int)
    for c in cards:
        counts[c] += 1
    if "J" not in counts or counts["J"] <= 0:
        return get_hand_type(cards)
    
    best = HandType.UNSET
    for c in NON_JOKER_CARDS:
        replaced = False
        next_cards = []
        for new in cards:
            if new == "J" and not replaced:
                replaced = True
                next_cards.append(c)
            else:
                next_cards.append(new)

        temp = get_wild_hand_type(cards=next_cards)
        if temp.value > best.value:
            best = temp
    
    return best


class Hand:

    def __init__(self, cards: List[str], bid: int, wild_enabled: bool = False) -> None:
        self.cards = cards
        self.bid = bid
        self.wild_enabled = wild_enabled
        self.type = get_hand_type(cards) if not wild_enabled else get_wild_hand_type(cards)

    def beats(self, opponent: 'Hand') -> bool:
        if self.type.value > opponent.type.value:
            return True
        elif self.type.value == opponent.type.value:
            for i in range(0, 5):
                my_card = get_card_rank(self.cards[i], self.wild_enabled)
                their_card = get_card_rank(opponent.cards[i], opponent.wild_enabled)
                if my_card > their_card:
                    return True
                elif their_card > my_card:
                    return False
        else:
            return False
        
        raise Exception(f"Hands are equal: {''.join(self.cards)} vs. {''.join(opponent.cards)}")

    def print(self) -> None:
        print(f"{''.join(self.cards)}: {self.type}")

def merge_sort(hands: List[Hand]) -> List[Hand]:
    if len(hands) <= 1:
        return hands
    
    mid = len(hands) // 2
    left_hands, right_hands = [], []
    for i in range(len(hands)):
        if i < mid:
            left_hands.append(hands[i])
        else:
            right_hands.append(hands[i])
    
    left, right = merge_sort(left_hands), merge_sort(right_hands)
    res = []

    while left and right:
        if left[0].beats(right[0]):
            res.append(left.pop(0))
        else:
            res.append(right.pop(0))
    
    while left:
        res.append(left.pop(0))
    while right:
        res.append(right.pop(0))
    
    return res

def get_hands_sum(wild_enabled: bool) -> int:
    game_states = parse_strings("2023/day7/input.txt")
    hands = []
    for g in game_states:
        raw_game = g.split(" ")
        hands.append(Hand(cards=raw_game[0], bid=int(raw_game[1]), wild_enabled=wild_enabled))

    hands = merge_sort(hands)
    res = 0
    rank = len(hands)
    for h in hands:
        res += rank * h.bid
        rank -= 1

    return res        

print(get_hands_sum(wild_enabled=False))
print(get_hands_sum(wild_enabled=True))
