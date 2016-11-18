from deuces import Deck, Evaluator

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



# p1_class = eval.get_rank_class(p1_score)
# p2_class = eval.get_rank_class(p2_score)


# print "Player 1 hand rank = %d \n" % (p1_score, eval.class_to_string(p1_class))

# print "Player 2 hand rank = %d \n" % (p2_score, eval.class_to_string(p2_class))

print "Player 1 hand rank = %d \n" % (p1_score)

print "Player 2 hand rank = %d \n" % (p2_score)

if p1_score < p2_score:
	print "Player 1 wins!"
elif p1_score == p2_score:
	print "Tie!"
else:
	print "Player 2 wins!"


