from __future__ import division
from deuces import Deck, Evaluator, Card
player1_score_count = 0
player1_fold_count = 0
player2_score_count = 0
player2_fold_count = 0
tie_score_count = 0
games_played = 0
import datetime
import time
import random as random
from random import choice, randint
from math import log, sqrt

# Monte is player 1
# Simple is player 2

class Board(object):

    def start(self):
        #     P1H,P2H,P1M, P2M, POT, TABLE, BB, SB, CP, LA
        bb = random.randint(1, 2)
        sb = 1
        if bb == 1:
            sb = 2
            return [[],[],100, 100, 0, [], 1, 2, 2, ""]
        return [[],[],100, 100, 0, [], 2, 1, 1, ""]

    def current_player(self, state):
        return state[8]

    def next_state(self, state, play, is_blind):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        state = list(state)
        if play in ("R", "CH", "CA", "F", "P"):
            board = Board()
            cp = board.current_player(state)
            op = cp ^ 3
            LA = ""
            if play ==  "P":
                LA = "P"
            elif play == "CH":
                LA = "CH"
            elif play == "R":
                if state[cp + 1] >= 2:
                    state[cp+1] -= 2
                    state[4] += 2
                else:
                    state[cp+1] -= 1
                    state[4] += 1
                LA = "R"
            elif play == "CA":
                if is_blind:
                    #print "is blind"
                    state[cp+1] -= 1
                    state[4] += 1
                elif state[cp + 1] >= 2:
                    state[cp+1] -= 2
                    state[4] += 2
                else:
                    state[cp+1] -= 1
                    state[4] += 1
                LA = "CA"
            elif play == "F":
                state[op+1] += state[4]
                state[4] = 0
                LA = "F"
        state[8] = op
        state[9] = LA
        return state

    def legal_plays(self, state_history):
        if len(state_history) > 1:
            cp = state_history[-1][8] ^ 3
            if state_history[-1][cp + 1] == 0:
                return ["P"]
            if state_history[-1][9] == "R":
                return ["CA", "F"]
            elif state_history[-1][9] == "CH":
                return ["R", "CH"]
            elif state_history[-1][9] == "CA":
                return ["R", "CH"]
            else:
                return []
        else:
            cp = state_history[0][8] ^ 3
            if state_history[0][cp + 1] == 0:
                return ["P"]
            if state_history[0][9] == "R":
                return ["CA", "F"]
            elif state_history[0][9] == "CH":
                return ["R", "CH"]
            elif state_history[0][9] == "CA":
                return ["R", "CH"]
            else:
                return []

    def winner(self, state_history):
        
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        pass

class simplebot:
    # def __init__(self, board, check, bet, call, fold):
    #     self.check, self.bet, self.call, self.fold = check, bet, call, fold
    #     self.board = board
    #     self.state = []
    #     pass
    def __init__(self, board, player_number, bcheck, bbet, bcall, bfold, scheck, sbet, scall, sfold):
        self.bcheck, self.bbet, self.bcall, self.bfold = bcheck, bbet, bcall, bfold
        self.scheck, self.sbet, self.scall, self.sfold = scheck, sbet, scall, sfold
        self.board = board
        self.state = []
        self.player_number = player_number
        pass
    def update_aggression(self, aggression):
        self.aggression = aggression

    def update_state(self, state):
        self.state.append(state)

    def first_move(self, state):
        # state[6] is BB
        # state[7] is SB
        if state[6] == self.player_number:
            #print "I'm the big blind"
            #print self.player_number
            if state[self.player_number + 1] >= 2:
                state[self.player_number + 1] -= 2
                state[4] += 2
            else:
                state[self.player_number+1] -= 1
                state[4] += 1
        else:
            #print "I'm the small blind"
            state[self.player_number+1] -= 1
            state[4] += 1
        #print state

    def force_move(self, state, play):
        return self.board.next_state(state, play, False)

    def next_move(self, state):
        self.update_state(state)
        legal = self.board.legal_plays(self.state)
        if not legal:
            play = random.randint(1, 100)
            if play > 40:
                state = self.board.next_state(state, "F", True)
            else:
                state = self.board.next_state(state, "CA", True)
        else:
            #
            # Big blind
            #play = choice(legal)
            if self.player_number == state[6] and len(legal) > 1:
                picked = False
                fold = self.bfold
                call = fold + self.bcall
                check = call + self.bcheck

                while not picked:
                    rand = random.randint(1, 100)
                    if rand < fold and "F" in legal:
                        state = self.board.next_state(state, "F", False) 
                        picked = True
                    elif rand < call and "CA" in legal:
                        state = self.board.next_state(state, "CA", False) 
                        picked = True
                    elif rand < check and "CH" in legal:
                        state = self.board.next_state(state, "CH", False) 
                        picked = True
                    elif "R" in legal:
                        state = self.board.next_state(state, "R", False)
                        picked = True
            elif self.player_number == state[6] and len(legal) > 0:
                state = self.board.next_state(state, legal[0], False)
            elif self.player_number == state[7] and len(legal) > 1:
                # play = choice(legal)
                picked = False

                fold = self.sfold
                call = fold + self.scall

                check = self.scheck
                bet = check + self.sbet

                while not picked:
                    rand = random.randint(1, 100)
                    if "CH" in legal and "R" in legal:
                        if rand < check:
                            state = self.board.next_state(state, "CH", False) 
                            picked = True
                        else:
                            state = self.board.next_state(state, "R", False)
                            picked = True
                    elif "F" in legal and "CA" in legal:
                        if rand < fold:
                            state = self.board.next_state(state, "F", False) 
                            picked = True
                        else:
                            state = self.board.next_state(state, "CA", False) 
                            picked = True
            elif self.player_number == state[7] and len(legal) > 0:
                state = self.board.next_state(state, legal[0], False)  
            else:
                play = choice(legal)
                state = self.board.next_state(state, play, False) 
        return state

def play():
    print "Playing..."
    # deck = Deck()
    # player1_hand = deck.draw(2)
    # player2_hand = deck.draw(2)
    # deck.draw(1)
    # board = deck.draw(3)
    # deck.draw(1)
    # board.append(deck.draw(1))
    # deck.draw(1)
    # board.append(deck.draw(1))

    

    

    # if p1_score < p2_score:
    #     global player1_score_count
    #     player1_score_count += 1
    # elif p1_score == p2_score:
    #     global tie_score_count
    #     tie_score_count += 1
    # else:
    #     global player2_score_count
    #     player2_score_count += 1
    board = Board()
    state = board.start()

#def __init__(self, board, player_number, bcheck, bbet, bcall, bfold, scheck, sbet, scall, sfold):

    #passivebot = simplebot(board, 1, 30, 10, 20, 40, 70, 30, 33, 66)
    passivebot = simplebot(board, 1, 20, 30, 30, 20, 40, 60, 66, 33)
    aggressivebot = simplebot(board, 2, 20, 30, 30, 20, 40, 60, 66, 33)
    while state[2] > 0 and state[3] > 0:
        global games_played
        games_played += 1
        if games_played > 1:
            bb = state[6]
            state[6] = state[7]
            state[7] = bb
        deck = Deck()
        evaluator = Evaluator()
        player1_hand = deck.draw(2)
        player2_hand = deck.draw(2)
        state[0] = []
        state[1] = []
        state[5] = []
        state[0] = player1_hand
        state[1] = player2_hand
        
        passivebot.first_move(state)
        aggressivebot.first_move(state)

        if state[7] == 1:
            # print "Start 1"
            state = passivebot.next_move(state)
            # print state
            # print ""
            if state[9] != "F":
                # print "Start 2"
                state = aggressivebot.force_move(state, "CH")
                # print state
                # print ""
            else:
                global player1_fold_count
                player1_fold_count += 1
                
        else:
            # print "Start 1"
            state = aggressivebot.next_move(state)
            # print state
            # print ""
            if state[9] != "F":
                # print "Start 2"
                state = passivebot.force_move(state, "CH")
                # print state
                # print ""
            else:
                global player2_fold_count
                player2_fold_count += 1
                
        
        if state[9] != "F":
            # print "drawing cards"
            # print "flop"
            deck.draw(1)
            state[5] += deck.draw(3)

        count = 3
        card_counter = 0
        ## GAME ON
        while state[9] != "F":

            # print ""
            # print "Start " + str(count)
            LA = state[9]
            if state[8] == 1:
                state = passivebot.next_move(state)
            else:
                state = aggressivebot.next_move(state)

            # print "End"
            # print state
            # print ""
            count += 1
            card_counter += 1
            if state[9] == "F":
                if state[8] == 2:
                    global player1_fold_count
                    player1_fold_count += 1
                else:
                    global player2_fold_count
                    player2_fold_count += 1
                break
            if LA == "R" and state[9] == "CA" or LA == "CH" and state[9] == "CH" and card_counter > 1:
                if len(state[5]) == 3:
                    #print "turn"
                    deck.draw(1)
                    state[5].append(deck.draw(1))
                elif len(state[5]) == 4:
                    #print "river"
                    deck.draw(1)
                    state[5].append(deck.draw(1))
                elif len(state[5]) == 5:
                    #print "showdown"
                    p1_score = evaluator.evaluate(state[5], player1_hand)
                    p2_score = evaluator.evaluate(state[5], player2_hand)
                    if p1_score == p2_score:
                        pot = state[4]
                        state[2] += (pot / 2)
                        state[3] += (pot / 2)
                        state[4] = 0
                        global tie_score_count
                        tie_score_count += 1
                    elif p1_score < p2_score:
                        #print "player 1 wins"
                        state[2] += state[4]
                        state[4] = 0
                        global player1_score_count
                        player1_score_count += 1
                    else:
                        #print "player 2 wins"
                        state[3] += state[4]
                        state[4] = 0
                        global player2_score_count
                        player2_score_count += 1
                    #print state
                    break
                card_counter = 0
                

for j in range(1,10):
    start_time = time.clock()
    for x in range(0, 10):
        play()
    print "Tournament took: " + str(int(time.clock() - start_time)) + " seconds"
    del start_time
    print "Player 1 score: " + str(player1_score_count)
    print "Player 2 score: " + str(player2_score_count)
    print "Player 1 folds: " + str(player1_fold_count)
    print "Player 2 folds: " + str(player2_fold_count)
    print "Player 1 total score: " + str(player1_score_count + player2_fold_count)
    print "Player 2 total score: " + str(player2_score_count + player1_fold_count)
    print "Ties: " + str(tie_score_count)
    if player1_score_count > player2_score_count:
        print "Player 1 wins!"
    elif player2_score_count > player1_score_count:
        print "Player 2 wins!"
    else:
        print "Tie? wtf"
    print "Games played: " + str(games_played)
    player1_score_count = 0
    player2_score_count = 0
    player1_fold_count = 0
    player2_fold_count = 0
    tie_score_count = 0
    games_played = 0
