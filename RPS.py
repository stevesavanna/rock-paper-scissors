import itertools


def player(prev_play, opponent_history=[], my_history=[], play_order={}, games_won_or_drawn=[], strategy=[]):
    choices = ['R', 'P', 'S']
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}

    if not prev_play:
        prev_play = choices[0]

        opponent_history.clear()
        play_order.clear()
        my_history.clear()
        my_history.append(prev_play)
        games_won_or_drawn.clear()
        games_won_or_drawn.append(0)
        strategy.clear()
        strategy.append(1)

        for v in itertools.product(''.join(choices), repeat=2):
            key = ''.join(v)
            play_order[key] = 0

    opponent_history.append(prev_play)

    if len(my_history) > 0:
        my_prev_play = my_history[-1]
        if (my_prev_play == 'P' and prev_play == 'R') or (my_prev_play == 'R' and prev_play == 'S') or (
                my_prev_play == 'S' and prev_play == 'P') or (my_prev_play == prev_play):
            games_won_or_drawn[0] += 1

        if len(my_history) != 0:
            win_rate = games_won_or_drawn[0] / len(my_history) * 100

            if win_rate < 100:
                if strategy[0] == 1:
                    strategy[0] = 2
                elif ''.join(opponent_history[-3:]) == ''.join([ideal_response[x] for x in my_history[:-1][-3:]]):
                    strategy[0] = 3

    if strategy[0] in (1, 2):
        last_two = ''.join(opponent_history[-2:])
        if len(last_two) == 2:
            play_order[last_two] += 1

        potential_plays = [prev_play + choice for choice in choices]
        sub_order = {k: play_order[k] for k in potential_plays}
        prediction = max(sub_order, key=sub_order.get)[-1:]
        guess = ideal_response[prediction]

        if strategy[0] == 1:
            guess = ideal_response[guess]
    else:
        guess = ideal_response[ideal_response[my_history[-1]]]

    my_history.append(guess)

    return guess
