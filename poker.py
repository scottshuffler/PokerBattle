from __future__ import division
from deuces import Deck, Evaluator
player1_score_count = 0
player2_score_count = 0
tie_score_count = 0
import datetime
from random import choice
from math import log, sqrt

# Monte is player 1
# Simple is player 2

class Board(object):
    def start(self):
        #     P1H,P2H,P1M, P2M, POT, TABLE, BB, SB, CP, LA
        state = [[],[],998, 999, 3, [], 1, 2, 1, ""]

    def current_player(self, state):
        return state[8]

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        state_copy = state[:]
        state_history.append(state_copy)

        if play in ("R", "CH", "CA", "F", "P"):
            cp = current_player(state)
            if play ==  "P":
                pass
            elif play == "R" and state[cp + 1] != 0:
                old_money = state[cp+1]
                new_money = max(old_money - 1, old_money - 2)
                state[cp+1] -= new_money
                state[4] += old_money - new_money
            elif play == "CH":
                pass
            elif play == "CA":
                pass
            else:
                pass


    def legal_plays(self, state_history):
        cp = state_history[-1][8] ^ 3
        if state_history[-1][cp + 1] == 0:
            return ["P"]
        if state_history[-1][9] == "R":
            return ["R", "CA", "F"]
        elif state_history[-1][9] == "CH":
            return ["R", "CA", "CH", "F"]
        elif state_history[-1][9] == "CA":
            return ["R", "CA", "CH", "F"]
        else:
            return []

    def winner(self, state_history):

        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        pass

class MonteCarlo(object):
    def __init__(self, board, **kwargs):
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        self.board = board
        self.states = []
        seconds = kwargs.get('time', 30)
        self.calculation_time = datetime.timedelta(seconds=seconds)
        self.max_moves = kwargs.get('max_moves', 100)
        self.C = kwargs.get('C', 1.4)
        self.wins = {}
        self.plays = {}

    def update(self, state):
        # Takes a game state, and appends it to the history.
        self.states.append(state)
        pass

    def get_play(self):
        self.max_depth = 0
        state = self.states[-1]
        player = self.board.current_player(state)
        legal = self.board.legal_plays(self.states[:])

        # Bail out early if there is no real choice to be made.
        if not legal:
            return
        if len(legal) == 1:
            return legal[0]

        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
            games += 1

        moves_states = [(p, self.board.next_state(state, p)) for p in legal]

        # Display the number of calls of `run_simulation` and the
        # time elapsed.
        print games, datetime.datetime.utcnow() - begin

        # Pick the move with the highest percentage of wins.
        percent_wins, move = max(
            (self.wins.get((player, S), 0) /
             self.plays.get((player, S), 1),
             p)
            for p, S in moves_states
        )

        # Display the stats for each possible play.
        for x in sorted(
            ((100 * self.wins.get((player, S), 0) /
              self.plays.get((player, S), 1),
              self.wins.get((player, S), 0),
              self.plays.get((player, S), 0), p)
             for p, S in moves_states),
            reverse=True
        ):
            print "{3}: {0:.2f}% ({1} / {2})".format(*x)

        print "Maximum depth searched:", self.max_depth

        return move

    def run_simulation(self):
        # A bit of an optimization here, so we have a local
        # variable lookup instead of an attribute access each loop.
        plays, wins = self.plays, self.wins

        visited_states = set()
        states_copy = self.states[:]
        state = states_copy[-1]
        player = self.board.current_player(state)

        expand = True
        for t in xrange(1, self.max_moves + 1):
            legal = self.board.legal_plays(states_copy)
            moves_states = [(p, self.board.next_state(state, p)) for p in legal]

            if all(plays.get((player, S)) for p, S in moves_states):
                # If we have stats on all of the legal moves here, use them.
                log_total = log(
                    sum(plays[(player, S)] for p, S in moves_states))
                value, move, state = max(
                    ((wins[(player, S)] / plays[(player, S)]) +
                     self.C * sqrt(log_total / plays[(player, S)]), p, S)
                    for p, S in moves_states
                )
            else:
                # Otherwise, just make an arbitrary decision.
                move, state = choice(moves_states)

            states_copy.append(state)

            # `player` here and below refers to the player
            # who moved into that particular state.
            if expand and (player, state) not in plays:
                expand = False
                plays[(player, state)] = 0
                wins[(player, state)] = 0
                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add((player, state))

            player = self.board.current_player(state)
            winner = self.board.winner(states_copy)
            if winner:
                break

        for player, state in visited_states:
            if (player, state) not in plays:
                continue
            plays[(player, state)] += 1
            if player == winner:
                wins[(player, state)] += 1

def play():
    deck = Deck()
    player1_hand = deck.draw(2)
    player2_hand = deck.draw(2)
    deck.draw(1)
    board = deck.draw(3)
    deck.draw(1)
    board.append(deck.draw(1))
    deck.draw(1)
    board.append(deck.draw(1))

    evaluator = Evaluator()

    p1_score = evaluator.evaluate(board, player1_hand)
    p2_score = evaluator.evaluate(board, player2_hand)

    if p1_score < p2_score:
        global player1_score_count
        player1_score_count += 1
    elif p1_score == p2_score:
        global tie_score_count
        tie_score_count += 1
    else:
        global player2_score_count
        player2_score_count += 1


for x in range(0, 30):
    play()
print "Player 1 score: " + str(player1_score_count)
print "Player 2 score: " + str(player2_score_count)
print "Ties: " + str(tie_score_count)
if player1_score_count > player2_score_count:
    print "Player 1 wins!"
elif player2_score_count > player1_score_count:
    print "Player 2 wins!"
else:
    print "Tie? wtf"

