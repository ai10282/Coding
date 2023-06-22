import random

domino_set = []
stock_pieces = []
computer_pieces = []
player_pieces = []
domino_snake = []
ai_counter = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
ai_scores = {}
status = ""
trigger = True

while trigger:
    domino_set = []
    for i in range(7):
        for j in range(7):
            if j >= i:
                domino_set.append([i, j])
    random.shuffle(domino_set)

    stock_pieces = []
    computer_pieces = []
    player_pieces = []
    domino_snake = []
    status = ""

    for i in range(14):
        if i % 2 == 0:
            computer_pieces.append(domino_set.pop())
        else:
            player_pieces.append(domino_set.pop())

    stock_pieces = domino_set

    for i in range(7):
        if [6 - i, 6 - i] in computer_pieces:
            domino_snake.append(computer_pieces.pop(computer_pieces.index([6 - i, 6 - i])))
            status = "player"
            trigger = False
            break
        elif [6 - i, 6 - i] in player_pieces:
            domino_snake.append(player_pieces.pop(player_pieces.index([6 - i, 6 - i])))
            status = "computer"
            trigger = False
            break

while True:
    print("=" * 70)
    print("Stock size:", len(stock_pieces))
    print("Computer pieces:", len(computer_pieces))
    print()
    if len(domino_snake) > 6:
        print(str(domino_snake[0]) + str(domino_snake[1]) + str(domino_snake[2]) +
              "..." + str(domino_snake[-3]) + str(domino_snake[-2]) + str(domino_snake[-1]))
    else:
        print(*domino_snake, sep='')
    print()
    print("Your pieces:")
    for counter, domino_piece in enumerate(player_pieces, start=1):
        print(str(counter) + ":" + str(domino_piece))
    print()

    if len(computer_pieces) == 0:
        print("Status: The game is over. The computer won!")
        break
    elif len(player_pieces) == 0:
        print("Status: The game is over. You won!")
        break
    elif domino_snake[0][0] == domino_snake[-1][1]:
        counter = 0
        for domino in domino_snake:
            if domino_snake[0][0] == domino[0]:
                counter += 1
            if domino_snake[0][0] == domino[1]:
                counter += 1
        if counter == 8:
            print("Status: The game is over. It's a draw!")
            break

    if status == "computer":
        print("Status: Computer is about to make a move. Press Enter to continue...")
        input()

        ai_counter = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for i in range(7):
            for j in computer_pieces:
                if i in j:
                    if j[0] == j[1]:
                        ai_counter[i] += 2
                    else:
                        ai_counter[i] += 1
            for j in domino_snake:
                if i in j:
                    if j[0] == j[1]:
                        ai_counter[i] += 2
                    else:
                        ai_counter[i] += 1
        ai_scores = {}
        for domino in computer_pieces:
            ai_scores[str(domino)] = ai_counter[domino[0]] + ai_counter[domino[1]]
        ai_scores_sorted = dict(sorted(ai_scores.items(), key=lambda x: x[1]))

        domino_snake_len = len(domino_snake)
        while len(ai_scores_sorted) > 0:
            max_value = ai_scores_sorted.popitem()
            max_value = max_value[0]
            max_score = []
            for i in max_value:
                if i.isdigit():
                    max_score.append(int(i))
            if domino_snake[0][0] in max_score:
                if domino_snake[0][0] == max_score[1]:
                    domino_snake.insert(0, computer_pieces.pop(computer_pieces.index(max_score)))
                    status = "player"
                    break
                else:
                    max_score.reverse()
                    domino_snake.insert(0, computer_pieces.pop(computer_pieces.index([max_score[1], max_score[0]])))
                    status = "player"
                    break
            elif domino_snake[-1][1] in max_score:
                if domino_snake[-1][1] == max_score[0]:
                    domino_snake.append(computer_pieces.pop(computer_pieces.index(max_score)))
                    status = "player"
                    break
                else:
                    max_score.reverse()
                    domino_snake.append(computer_pieces.pop(computer_pieces.index([max_score[1], max_score[0]])))
                    status = "player"
                    break
        if len(domino_snake) == domino_snake_len:
            if len(stock_pieces) > 0:
                computer_pieces.append(stock_pieces.pop())
            status = "player"

    elif status == "player":
        print("Status: It's your turn to make a move. Enter your command.")
        while True:
            action = input()
            if action.lstrip('-').isnumeric() and abs(int(action)) <= len(player_pieces):
                action = int(action)
                if action < 0:
                    if domino_snake[0][0] in player_pieces[-action - 1]:
                        if domino_snake[0][0] == player_pieces[-action - 1][1]:
                            domino_snake.insert(0, player_pieces.pop(-action - 1))
                            status = "computer"
                            break
                        else:
                            tmp1 = player_pieces[-action - 1][0]
                            tmp2 = player_pieces[-action - 1][1]
                            player_pieces[-action - 1][0], player_pieces[-action - 1][1] = tmp2, tmp1
                            domino_snake.insert(0, player_pieces.pop(-action - 1))
                            status = "computer"
                            break
                    else:
                        print("Illegal move. Please try again.")
                elif action > 0:
                    if domino_snake[-1][1] in player_pieces[action - 1]:
                        if domino_snake[-1][1] == player_pieces[action - 1][0]:
                            domino_snake.append(player_pieces.pop(action - 1))
                            status = "computer"
                            break
                        else:
                            tmp1 = player_pieces[action - 1][0]
                            tmp2 = player_pieces[action - 1][1]
                            player_pieces[action - 1][0], player_pieces[action - 1][1] = tmp2, tmp1
                            domino_snake.append(player_pieces.pop(action - 1))
                            status = "computer"
                            break
                    else:
                        print("Illegal move. Please try again.")
                elif action == 0:
                    if len(stock_pieces) > 0:
                        player_pieces.append(stock_pieces.pop())
                    status = "computer"
                    break
            else:
                print("Invalid input. Please try again.")
