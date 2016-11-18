from deuces import Deck, Evaluator
player1_score_count = 0
player2_score_count = 0
tie_score_count = 0

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


for x in range(0, 3000):
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

