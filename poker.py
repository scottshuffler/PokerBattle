from deuces import Deck, Card, Deck, Evaluator

deck = Deck()
board = deck.draw(5)
player1_hand = deck.draw(2)
player2_hand = deck.draw(2)

eval = Evaluator()

p1_score = eval.evaluate(board, player1_hand)
p2_score = eval.evaluate(board, player2_hand)



p1_class = eval.get_rank_class(p1_score)
p2_class = eval.get_rank_class(p2_score)


print "Player 1 hand rank = %d (%s)\n" % (p1_score, eval.class_to_string(p1_class))

print "Player 2 hand rank = %d (%s)\n" % (p2_score, eval.class_to_string(p2_class))

if p1_score < p2_score:
	print "Player 1 wins!"
elif p1_score == p2_score:
	print "Tie!"
else:
	print "Player 2 wins!"