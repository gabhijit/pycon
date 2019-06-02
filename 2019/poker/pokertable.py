#
# Copyright (C) 2019 - Abhijit Gadgil. See LICENCE file for further details
#

from pokerhand import PokerHand, MiniPokerHand
from pokerhand import deck
from itertools import combinations

class PokerPlayer:

    def __init__(self):
        self._own_cards = []

    @property
    def own_cards(self):
        return self._own_cards

    def __repr__(self):
        return ":".join(self._own_cards)

class PokerTable:

    def __init__(self, players, deck):
        self._total_players = players
        self._players = [PokerPlayer() for i in range(players)]
        self._community_cards = []
        self._deck = deck
        self._burnt_cards = []
        self._table_ranks = {}
        self._deal_winner = -1
        self._flop_winner = -1
        self._turn_winner = -1
        self._river_winner = -1

    @property
    def players(self):
        return self._players

    def deal(self):
        for i in range(2):
            for player in self._players:
                player._own_cards.append(self._deck.pop())

    def burn_card(self):
        self._burnt_cards.append(self._deck.pop())

    def flop(self):

        self.burn_card()
        for i in range(3):
            self._community_cards.append(self._deck.pop())

    def turn(self):
        self.burn_card()
        self._community_cards.append(self._deck.pop())

    def river(self):
        self.burn_card()
        self._community_cards.append(self._deck.pop())

    @property
    def table_ranks(self):
        return dict(sorted(self._table_ranks.items(),
            key=lambda kv: kv[0]))

    def __repr__(self):

        players = " ".join([str(player) for player in self._players])
        community_cards = ":".join(self._community_cards)

        return " ".join([players, community_cards,
            str(self._deal_winner), str(self._flop_winner),
            str(self._turn_winner), str(self._river_winner),
            str(int(self._deal_winner == self._river_winner)),
            str(int(self._flop_winner == self._river_winner)),
            str(int(self._turn_winner == self._river_winner))
            ])


    def rank_players(self, pre_flop=False):

        player_hands = {}
        if pre_flop:
            for i, player in enumerate(self._players):
                player_hands[i] = MiniPokerHand.from_str( \
                        " ".join(player.own_cards))
        else:
            for i, player in enumerate(self._players):
                possible_hands = []
                for c in combinations(self._community_cards, 3):
                    hand = player.own_cards + list(c)
                    possible_hands.append(PokerHand.from_str(" ".join(hand)))
                player_hands[i] = sorted(possible_hands, reverse=True)[0]

        players = (sorted(player_hands.items(),
            key=lambda kv:kv[1], reverse=True))

        for i in range(len(players)):
            player_id = players[i][0]
            self._table_ranks[i] = player_id

    def run_one_pot(self):

        self.deal()
        self.rank_players(pre_flop=True)
        self._deal_winner = self._table_ranks[0]

        self.flop()
        self.rank_players()
        self._flop_winner = self._table_ranks[0]

        self.turn()
        self.rank_players()
        self._turn_winner = self._table_ranks[0]

        self.river()
        self.rank_players()
        self._river_winner = self._table_ranks[0]

        self._pot_winner = self._river_winner


if __name__ == '__main__':

    for i in range(1000):
        table = PokerTable(5, deck(shuffled=True))
        table.run_one_pot()
        print(table)
