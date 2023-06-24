from __future__ import annotations

import sys
from enum import Enum
from traceback import print_stack
from typing import Dict, List, Optional, Tuple


def debug(message: str) -> None:
    return
    print(message, file=sys.stderr, flush=True)
    print_stack(file=sys.stderr)


def my_assert(condition: bool, message: Optional[str] = None) -> None:
    return
    if not condition:
        debug(message)


class Neuron:
    weights: List[int]

    def __init__(self, weights: List[int]) -> None:
        self.weights = weights

    def calculate_output(self, inputs: List[int]) -> int:
        return sum(map(lambda x: x[0] * x[1], zip(inputs, self.weights)))

    def __str__(self) -> str:
        return str(self.weights)

    def __repr__(self) -> str:
        return str(self)


class Layer:
    depth: int
    neurons: List[Neuron]

    def __init__(self, depth: int, neurons: List[Neuron]) -> None:
        self.depth = depth
        self.neurons = neurons

    def calculate_output(self, inputs: List[int]) -> List[int]:
        return [neuron.calculate_output(inputs) for neuron in self.neurons]

    def __str__(self) -> str:
        return f"Layer {self.depth}: {str(self.neurons)}"

    def __repr__(self) -> str:
        return str(self)


def compute_synapses_count(
    inputs_count: int, hiddens_counts: List[int], outputs_count: int
) -> int:
    return (
        inputs_count * hiddens_counts[0]
        + sum(map(lambda x: x[0] * x[1], zip(hiddens_counts, hiddens_counts[1:])))
        + hiddens_counts[-1] * outputs_count
    )


class NeuralNetwork:
    layers: List[Layer]

    def __init__(
        self,
        weights: List[int],
        inputs_count: int,
        hiddens_counts: List[int],
        outputs_count: int,
    ) -> None:
        synapses_count = compute_synapses_count(
            inputs_count, hiddens_counts, outputs_count
        )
        my_assert(
            (len(weights) == synapses_count),
            f"Weights count ({len(weights)}) does not match the expected count ({synapses_count})",
        )

        self.layers = []
        for layer_index in range(len(hiddens_counts) + 1):
            neurons = []
            if layer_index == 0:
                neurons = [
                    Neuron(
                        weights[
                            # fmt: off
                            neuron_index * inputs_count
                            : (neuron_index + 1) * inputs_count
                            # fmt: on
                        ]
                    )
                    for neuron_index in range(hiddens_counts[layer_index])
                ]
                shift = inputs_count * hiddens_counts[layer_index]
            elif layer_index < len(hiddens_counts):
                neurons = [
                    Neuron(
                        weights[
                            # fmt: off
                            shift + neuron_index * hiddens_counts[layer_index - 1]
                            : shift + (neuron_index + 1) * hiddens_counts[layer_index - 1]
                            # fmt: on
                        ]
                    )
                    for neuron_index in range(hiddens_counts[layer_index])
                ]
                shift += hiddens_counts[layer_index - 1] * hiddens_counts[layer_index]
            else:
                neurons = [
                    Neuron(
                        weights[
                            # fmt: off
                            shift + neuron_index * hiddens_counts[layer_index - 1]
                            : shift + (neuron_index + 1) * hiddens_counts[layer_index - 1]
                            # fmt: on
                        ]
                    )
                    for neuron_index in range(outputs_count)
                ]
                shift += hiddens_counts[layer_index - 1] * outputs_count
            self.layers.append(Layer(layer_index + 1, neurons))

        my_assert(shift == len(weights), f"shift {shift} != weights {len(weights)}")

    def calculate_output(self, input: List[int]) -> List[int]:
        inout = input
        for layer in self.layers:
            inout = layer.calculate_output(inout)

        return inout

    def __str__(self) -> str:
        return "\n".join((str(layer) for layer in self.layers))

    def __repr__(self) -> str:
        return str(self)


def compute_best_hiddens_counts(
    inputs_count: int, outputs_count: int, layers_count
) -> List[int]:
    return [
        inputs_count
        + (layer_index + 1) * (outputs_count - inputs_count) // (layers_count + 1)
        for layer_index in range(layers_count)
    ]


# 188 inputs, 78 outputs, 1 hidden layer
INPUTS_COUNT = 188
OUTPUTS_COUNT = 76
HIDDEN_LAYERS_COUNT = 1
HIDDENS_COUNTS = compute_best_hiddens_counts(
    INPUTS_COUNT, OUTPUTS_COUNT, HIDDEN_LAYERS_COUNT
)
SYNAPSES_COUNT = compute_synapses_count(INPUTS_COUNT, HIDDENS_COUNTS, OUTPUTS_COUNT)

APPLICATIONS_COUNT = 12
TASKS_COUNT = 8
CARDS_LOCATIONS_COUNT = 6
PLAYERS_COUNT = 2
APPLICATIONS_TO_WIN = 5


class Game_Phase(Enum):
    MOVE = 0
    GIVE_CARD = 1
    THROW_CARD = 2
    PLAY_CARD = 3
    RELEASE = 4


class Action(Enum):
    RANDOM = 0
    WAIT = 1
    MOVE = 2
    GIVE = MOVE + 2 * TASKS_COUNT
    THROW = GIVE + TASKS_COUNT
    TRAINING = THROW + TASKS_COUNT
    CODING = TRAINING + 1
    DAILY_ROUTINE = CODING + 1
    TASK_PRIORITIZATION = DAILY_ROUTINE + 1
    ARCHITECTURE_STUDY = TASK_PRIORITIZATION + 2 * TASKS_COUNT
    CONTINUOUS_INTEGRATION = ARCHITECTURE_STUDY + 1
    CODE_REVIEW = CONTINUOUS_INTEGRATION + TASKS_COUNT
    REFACTORING = CODE_REVIEW + 1
    RELEASE = REFACTORING + 1


my_assert(
    (Action.RELEASE.value + APPLICATIONS_COUNT == OUTPUTS_COUNT),
    f"{Action.RELEASE.value} + {APPLICATIONS_COUNT} != {OUTPUTS_COUNT}",
)


class GreenCircleAI:
    neural_network: NeuralNetwork

    def __init__(self, weights: List[int]) -> None:
        self.neural_network = NeuralNetwork(
            weights, INPUTS_COUNT, HIDDENS_COUNTS, OUTPUTS_COUNT
        )

        my_assert(len(self.neural_network.layers) == len(HIDDENS_COUNTS) + 1)
        for layer_index in range(len(HIDDENS_COUNTS) + 1):
            my_assert(
                len(self.neural_network.layers[layer_index].neurons)
                == (
                    HIDDENS_COUNTS[layer_index]
                    if layer_index < len(HIDDENS_COUNTS)
                    else OUTPUTS_COUNT
                )
            )
            my_assert(
                len(self.neural_network.layers[layer_index].neurons[0].weights)
                == (
                    HIDDENS_COUNTS[layer_index - 1] if layer_index > 0 else INPUTS_COUNT
                )
            )

    def prepare_inputs(self) -> Tuple[List[int], Dict[int, int], Dict[str, bool]]:
        ai_inputs = []

        ai_inputs.append(1)  # bias

        game_phase = input()  # can be MOVE, GIVE_CARD, THROW_CARD, PLAY_CARD or RELEASE
        for i in range(len(Game_Phase)):
            ai_inputs.append(1 if game_phase == Game_Phase(i).name else 0)

        applications_count = int(input())
        applications: Dict[int, int] = {}
        for i in range(applications_count):
            # object_type: always APPLICATION
            # id : id of the application
            # training_needed: number of TRAINING skills needed
            # coding_needed: number of CODING skills needed
            # daily_routine_needed: number of DAILY_ROUTINE skills needed
            # task_prioritization_needed: number of TASK_PRIORITIZATION skills needed
            # architecture_study_needed: number of ARCHITECTURE_STUDY skills needed
            # continuous_delivery_needed: number of CONTINUOUS_DELIVERY skills needed
            # code_review_needed: number of CODE_REVIEW skills needed
            # refactoring_needed: number of REFACTORING skills needed
            inputs = input().split()

            applications[int(inputs[1])] = i
            ai_inputs.extend([int(inp) for inp in inputs[2:]])

        ai_inputs.extend([0] * TASKS_COUNT * (APPLICATIONS_COUNT - applications_count))

        for i in range(PLAYERS_COUNT):
            # player_location: id of the zone in which the player is located
            # player_score: number of points scored by the player
            # player_permanent_daily_routine_cards: number of DAILY_ROUTINE played
            # player_permanent_architecture_study_cards: number of ARCHITECTURE_STUDY played
            inputs = input().split()
            player_location = int(inputs[0])
            for i in range(-1, TASKS_COUNT):
                ai_inputs.append(1 if player_location == i else 0)

            player_score = int(inputs[1])
            ai_inputs.append(player_score)
            correct_tasks_only = 1 if player_score == APPLICATIONS_TO_WIN - 1 else 0
            ai_inputs.append(correct_tasks_only)
            ai_inputs.extend([int(inp) for inp in inputs[2:]])

        card_locations_count = int(input())
        for i in range(card_locations_count):
            # cards_location: the location of the card list.
            # It can be HAND, DRAW, DISCARD, OPPONENT_CARDS, AUTOMATED and OPPONENT_AUTOMATED
            # training_cards_count: number of TRAINING cards
            # coding_cards_count: number of CODING cards
            # daily_routine_cards_count: number of DAILY_ROUTINE cards
            # task_prioritization_cards_count: number of TASK_PRIORITIZATION cards
            # architecture_study_cards_count: number of ARCHITECTURE_STUDY cards
            # continuous_delivery_cards_count: number of CONTINUOUS_DELIVERY cards
            # code_review_cards_count: number of CODE_REVIEW cards
            # refactoring_cards_count: number of REFACTORING cards
            # bonus_cards_count: number of BONUS cards
            # technical_debt_cards_count: number of TECHNICAL_DEBT cards
            ai_inputs.extend([int(inp) for inp in input().split()[1:]])

        ai_inputs.extend(
            [0] * (TASKS_COUNT + 2) * (CARDS_LOCATIONS_COUNT - card_locations_count)
        )

        possible_actions_count = int(input())
        possible_actions = {}
        for i in range(possible_actions_count):
            possible_action = input()
            possible_actions[possible_action] = True

        my_assert(len(ai_inputs) == INPUTS_COUNT, f"{len(ai_inputs)} != {INPUTS_COUNT}")

        return ai_inputs, applications, possible_actions

    def act(
        self,
        ai_outputs: List[int],
        applications: Dict[int, int],
        possible_actions: Dict[str, bool],
    ) -> None:
        my_assert(
            len(ai_outputs) == OUTPUTS_COUNT, f"{len(ai_outputs)} != {OUTPUTS_COUNT}"
        )

        possible_action_scores = {}
        for possible_action in possible_actions:
            for action in Action:
                if possible_action == action.name:
                    # p(<Action>) = output(<Action>)
                    possible_action_scores[possible_action] = ai_outputs[action.value]
                    break
            else:
                possible_action_words = possible_action.split()
                if possible_action_words[0] == Action.MOVE.name:
                    if len(possible_action_words) == 2:
                        # p(MOVE <zone>) = p(MOVE <zone> <zone>)
                        possible_action_words.append(possible_action_words[1])

                    # p(MOVE <zone> <cardTypeToTake>) =
                    #     output(MOVE <zone>) * output(MOVE <cardTypeToTake>)
                    possible_action_scores[possible_action] = (
                        ai_outputs[Action.MOVE.value + int(possible_action_words[1])]
                        * ai_outputs[
                            Action.MOVE.value
                            + TASKS_COUNT
                            + int(possible_action_words[2])
                        ]
                    )
                elif possible_action_words[0] == Action.GIVE.name:
                    # p(GIVE <cardType>) = output(GIVE <cardType>)
                    possible_action_scores[possible_action] = ai_outputs[
                        Action.GIVE.value + int(possible_action_words[1])
                    ]
                elif possible_action_words[0] == Action.THROW.name:
                    # p(THROW <cardType>) = output(THROW <cardType>)
                    possible_action_scores[possible_action] = ai_outputs[
                        Action.THROW.value + int(possible_action_words[1])
                    ]
                elif possible_action_words[0] == Action.TASK_PRIORITIZATION.name:
                    # p(TASK_PRIORITIZATION <cardTypeToThrow> <cardTypeToTake>) =
                    #     output(TASK_PRIORITIZATION <cardTypeToThrow>)
                    #     * output(TASK_PRIORITIZATION <cardTypeToTake>)
                    possible_action_scores[possible_action] = (
                        ai_outputs[
                            Action.TASK_PRIORITIZATION.value
                            + int(possible_action_words[1])
                        ]
                        * ai_outputs[
                            Action.TASK_PRIORITIZATION.value
                            + TASKS_COUNT
                            + int(possible_action_words[2])
                        ]
                    )
                elif possible_action_words[0] == Action.CONTINUOUS_INTEGRATION.name:
                    # p(CONTINUOUS_INTEGRATION <cardTypeToAutomate>) =
                    #     output(CONTINUOUS_INTEGRATION <cardTypeToAutomate>)
                    possible_action_scores[possible_action] = ai_outputs[
                        Action.CONTINUOUS_INTEGRATION.value
                        + int(possible_action_words[1])
                    ]
                elif possible_action_words[0] == Action.RELEASE.name:
                    # p(RELEASE <applicationId>) = output(RELEASE <applicationId>)
                    possible_action_scores[possible_action] = ai_outputs[
                        Action.RELEASE.value
                        + applications[int(possible_action_words[1])]
                    ]
                else:
                    raise Exception(f"Unknown action: {possible_action}")

        print(max(possible_action_scores, key=possible_action_scores.get))  # type: ignore

    def run(self) -> None:
        ai_inputs, applications, possible_actions = self.prepare_inputs()
        ai_outputs = self.neural_network.calculate_output(ai_inputs)
        self.act(ai_outputs, applications, possible_actions)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        debug(sys.argv[1])
        with open(sys.argv[1], "r") as f:
            chr = f.read()
    else:
        chr = ""

    weights = [int.from_bytes(c.encode(), "big") - 47 - 0x20 for c in chr]
    # weights = [int(weight) for weight in re.findall(r'[+-]\d+', chr)]

    weights += [0] * (SYNAPSES_COUNT - len(weights))
    ai = GreenCircleAI(weights[:SYNAPSES_COUNT])

    while True:
        ai.run()
