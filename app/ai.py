import sys
import math
from typing import List
import operator
from random import randint


# Complete the hackathon before your opponent by following the principles of Green IT
class Application:
    object_type : str
    _id : int
    tasks : List[int]
    score : int
    # training_needed : int  # number of TRAINING skills needed to release this application
    # coding_needed : int  # number of CODING skills needed to release this application
    # daily_routine_needed : int  # number of DAILY_ROUTINE skills needed to release this application
    # task_prioritization_needed : int  # number of TASK_PRIORITIZATION skills needed to release this application
    # architecture_study_needed : int  # number of ARCHITECTURE_STUDY skills needed to release this application
    # continuous_delivery_needed : int  # number of CONTINUOUS_DELIVERY skills needed to release this application
    # code_review_needed : int  # number of CODE_REVIEW skills needed to release this application
    # refactoring_needed : int  # number of REFACTORING skills needed to release this application


class Cards:
    cards_location : str  # the location of the card list. It can be HAND, DRAW, DISCARD or OPPONENT_CARDS (AUTOMATED and OPPONENT_AUTOMATED will appear in later leagues)
    # training_cards_count : int
    # coding_cards_count : int
    # daily_routine_cards_count : int
    # task_prioritization_cards_count : int
    # architecture_study_cards_count : int
    # continuous_delivery_cards_count : int
    # code_review_cards_count : int
    # refactoring_cards_count : int
    bonus_cards_count : int
    technical_debt_cards_count : int
    cards : List[int]


threshold = randint(0,3)

# game loop
while True:
    game_phase = input()  # can be MOVE, GIVE_CARD, THROW_CARD, PLAY_CARD or RELEASE
    #print(game_phase, file=sys.stderr, flush=True)
    applications_count = int(input())
    applications = {}
    for i in range(applications_count):
        app = Application()
        inputs = input().split()
        print(inputs, file=sys.stderr, flush=True)
        app.object_type = inputs[0]
        app._id = int(inputs[1])
        app.tasks = [int(inp) for inp in inputs[2:10]]
        # app.training_needed = int(inputs[2])  # number of TRAINING skills needed to release this application
        # app.coding_needed = int(inputs[3])  # number of CODING skills needed to release this application
        # app.daily_routine_needed = int(inputs[4])  # number of DAILY_ROUTINE skills needed to release this application
        # app.task_prioritization_needed = int(inputs[5])  # number of TASK_PRIORITIZATION skills needed to release this application
        # app.architecture_study_needed = int(inputs[6])  # number of ARCHITECTURE_STUDY skills needed to release this application
        # app.continuous_delivery_needed = int(inputs[7])  # number of CONTINUOUS_DELIVERY skills needed to release this application
        # app.code_review_needed = int(inputs[8])  # number of CODE_REVIEW skills needed to release this application
        # app.refactoring_needed = int(inputs[9])  # number of REFACTORING skills needed to release this application
        applications[app._id] = app
    #for i in range(2):
        # player_location: id of the zone in which the player is located
        # player_permanent_daily_routine_cards: number of DAILY_ROUTINE the player has played. It allows them to take cards from the adjacent zones
        # player_permanent_architecture_study_cards: number of ARCHITECTURE_STUDY the player has played. It allows them to draw more cards

    inputs = input().split()
    #print(inputs, file=sys.stderr, flush=True)
    player_location, player_score, player_permanent_daily_routine_cards, player_permanent_architecture_study_cards = [int(j) for j in inputs]
    inputs = input().split()
    #print(inputs, file=sys.stderr, flush=True)
    other_player_location, other_player_score, other_player_permanent_daily_routine_cards, other_player_permanent_architecture_study_cards = [int(j) for j in inputs]
    card_locations_count = int(input())
    cardss = {}
    for i in range(card_locations_count):
        cards = Cards()
        inputs = input().split()
        #print(inputs, file=sys.stderr, flush=True)
        cards.cards_location = inputs[0]  # the location of the card list. It can be HAND, DRAW, DISCARD or OPPONENT_CARDS (AUTOMATED and OPPONENT_AUTOMATED will appear in later leagues)
        cards.cards = [int(inp) for inp in inputs[1:9]]
        training_cards_count = int(inputs[1])
        # cards.coding_cards_count = int(inputs[2])
        # cards.daily_routine_cards_count = int(inputs[3])
        # cards.task_prioritization_cards_count = int(inputs[4])
        # cards.architecture_study_cards_count = int(inputs[5])
        # cards.continuous_delivery_cards_count = int(inputs[6])
        # cards.code_review_cards_count = int(inputs[7])
        # cards.refactoring_cards_count = int(inputs[8])
        cards.bonus_cards_count = int(inputs[9])
        cards.technical_debt_cards_count = int(inputs[10])
        cardss[cards.cards_location] = cards
    possible_moves_count = int(input())
    possible_moves = []
    for i in range(possible_moves_count):
        possible_move = input()
        if len(possible_move.split()) > 1:
            possible_moves.append(possible_move.split()[1])
    #print(possible_moves, file=sys.stderr, flush=True)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    scores = {}
    for k, app in applications.items():
        scores[k] = 0
        for i, task in enumerate(app.tasks):
            scores[k] += min(task, cardss["HAND"].cards[i] * 2 + cardss["HAND"].bonus_cards_count)
    print(scores, file=sys.stderr, flush=True)

    # In the first league: RANDOM | MOVE <zoneId> | RELEASE <applicationId> | WAIT; In later leagues: | GIVE <cardType> | THROW <cardType> | TRAINING | CODING | DAILY_ROUTINE | TASK_PRIORITIZATION <cardTypeToThrow> <cardTypeToTake> | ARCHITECTURE_STUDY | CONTINUOUS_DELIVERY <cardTypeToAutomate> | CODE_REVIEW | REFACTORING;
    if game_phase == "MOVE":
        scores = {key:value for (key,value) in scores.items() if value < 8}
        if scores:
            needed = {key:value for (key,value) in enumerate(applications[max(scores.items(), key=operator.itemgetter(1))[0]].tasks) if value > 0 and key != player_location and key != other_player_location and key != (other_player_location - 1) % 8 and key != (other_player_location + 1) % 8}
            has = {key:value for (key,value) in enumerate(cardss["HAND"].cards) if needed.get(key)}
            print((needed, has), file=sys.stderr, flush=True)

            if has:
                print(f'MOVE {min(has, key=has.get)}')
            elif needed:
                print(f'MOVE {needed.keys()[0]}')
            else:
                print(f'MOVE {(player_location + 1) % 8}')

        else:
            print(f'MOVE {(player_location + 1) % 8}')
    elif game_phase == "RELEASE":
        if scores:
            best = max(scores.items(), key=operator.itemgetter(1))
            if best[1] >= threshold:
                print(f'RELEASE {best[0]} {threshold}')
            else:
                print("WAIT")
        else:
            print("RANDOM")
    else:
        print("RANDOM")
