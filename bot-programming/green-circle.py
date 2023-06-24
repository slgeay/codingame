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
        chr = "Gagq\\t:@#y+QJt8n}T,VH 5W#%K!q`;%A)^&sK<VUKQf{UDP6}<KSA8Ky;Qp0gKh'\"T`S&HN~K'b#<f=iCt`/'K#2jj; 3:}\\gFAZixW+vX(K@!4LT1Q~~fQ)D%E>Qcq1^(~[/PA$l:ZN.MK2-F`&SM_uF-<z$_GtEd-RY9)_M+1K?!~0UdG4.ma NLV%hBe2Um2G,;)xwsGKw1s;`%fST\" tFI;_?eoKa3k(hGUSM1rL)_ CWW,~o$v~9lNMA;h(q%:f$uPaQS>XB6QA@ @:ui==K7.Db/NG}hK!ldpWjtK$sG2#,woY}KG/9GkSLK*-(%34qW>bDMV\\%BNWDj~$&cGj/ zyw4i>Md5K'T|IKA9)Q[aT)\\0xL<KH?}MP@W4#>KCMM{GA+ST!}ZhEAo1L~;0-J\\uk~Lk,(ik`dvGZ2s/b2Wu3g@FK/#K(h06dVpK*WJS2iILGmn8H7u>8f#W\">5tnB~GV,vY*&YQ?B)FnQ?qMmS;I^DPKV\"G,&={$Gm7@!MizSH;%cn_8hFM*>e68QG7=+wzSK,ZG/WCGsfW5:q\\w`|F)DST%A7ZazPaa\\QGS#t%{StPd!MlWKMWi+!L&W(BFW#rY\"6&r55d((,a{ j63_&+ ?*Gm>$PG7Wr7aKJ44F'G?IKM>'IT+GWG>T,ipGhlMGS(.*mG6SyV&xE'HR_|0hZ*71j>j]QqG[W91^W5z?<'%M^5DG5%k><3YE1_ESV=$ZFqWs<`NW|{r{.WFnj)SKU]GuUY-QlQCSy82QUM*(\"AKCM%yg?ijGl~vYv1W.gG#>eQR1@-8QHhT9~+6U)wQG?vk/_@rWBhqe u0Q~*Yb;KT F?*^07Ap8-tN; T]Ln|BX.NWf$nc-u'PWR'pM|S_WSIBiSS^;zD(#)u_WqS/,MnQnu,\"_QQGNINWW[_Bj,m'KD]ppK70##UQ##K!`RK#KKEfuv.So qvQn*?3fKd.FKcEicMxx0HL:{v ?9GKd^m3q{@@D'l(@`i5#1,MUL}z3(Bl%)\"4??SsSPnW)phu>DujS8zv$zMYy!J83^Ry\\m;=%;K[xp=@%}osKD-ir+pK6]/[WW\\v\"1y*fE0Mqu\"7JiS}EYC|FKd)<gW!.3SHR8yGBG`bK@3`0A'F{h}Cc|\\uE5G'i$Z<<TF${N@b.{g=6`)S_XN,ISK_CDjnr@CY$aR<u.,_>FZdw'edP>BCnwHLT/G\\BlM DPjg[*NsE<\\}>W\\tY/aK1x bJWA].1Tf={3_&sMZG'x[M`[!nrN{NGhG&<H/['@b:bN(KqD+]\\KS4DGc/S/#F,Qn4T6.;!fQ0SR}K|k@FK0'e>7m7KMNGfW5nH2iAVKS-GHsKm?ZT)(yM;?B7UQ7nSAx,ZRKY2hA>1G&eMJ\"WS.Z:QZZvSG.5:D?Gt>UJ^fDjS`7lW\\-GM_+&j2]?t=l4G8`(W3MuKRU,9_VyGjQ%@8=kE~5~+L#YoZ7KlanQWKaZuKR#}!qXg1`JoU3;qQ(K}oK_QVa.kuM}QU_ok;wb64DGWnj,Gc'GBNK;sNkQCUa$>NiPc/JtJPwgCWS3w!GSY/?) FD6Klc3l>MGuKM@kn1BQ_Lv&mt|W8kdbv1$'4^m#|;pi|5,X\\]KUF6MS`WH9eBR\\h'43K*@$HibKGW,'9^>0+&-S3l[TJ&cUVibW6)nS2BT'QW\"EH?7PJ3Sn9)nU?p{(]SX?ZKkB Hgce,2tGQ?Q*im17eRW>uS+Zm\\}&GXv^xIfUW2V4=EG Z8y'SQSR?|(;Q?+GMF3>3]fsz<)&dqRmtC2=^tS,4Ki+J7<KhJWG]#SUWK:]e.RVxc#z.S&Dqe`_P`|>Dq?6K|WG*-M_9>*]f)G%h0&WDFQn93_p_`|7|Bv\"saQW)>',P9I5>F}UFX6GvDmE$-*EKFmpQQ(MI>n46a*3}pl]nGSk&Jk|P9{d6*VP49PSM'bW5yW%D-T[@=i^#VlKxTjW@MN6}W>\"'Xp$G$~j6i~?`L| `7KSA^M6Q!j_#TNRU)S+eS1G>#'D\\{zqhs/kM@i1hu>\"KQ)}S1u67SV!GWRn.9M\\sN5[KG2J5aTG\"y+6tGdcaQ>l6cyZ^NUQp&2`Q]3dS^r0bWtG!8ZL,t1\"h5I(qVICoseR\"d>i06KE8u9r`pfGn&r31lL@E4S \"/nqi+x{ffC\":(3P:~sKuzac9T`>$+o89j$UK/S0J)=c\"GG0eK7l0@+o'=TLhj--;wUq\"S$CNUkKR.Tm v}2D[8z5nWxV4#EMchMj{`D/fGZ|YqIH.ea14T,a}GY#QZhFZ.&hw(X.LT-)1Js^,5W00jA7#~:7G=9iG)RVb\":*qN!Q)W:^>.8-S]`>X#sW2 |Bm|S\">[;ShBL/'U.-q&A6QP}P_d&NK\"MSI9t@cc-8 #Zv_S#0[1KEfKvMzM*A-\\-T<<QxlK,d5RW(GQW>]pJmM<G<y1'<K3hinMUiS.-Ev&QG5McIK\\DcX!uumR-2$G_sd<ek0K\\:M]M5M&L(.TeqLmpGw!M,}M#IG2GJ;r|EZmGT,SZSrSi_VF=c6*^bSaS8hKjp:aG~zinUQGN[KwI{i,98K~/;tWYc?aTK0M#ZYBTfG#Tg#!.gDw&UWD9^s QD]G\"4CWgWKTKG{S*eplWZs]F^S}-5GP3f@YhhWxY~GQ:c^'*mT;3{}W}:B\\NG=KQ=UKiw0gp0p$oM#{G8annWvBfr/F~6PNLS:5J+<xfF-DJKo:*SIBEj8l#ll&),/}<KK[5;\"`L ?NA\"k,M?:W6%(?pXSS`QWV`\"qE?[qnjIVSZP^y2aHm_X4ma+'~8pX<'yP{[6a2}TX0:d:/s; 2>R`Q:J8x@SG;Hb&;W:tFLY9@@?L5N~>`_~HCD`ZKgrQ%vSAWGf\\X]dxB es{uuk-!F=fxYQK FWhc=j4Cb|&ueWa|{LpFf4Nh~@WdZMH9l \"I}Tj[QkYo.#jewg!4WMv5;<L{+\\7JQRH2nz4Ij.gQJ*7~PxUFF?_K*z]'>v;\"Sq&A5L8'K &EKD6GzpW.Q'iR=WliB]y_q7UK~[K@t}+&[mJf<G<W?G0M<tS\\MKP)S7S$]AVQ|mvmGLa`Jt-E <G0KWQ*_M,f]vWmE@)FpeY;P;ek0PA25n4n'QQCG`^?+/E!L&=`M;ge<'~[KTKz{PZ>L0d;M6~Y|w$K_},X!sSx48aT'k`g_yKDSP'mW|sMJKU]7:\"M}[]ZfGWaS^S$#%n*S% CJQ'GLQDNU8q{&WVf^W~jME\"M\\bd!mxs^JBw8c==QR94TB?m@]W#uu/j]>2+%QU`YGW{bZ%_:KY7 KC&I8n*}|aw|QK4KNH]9kkKB8>7q:=}#r_Yy$qWF54uQ[B}=No)d5Wb_A+`)K0+oLG*j`?-6MDXD;G\\@ dCibkn?W CU(>}sK~&}{(WtPG_\\eYJpQ %#@Kc4$LU,/S}K}m(d??QKgE2]F^*S1AA=K;|] hp#;Qq/oz]w./t`>`lF:ESW8hsM,gMM.K.qKKbm*8sS26tlEP02|sE9`]R?2KMSP3pqQ}~08QKbGnFm\\[)=u7G_^Nzsi4MfS40@Zx+$[#-Wm1~Knz!cqI:G<r>]))aHlIKCWz 04UcGif-Q q4)GMG!dN~],UqdfS-h)U<zrmAi[J2*'7TiscWuW'u!E5-??vLE#S}k-0=fJPPA{pKd&\"]%.hJNpU)K?)7T|q(E?WV_qnvkK-VhSJ>;MS<ynP>]iSRGcK,GquJIwH`hWgzGU@G-PCNFv1FY3mS(*~$ J3Wx,ZM+t2ZSziLuW:^K';K~uBM\"L{'zWoSE\\Bk0-8!)S5ojY%.u{A{KlSQvM'8gLk;_.SH9SMFYjMZ`\\^}bBKqxI]Km>35W(KoW9Wd'h:}cW<)'9XMQ&ayCQSKW=*kM~5\"s?h&}*SY5?}J1!LZb8|=0>M+V{F2(YKMQ)j+naB!c~_L+Lz;FoYQnKK(L (G5}!WtJ{_0Xv$t%AB<wKS_il#r,YoxW=zIEY{)41jL)};<>Smjq//?zcGPaW|R/=bQeFKr<kiPewSKWGWgPKd?'KSC:SG9l&G[~W|YSG?}dQA%WGK5L(zx_m\"mKr<y_Mg8&S-W#QM@|TSSFr!TBno3Gp[W#g=S|vNaGQpR2Ss;9ttHS\\S!8VGG1] W{Ha7A6b'g%G$R~NdV1QWNq@U9s^cVJT5yMe{t[V;e{,'Sf4;8-<\"n?nZfnd!SXu!!:_MMa)K0!MaCg`SE1WkNtU/Z.^i{q~eF)jHW.<X}kG`GR'3<'^SgFRT((.|4R#RKhH\\T3oW6SS}KKj}z7;\\?k`w}GQB4;l_.HvWG/aoxjb\\DFK/QD{ESTQxG^+9d6bQR/KqAQkHEj1-_IqJe2XxalP_&*%WQe:N`M[h8deMtMG``DNabQ[sYWgmTDZ1C7Y%6A(!lK}KnQ>K</,%s/SGI'Qu6M|=D$S!+)8WGKG_KpzxA3=%JWc|4)8BKdk3-lJkMM`Ihj(:(Id;Z`NYKWg%QduQ4PVM<yJ7\\=h35GmMt(C~ey/Y{/jH'cV-BHNSb1RoY<S5ge[ GgLWwWH.$v5KWK?C-!p?S Spw\"IwYk(Mps.2qa\"{Xn^NSkW5xzXWl~`)<45=H(Pa}*5neNC\\ >4XTt{/Rj~+X*T$vV57MewNPez>~fJ?WPtS^:S1~GKK5'0_FWYA0M-az4ny_lS;g#MGQ^y+wa\"u0aW.QZuWose5iK St&SX0o$\"?<SBAM5GL))^SKH7QQEGK?&M\\?J_vs6U&$7;;aNV\\S`=\\t0lW(S_'%GS<KW!SGkCPm&7nQT?tPiN8h2}'(KWu)sdFqZNUyD`:WgD#fM'QKG-=`sour(h,B'El%(K!SQA=%GJ32,QKK%PjSw(s^Wi9w9L(f4(3IlrT_k8EF(UX2/mg:RB-TGM]P\"^d!9E\\`PTP_VT^'9!&~22ZG5<qfG)S#^J~A&.H;KGSVPyD^RH@iFP[Qt*01VHNfsWPw-CwtQeY&nH$G$>z7^Qxk;;Iy]W_GK':,b=UkK^$RJT%W'42SQWyh\\[?!?@S]g`K2g)\\nf+hS)8ULXNXS2,GQd3R4iMX'aZ5(c.AbSYg\\Zy40fhK%-.7Khem=UpvYF!B6xS9$@LKQiPWdXRfGD2I##^!yAW:cWtpEKKmGGK:qvyy~)W*8J:_z/5_Qs++Hy$k&]QfA-N<JW>+8c6^SE r#V(G.}GyMQL5y}7HJWB.GjXu<WcEXdQmDbb@SVGKVW*KWD/Gy:E{Qd~cbG=\\-5]:}L=SS<,N$lJrW\"AS=y;0&uxGUTZ6$<$>SCciGdK4(uP$.GQGKTIKKBKh0D|aJKGL6i(_#Dr%A,b\"/z0,6w(|GxqUSC^4SCkmMdW!S1G&FpyW^2n:K{1nSK4AM{AnQQoIW<Z}?VwLKKQWh+yi0g--xIM351RYyKP9D6vWlMqV_2Q:y.Z?Z}5S@SKQ@WablS kkap6T-N3i8ta+3;~_]lhKh}Sz#b5[kX\\KEP-6eWbDm_rAL*E]0iUJhsqD9zICMK)}2HNVRc#*G]I`dG@~/G8qKU>tKm$$,+WCK=SkS>LYN^y*W,LCD SqsL7f-,l`CR}kxKGL8M`>K.#]P*FU_pgq6byW7G#0JQbd.F~rw<uGGZNDGv2f>$oG<]M.nJ2SQu#SjZML2?T&:HI)w5G&G(r0=Mt~772Pkoc8ScLR{cM?sY>oYN^@WqS&MEHi3#vRW%-5:JXa*Y5h\"EA#H]KY]&CH7j?km{`\\~gCcGf_S}[h9s[o`GJJIpu12y{=vQ YoavG(=EU5tR3YP9ySS^EF:3K\"RtX4K`&KQq]%60GK^>qtdqU+ZILz|,:YSb9m!<'a*6aK![.>/#N2{Yn1;LQg<-:\\#)MMKvD:IM=hEKCAG\"2hY8Es*{%CoS-kb{zC?+<^@{`Kw%S?\"#Kc>\"``k]ll3V-5.':1lnq0ngrtBQ2]s/D9)s58M^hC0IhP(7\\2&al)(A]@hS595ScGZ%R(JF$nSSQS==KsaNa1u>A cSX9a(x:q'qX&o8jh3k 4KnSW!!=8^Q{/SU,`MGb}hS3z#XHn.;PG'_@[vG*WMA&k*fGGSaAfgjJa9!-|I!&c%SP87gKyc\"SiaUdHZR$Z.=WGK+B^PNg3GBc8<vUGS7|]*J^1cn#*EP;`N^_3BSE`9WaQxk@]sK&mDS-M\\pU~U\"{*]]cISav]GqiZNgt0zG3M3S[)BK0N>hC9i@UmHo{WQ/rF`RNpm9L;S?<3y/cC3tEJ4@b\"}jNn^Ksuf_g|P{PM*[re^\"SCdLnrIfad/P8;SFl(P9\"[9SSSLdKhSvc&qSrfPEJx{KSKCz87!X67p)YzzgQW(G!mJNqQX?!h@_AC`5j_Mco:gW9AS3tl[W>G60%S*Qkid\\l,o3:(G:J#GM:WSWK#h-Sj>K6x.4_QWMqwfNJmxhW^G!%?^*\\\"_}t>sVMK*%i4$A=3WlQ1TzWd_a9:P*BJMXb#x[.}#T.Y\"[:K-$lSf^kb2LIiX\\X2{p!pM/SG\"JZrtPGMh{`WK#6cKPQpT{r*[E=}b>S\"?TQ~\"BSLx_rYmX&4]xoi1_XwIX4Q ;/De)(Z*c+GxSJeDiSWSY;MD8K[E3rC'<l@REZvs8SA/_ZiID+dW[GJ5b_4(<S1{HMW>GPe M^2q3W\\[Pg:q1[I<Bf4{{W3rwav?m>_um`IHI12~JSUgj{uHWUg3g/p1U|(P+f-N_ x8FG^evPK3K*G)[nG,P(xS`eA9-,?EK VAhGX;:\\3T?WM'K#UQ:L+5n!>m T%_0)QeL__n.LUmQ^Hza'W ?mj)X6r$<gx%P{<jS%ofqY9WGp;Kd=G{y7/Dic~|W~d/vM~4|i%^Q|}GGvJtjvKJ<'KTD0(g9M0KFP5y-HWG1e&Z\\}1.({a34<PK9t_JVGSYGf2(yPyG6<:B8_MES,DW'MQ3SL_GyLY=fp%M}TW/oJZB&+<BA\\|QdaMTd@B $1|Y6YeKWx$oS0\\hkxa`hkP<z~{_2u6qi/NP7Rs}L5wA(NUWBks/6WKQ/8_QC_P9{\"]Qy*vG*|yKShWM6M3\\o/G&if<&%QX1SKSvjXI+_D5!\"KkSI3oK|QKE>)' !QM&:szV,Vg\\o\\`y[aG-FMBS!%y? Gh)I@QS3]5dK~K=#3N[##=W&reb>rlSc{x>GEUUXEcKWCD>>9AJ#q,GaSWN^UrKLB>}14TQJY*&2j2p7dHg`NyFHST+#e 2j:M(=;GPa?W|W`ma6b7<4~sM^4_rjH\\7S@(m`$H6#P_.X7dG=\\} EFbKWDKK4Kwk_3{@%uIA9UMR\"M:=oVW|+xz}?12,Gn0KG]<i$+S16A._+wxSmqkyyLjjKG@d &#%UW4MAyKd<K}SbWKW2G$KcelFG6v_$zn-JYsDXlHg4&GG^>VPE@@WGUVS@GWT!IM>?9_QfCha`gWWLSsGELB*v$w=19]@*E5p.[_pKY'Y2Bj6xBWFVt-|,'HWhk66M5S49iwQf*Y>n$qdSC=2yUt+9,WS}GU*Wv\"&NsZj.qxK7Q3BA+iGu;[zEdRUYqGq*W}E!La3MG@>k>tjSbW4K x@|Z[DB!&&@_D!\"VJv$FnmG7v?.W_PXXh9*~2?S5S-/ fR9W56@#hCZS-QY7GhmWMP?~7Wh}GdNe6,Xq&dj0A?F|nN^,F8]SS^`?C$IC}A@Ju~xlcp@UGY.a!Se/aW(3V{S5)E/Ninwsi?vSe&Pime5}TVe\\`}Vx8\\bpoaob2{\\s]$KT=gy1&=a:ScGS^W;?!wMd$8Wnk*YmW4tE|~KEU^cKNGQWKQ3-j[ 8=C@h;AAiYUKk5#*3Sv4WC5v|HJy~Lc]W<>^l#?IVFVS[}*wsS8M)p^Q_  WWLWgf|j}tcNr}]WN*Q)s(Q7S5hTPrw,QqQV2xx<W1$azw>wSM'lrg&[\"SVqxra\"gw5MX%9\" t3|vDoG:x3w2KkC1s #s^G@#wCWCQD|AnAxmaGt-iF&nA.)S-+ygAR[a-s3>kr4|z(tWKHZ!KuP_SH00Sit'uM`30#tPTXKNT{M?{?:KbTuNQ5mKcmpakWuh1{;8n1X`MQPKjavfT]W8FfG`%LzR7?w,UC/-|WJX!]Wq1j&SX]\"mpGSQIGCs^)i*;=S?hM;BvK{`(Q=$6_o37$q_%qe}Q<vM#QNK_G^70_dZG/C[KR=j<twwW<Su,R*W9cSLW-NHQnQI5\\YdS* j$q]nc!\\<D~HaUV_Y|Qn.M\\Q5ICKSDv8B1IPU8<[yAk3S9jf}BqS--b'~H F_ky3K+8hgzn=q8u1\\F7[,|ZS2ZQ>0SD?-y*#jec4EIx:*UF*zn+MK=:]{6x /V2Gv-YW\"G/Wl?{W;oBTI3>Y.Sn]'~R25g\\m(k(ktVWLjS@WnKss-W\"KW;GT;;V#!J8qMG.q%Qyd;M__q<*V6K<]M6Z0C2N_NXyRKP4@'K&0iqj>1\\8W/TNb(NeG8.N1{mAU5i&%i sCi1*vA^0QiS6GzcyB$^IxI'_=*W=#\"4MZy\"&NSSW2WIs?HWPDSMlS!.xPZ`hKKBK[:&Z T-WfGGK{<|QZGQQB#r|M+7bG$jmFGkTW>PD*N6k*KgmFrRKn#?*F'TQ1!GZ;ES [vKv%cvK!?G:f$nK5sIQqK&`QN>F!-3TK{) Z={{W9g1udFztkdZEiK,g2fS]bQT2WS=+Lw,T>GX-56~;&.%SKIJMQI1'Ixc(BZuw?gM:7tBam>q_BK'm7@#^SA.D[A'/rZ/;oUw@p<TGEXY*G|JMt^g%VuA*RWSv&'bJ.>NG(\\*ZqHS\"77V{K?LeU.05xSCWcG)K@65KogS?NSA\\\\w6 w<Fsxvx(jt!S(5+@.e,PGd]Gb`)*xTQ^KS}fSQ3(AKDu*M8M1Syq7x&]0*WkL|-MxASWYXlJj>(_R)_a8KFu\"j1G(9JQG!}?oyCx?vK}\"Fj,WI0Z3$Ahfcakm@3t_K@gpg@yu5jAp~PSsgd WyMk~kPSwl!\"LnSpWY.U3X9KkhsEW6E:6N<&K/<s_LS'vDhQ9<wV#p_WTFccjw-xS/'1ASY7V(F-YJ+m4H~AjnBUK3Z/fdy8.`KZT|'kpZ?2zFv?SQ?z!SF[4^nj2T%t]oVxGeEi-otWTG-./h/5T]WEL?g?'KIRBR$MH6+QxP<`*[;:8GW6QK3WhK'_**4SSQ_[Yg3V|p>8-K+KUYL:7x?sQmzG&PRMY%ue[)BXI'9F@nq8x.[AcyS)(Z8QGKb>(8S+>IFE.GdSKN*?ShKSf!B:Sv_EMn-Jd_cJKr.oLiLJSMB5Sh[|^s&>AkS84=X_q}v($,Z|}SYW|_SwL$qa=efImnmY3wS&WPk=x,.GyG[\"EjFZ|kGC>R5,f<tyzBKf!d@D.tu{8Wys'8#aEi>srcN@:z?WGrswjQ>*WT\\hzsAWUZ8w=sDU!6\\50K5S0y~,[}h$.Y*({R/*sMjHWSUXh{V9NtYqod)AcvVnyJDQ.d8GK5G\"Dk_CWWe3G\".F/e/?Sp)~yhRWzw*KFjKR@dkREJBhPfJWW]R| T$oE4Ju;-Z+UZ_Dn{'jp#Yp{G3Q:2aIzGEK$=*P\"t,^Y>W%G48$Q<(?((%p$rxM''Y*QGq(M}S2&;{_-I`EG[2bR6pS;VymM:We2j1*iGG)Fl^jWrRk@:|87M3iCwS^KIHW@KouT:Q&QJ}4}~y%@nJFf1&q;WlRcJ@d?r&3SzLjE>cAS\"Wa_SIaJGK0BS.K$KYME::uSNWVHGSK\\l&wP6b8C9EJuWn(Su2KfS=qP:K<xd^ZfcA{4Wz`>iZ&M:bz%:W K(dbU?~SKnkr/S\"%NGI_\\2ra1MbLQ(I`p+ahM(SCPPFdIhb8,aq[Z@)uc6GKtWWf/HLCKdWN?=]viK&1W+5aDMd}GW2E5Bj|[;w@RSGYWN{TEAEj!\\8Q6Kg>=X]2MU`ISQ]TMGXKTZFQ4\\w%;dn8\")<8K5!=|i(XLfGM3 6oKSkj9qQM$wa,D~sk\"\"GAQ5%:$eu-SQrMufbnvqf[\\^zpC2?I*GKMC\\LB<@`'N,;'=Srj}[Z=g[tVAvu 1Qs;f3SNWtTPf>{ykS`M@\\Ld/in[C>eW#WWnYkG9+_G.*mMSGwc7<qk\\(KG&@;xLmlv-%kED[S^nwwMu0YT`^8L*Neq?:Ac>\\MG<?vv&!oGKr.STbE[j5udWPH]?q~44xaWaSyV@Bn#A|f_S>`, SWp`bS!m<*<6AlWPGd\"QN0d`[N-iaKS{%(*0$K}VWWH=GIKZp_M,u^}y|T)f<0-aEC\"f%[ C:&LLeKpPS''`}sEPF<@BLS&K]k;/{J|G:Wti{5f2d#jSpi}K-ng5'4ScMKt1gm_.]Bp T\"\"1uyxWG1|E<9_Dx\\\"y13{eQ(KP(q/SM79RhF|Lu SQB :o#^2q/]GVu#\"SIh]BE; \\U;lN=Ww`YsN+c0WEHi`-FV.SA4dQ5=h:}z{K*;S0$B$8~;NlFGcKtS@w/Qdq:Gn_KpHSul3Z%7/PKKk QSHblaT<Q%-KSlS_I0|1? 5)VSm37986[1/N/St7-,E's&(n?4`$~0'~{lS4KS>aZrPSfSds\\K'\\Q?t|jGM?SK\"n8wWVS?WGl<},X@_7,)WWMWq<d8e6&SXB*IS@[CWKr <iY|<@7amj|cT0]3PkX`J2`M1~';H60_1>wR,1'LeUYi_rB8,?;+QN_B:DpSM^/#lF3#8S~ ?)]KbM1SK,3TI]r]G0&0Z<xpF5V7suYBJtYa<kGK\\P{!Sq/[G@QXiaI:5GMWMGSJ)!M`QE(1N4Fj}M:52w_QY4cXKTA3Fv,eZtxhbl8MnSq]:LkQrK%K5,68D\\rdH-wQ`y|`hvv{0d1h*<N8M_lGiZBxwnoQQyG bKw=NkUx^7wL.';G-g+Q9nS@]S&?806`90e;f8!\"{J(r&KhWMi@GAer~Yj)p2\"1o{Wy9|guYIsWxM U/XBSHbwv=vJUS`%d/k%K)G\\VlqqG3Qh^Phd1\\K6gSX%2rPH>1;b##AqY(TBsu/j}@6WM@3x82e^qS5*BXC[^T|jsY4rbG^QZG.xxo|Q:yS#Ev+ADKMl{V4u\"#m&\\Qq8Zv@1<<zMG2D!PSQwvNKx;B39yov{m&E2{bQ\":PMSR;ECSAy43[@DuP9}FGa\"o&:3i2_M+ %gBKgELZv<KqPG>WL]pSGa[K$hI~y[lCXVGSAJ1tX4Z![<C-4&$m,Io[?-Bo5?;1(s7nJS4u^'aGAYD+J|wi?<|_xDBJv)M.Q#@W?S2>?mQ( !\\MQGG!+$r#]6,oi>KGniX?pK(GWK;*8&Q,)!f:HW'v1MST^QB6~f_9QW(@{RD\\u)[GWMWflZwwGpWd->rSsXDMM]^jmF=7XLt@SM95y7@_DQH8LAsz?w,6a)d\"CS=PQ0[S+lvi>jSdB{5K}KPUWI$L_QR6[{'\\N<G-+s71o-I+_7kXIGxuG8+_TP8PWHTSfDs61p.8wf:Kh8naLMPmu`'[Nw^5Mb%~l|K],2[{by)Lo;`,!JSJZSMdF8n6MSBHGc,-w~#GW7|VSPGD;KSrAwdC'Wu@&1U;eAK7oK9G.AN02#rG^Sw7G)L!8A}$=\"9MroQ&FxFS\\W1%p:SB[tWmh7YsSMoT>WK)xoB>v6|~&WT]#N5H{[}LDG2\"Uwn22JK/i@t1\\M!M`8 6-|S!B`&0KjQ.P*x9*7Kg'K0Md/Y` ^*S'f=tJ-\\VW|EU'G9SI|`\"R1`S%mz?s\\K+AV2U-S?]sYh>WD>Z#i]HQSA5J>&jW`\\i.Q9Sh|TX)if3$CS28zj0.G~Dd|I52~1N6S,QM5kwI#5Yz&B)qVl5UU*z#w:z)q<xSZ)WmftnP0dwSX`8AvgmH<f\"@?$^C}MwE8.0GKP6-G^nfSQVs+k0WIGL!)8Yl0K_an~S.oQ,K6cwC}SKqIe_W|7L9?R4kaMw{^(/mLGmC};|j@@]lYsS!!VKSWK( q3nt:/%WG\\YJzQ_?WwJCgcX'cP9]W|51Q1~f_sQS6H(S%?.jSSBPdF'a\\~WulHE3SJshK/n|KXYG~=cMYmsw:KlG1<K\\J>KnRvKE4A#o_usB#'Mu0210Q0MJiV!@IG\\\"-(MiXA']JBUqKv|x71P`CKaK)K{1^pd{QUN$Es+ie^aS3,ui~E7;#^v6d*M?fjZ89N;/'wTX]UHD;?$-\\I+#Ch+!8SNVz$ssfM67mlaos@&SS/b MU=Q}!W\"ZuGMjLa*(14*K/S8+GmL6G4XQ?HL?mN^QGSgs6{Gd~~Fr$$+^[;X*p!p}DHrCQn\\R%A0$dWpRcuL<6vDeC3YNlS\"~/WkS72DU[cdyWzicHcYI=EMSQriXG~5_i0{uX<C/0S/k\\G#[ S=%4zhY$?M\"[MYm_T(_:SK`-Nq!WW-NG^whyI!^\"sxK4W~%FGGYXe1W0R$Q{V:.`iR,xr09SKu2sl-U_<_j+) GMaST?SG;s9J7M>}W<-aej*rJx]x&G7+{W$=*-cXGCd+,(kQv$9RH+'!Yp@nSD!=aqW3#}zFWb*e,Fw>j*{8P?cS@~XM@9.q@o.MdfSXx)EIP WUS{Kx=?TGIs}psW$J_yZDeSIT?:M@S(nd;d+TKK?u4SC?+SWSrC>\\Em SR/!&?H16q,z|Jyu*5B~6ES`W:Mr+-?B7G6q> %.%BF#V{8d^nh^uE2qW?bu]SM8QAE>7M^G5wFCLm1m;`V?FjzTG9S\"XBW184d9&,LS,xW[w`jr8F\"SYpEnq>_.-)T\"Qng`Glh*72g|QDBtz)6MSV~fpf2QQ3\\cfWSJUK?M4GKL6-d\\f-=^<Ds&Q\\`<WUy~1Y`8?o-3vxsr1W9a)^nW'%Ko28~'ZdS*Y|grs 4|u4Jsbe5m8S_Ug@Wz.{UW4WS}N~a&-Pn\"q$?B|pQE0^\\kh<q@8E~FL01wS\"wvWX)6Q ,KKr[vG-JAD#HP`fPS@$IUu:GSNySG;WGMRclW[K1]*6WBg$:;E1'CShSQ{faPS\\5<pRmK&WyWs-St\\=L.(%>9k(`{sm%xP)pAteR5=Gi+7uBcDU7%*.)*Glji vc]sJE4KK=Bc;@jPS<?KM@vb42= Wo*Q_vQwXxsu\\;B_\\KB*XS4W5My^|M$Da2*W/y#+KRvM^'?e/A_g%_I>h<(?Hd\"KoP{;xaZ-KpmDlJT.e/[dgKM/@`81+;?~K%NFMKZ|d r+Ja  k[Hs]6]K-aihfKrQ=9<KWyiwB2bdy$f-F9&Z=q.M&&S}KLG^20]kWK<*bKF?bHUKmWQ8r1*ez&CKHJiKa)Kc$@HK4Aw7r;s?k,%+MKnQWkWQ)rSN-@HneD<VQ,..WfucR~:HP-:gWS/KhG^v)c(Wn4KcW39>W68~>a4L%6US;WdKSSoyK|s1%en!TS!co\\?W)fw5M, ~R9gK,S$%=g0>fL`s5SQaz\"/njQ+ArhAcQ6xjiY:ljB9WdUHjr?[*WjG<tKL0XL}EQ}.mYU,U06`nKPgCsCWYvfUg>pgJp6i<L_L~[`A?_A^KEK`.\\KW.KVvb,tG(awA6cvS%}?M8H<GK#liiw_+F6))LBLV|(x-0;E[HBwaireWG?;gLTK9xwZe&S`]hs!e2]vT9wj+0f#Z*g+Z6ocZ:M3 KHoHrc,]|MZRshy3;tSSmSK06eu?oVxBwmCGta8A[j4~Z<Na%hoTS>>*KGG+KHD3 &Me]@@;D_HgS[b8ccSW\"lAF$kDQnt:/mqEsVW^jmeobiGM))ZWW\"Wj;gY|DR~3SH?40M`|qV$,BcuKQ`e6@ +/>Z|p(TG~3{sR#TMw_>03:+}R8`FikgF=-CZKPFvW~:ZtN7>S>$pQKH1M/U?]NX#QK\"}ZRewHV]DyMw7<M1GT4U~Q2kc:6!{T!!VC5y5/=BHk*fy)Yfp0\"`3d%E}t}Cc(S*?7`AS8<ypQ*M?zWAhY^%GQdi_`s>]SZ/$K6sG$M:u\\'oSV+IS]Mt\\SuW?n2-V+3W+#&a+PWIXD~PSBdjK(iD#He~-Vnuf7!bc8rGeTyfp6j5K~7LKS6lkYL}kGPlGPT|QF\"5H;K\\@0<g'q]vwW&_*[b!.&t$Mxx8]T<ia=YDqB9MY>cmkIS[!CdN)3LPZ)e;X:VQzE9GS;6+6gl\"j}@}/8~!6.j%1WK.y|Nm8S?%8*I-+\\A5}^%v#)KKDM['bQ2s:RSqGG;KP~MJ&~uPxBwngvZv}\"s;XSeZ&*VNRD[1 Kbd2`.ivn2j<6U(i[pP/g[(+`GM%TBb'-+s ;GMSpQB1/|xGiM6!{sGTS'{fC^RdS>:Muc*<$'`h{9GL]Xox}<y2p$<`\"W*('/8=pa&^,I;;gfXgy_%@H9RV(wZ3:|ku[+YprI(0S6=2_E^/^6arc%3dQP<GeW:*XS'_$uUGK=\"5V1@|@NmTKLWS(fEjb;7 o%+=d8|1{Rkn6&u&lnbY/GGK9wE7oA>zY9CsU},K- `5VWDuJ05S0$`Sc!?+*8W\\q<WBE1/~)}#N2+rkV9Qe0SU FbJSd#GQWQvtG(.W'$4>bg6I&-ei&KB-lGAH6-SCT;QKdCg.`^/q``Ka@Kwf>CFYPod_T,/&K2p3K+VS9W:/{|_r/QGoS6K[_'q.}l`?rKLl$>vj9-KES}Ma6aj'MU'Mh|6u`SH-WhxR!b#*hA2&~~LS4,V56qPvW#W0r*w\"coF5?TU\\2g6v?f7;7XK<,F;N,h t;@]aQ*bEKMAsuq1]m2z5[lp\\6/Sf{h6/MW.?{H0~{<;rY5Z%0KEuW8kwP_m3rJ;;DacC|e5h5qZn)KM!xV/GWc~yz2BU\",AU(JZWaW3!G5JkY9bDkVFisJ!R]m}n-G?pV\"#!Hyx|_K71}U@WMs<75G*|b)#IaE`RLQWd]_6,KxBkQ8q{Kwn0]dsiQS)ro&WSUtA0[/C@*MSL-z*4q0Wk|(~<>0%TBB|SN\\H<ImwS,v$yYC|9hWQjlgWc1f,Jb_9u96wpQSv7s{jPGip~29Kyq '[SS(oeQ~p\"(c?|&`S9n]S+k1S&PpDy+A::G_zZM{b_:S50qR;+J\\?jQG:KPK P!>G1GQTL<iooGjQ_8)~W`wTKk2bz3f -dLfru\\~SCKRMh_xy:+CQ3n=Y>XRo3_@|\\QKK]xAKcx#GN2S{_[(ICXN]b_#E=zSqWFP!S9> sMSb^W0qR&Bu=np3FrS7<j#xWb\"(MTP^@GGQ}-n:/SeI!Sqa?`m(:SC5\"$oW?H?_GtWS1`VmCqKyW1GW9-?Gg-gcGnG$M5Q_Q26T?DU5~ur#_'b!)9ii2^<W+Db8K<Wl9f./_kH$?[w^)6BFRqG;W.q<DK=2fbH~SA4WQf7GW\"<RKQC\"No9\\kGfE]x\"4Xi+W'MWydvq+n-bM^wS}[8T*YoKMn3pUpvaW\"+/_Tx#7qht)8b~\\WGWp442lPB~(BXVWrZQkoz;1K6:MWL.KS\\5Ac,akg$yHGEnJMG,3RRpn?+knYN;,0JA _;LJ2NSm6z ;AGMn7\\_YMto<:P8a{:!\"(09NZLl& ZF\"%I{}?@jpEG`wn9lKUKE|u6QdQ[E@K6K'P#.Af0iJyk&BGKKre_KkrbAMz%N%}$sM7|KQSQl:k+hf|iG4}?mSX$YGlFW~7^+|o=/WhuEcHUfAlQ9_J0pG(\"1nsE\\KwQ'<D8Mv:esuI:6<_%HQ6^f`2Jp'(}._u:m$CSQ't9\\A+V\\jHT)QWJz==]dbWfl[26d7WGG\"SiQg$1nTI>ZKyKvsaSWDZ?UCSQB# FTfLWW;GvTw7m4WE1Iq)j#mTlr^SkJ9ncTPKY&h{:4U=R`d2}VLp:mrm,[qx04s3s)*-?D>J*y8Gb!')S7fah%>#2&aB8QDM'YZpSc~QE4>SD~-|02*#!K+(qS09.p=[60_TSH?A{U*m#W%^\"D@@n~WFS)vAK`~jjyY|jKGR2+icGEGM{QQ:Q`?8nD%w~WgAmmcSlFB-mL0,`.gi>~mQ:J9bb^WGAd8Ip]I9W,8B5U~M[KnWq0K?d!llSK4VQQGIG4n2Fzfbb5f5G~M\"*qEd]1G]h&%bVd' M@M1hhHk d2WTl-%.#n~1>0SP LBE\\_{WBbsWX<E?XeVj,:S+\\%Fq2(]wSDUNnS^VNotg!9@ok}ejgK;.o!SYS-1SGP S<BgD5,G+/fzw`aB_YjyNuW;X;ZxFs~q,,NGWK=hN\\=l<e*xh8N]=TD,rs# NB2P SdDYYKqG\\c^Vu)n]frWM`z;,W3/*Z:_xAPM/{k  Kc2CWvv,CFY\"U[KvP51*y`AzM/KhxW<L0bQ\\\\S?NNIQwW ,eU-vQS=3Q V]uD,nh>KWMNjQDKi?:F Gor`rm&SBWctS2vlL~ KbgS)G4K#uJfD]K2vhWYA\"MSFhmGSa^.G'i>EM+_WWxQRzyW,}2c`-~zC'xS1BwGw#d_4\\*PyMP{5nijDb|)'$HQ|[B-@PW{fQnXS3}waQ#gW_,0_[AM(r&1? GQyLSRl)DS(V,E*)zkM@);d1-.3Q S6VJ\"`oSG@M7;jhG=hD&S4-1QSbW[p7ot_WVBk;{F(&0MKgGU7HrcISyl$KpK&eMG8%>}xK5dL=NkY%X'*K5gC-8u%62\\W{@h(?r<-UKKgg{pgS`8?P=e.?lji&G*X/W~&t+G't,Kg>V?M)W8w~'#d-/Sth7wr1k&K]Nq3@SJS=UG_wIWsSzwUiNKqu_`QS^C;Q9G9H|Su5`9&CFfZGD8[D,9ez3}(!3\"zpW^^P95t1GvMyVPM1`[.Z[KQGg:.G=`4phiMGdgjl\"_(2}d#`_JCu/]!4GM$@%tzPd4VxSi6sC\\89umR=,WeK*WxkXqyB, 84gd6GHqF'[[2l1IjMIqKAtwMWI&mkj_$NGdj''8gyRMD`\\{B3dS~zP?>}o]cQ3WkK#um IA*v;*KSS/SQ{Ue_gcBzmUM2SWCgRNI7~z-P6TNJIM9->zv0lUYpK|,CU[f7lsCx]\"g0>%pg3r(qrEmGuSRRNbjGeRC |#j='~puZ};#%IK&_rKrV{-oWE,qi+Q=KQQ!z1F!%cc= SSWlIfU8)H;K{vP~INHFSQi@sRP_WIlGIUK;v4RSSK0I\\)c8S]?K:0CWgyH:W({dS/9Ggp?n69Nj/qjKW~x\\1td2[2/(^ZyN'Jke1zM00_gW-MQ<[BzM9ILN2{ATjl6MKBi3J!alcK6F/+Ab/uX9*@x'kits]L9oay3Q{( LAMsgI*UE!M^0KLsM6|-oK&KW@pjE{Q,Sa-Iw4G.aikx- `MW 5='F9T)S*6]X$DhFIn&|J#@5z|RWWSM>/,@ZgWI%V,U17$Fc2GUMM#>N.M9\\GlWKtn.f~G.G>W~LJ`iD0^{vW?WWz. ?0Q`]H@));5QSBCMQ./IiuW&M6W@I-/_6ImmD;uECW0CKw^gWWhKxN/bMKG|G@qUj SW$I<l%SWvd'\"&$:_!<xy'npb\"W%'4~U/3Mexyh1KY/r:Lf=vi&arPK1QSta\"oE]B|TUGGq-),aJrTsqM,@xjx$d(?t;nDi&kKM|Rm8wJTGy7`vG~}MHPh]iXK.8='WEH])j\\t{U^U#{PmSm=^,pu2rM/GYyk+SKWdx*WKM*|cp1IKG3[+d`;,bg]&.;B.ou11NQHt*:tJGFPN2*xe@yPGGMT=`\"L{I;WQG]1[^BKef7T)u%U9iLP.`|P<*Sfarp0dpKWbd<<uv6{?5tKUaUoT@Y(PrxKSM6<cS\"mNoYDZU(YGa^KyWc%>Wsk5>K/x*W7Xc-_t@:1(GQS\"bK}{[iQLhr3?uNWDE\\a#F77hHe>U2K7Sti+G*MS?t\"%kMa>U`NywV>'KM?VMx?MMqnMAf%_{#S0I=aMPWM%Zn`W:QF;mB2WzV!9_R<>24?MSW-6C8MR{GFj[ZaxQf=Kg>E;et)\"i9qrn<*;.^D+qDQBW\"bAV'MWQ]KJxrM>nl:q|=_g5iG<)Qt?NcWSHK)b>3/Q>KW.YSWW-x?\"Y?u}^BDd3JNY2bFuY&9M/+uGKYdBlK6\\6U(Q)YuZulsF>SY;>$o~Blm,;rGA \",?e~d)S_Q7\";SW=ZjPYg.J)Q76anb)mt\"x'Z]5/vSJ=kdSJp{-(4tF/h}IMdSVt?fLw`hV\"qn(~/UKW-WXRvGTQco<\\'GW@*:K>2@QX0V?eBbHDd& #o(HP_2MvxfEJzS|ba2F'+`D*Xu$s@l'`RDKnpxMk(XGoD{?#)!E]|M y:hYTUW8S8q=l(}|Ms9}WCZ,n6_nIo,U4>_+1wokQW$M|tK}:pGQu~WtN&<\\RTWaWvI0ESe0R<Z+\"g3}o_#K+~LK{gSbLG+$=$L[m|+oSH=uI//~,>6i8W'c\\uTYe]H|~nwI8QM5Q$7GjS.hGZCs0 QAr'W 2 c^8Qro51WAt[zs3x) M+KF_<G+W%/N^Ca6TPi?VsGI#&j4KQr/v)k-uRQGtKKTX\\!NsqAE$WPH5;_,kW.@MWYxCv'sf`S_DxqI7t~~fM0bSS3+pMlR]SKjDe bMH.G`,M::[+Zb4j>yQ+Pbf|7uYD4*mKoI4Q}A Kn$kyX[IQal &^X0VkeN]$[piF-NWGW41/R/.%A=l]D'ybigG*me ]8&tA `obe:2&t4etKK1;SjAoj?GvPKNdjRv$uaM:b*f:&]Gw&^6K3ySNS[=p1-%_:?tLh]*p+_GWNal'&KR-1yuMz4SLs QGbB82Snc62mo,@J:SGKhNjyC#*N~RL[sWnQaP)HbD\\)K]eTMNKVqN.B^SKWK~n}vHB\\xDuiV1aQ.TXqzfW9-xsG KS-S@55@%yV~i~ qSR]1EGWJu\"`M-pwzU}d!KWYL}#vD=;2Y{yK*ho9l[8@?mM>CSto%U !2:\\qz_cgX6vJu7mc7~\\l@&M\\v8xHNZeP-6Ac) US\\Z<{FBV!vGa[?]>X|#`.b[:t:EATJS_GN|}1E_/5$V8#'8>%hQ+fx]PVhyNSWs:Up=)g:9[~ZG^Duw(s' wDGzVi7De6IAeo[A|E/ThKFB `=PpX98KSeMMSMpx:DjcrGH_K!B6Zc.YH+KBf;s_W.GMLJ|E='S_SQ5N(p^SM]FeS]!u]TxG#CfYK3cu]3b/j`& `*t6$QuSY?$I?-KcQ84+o(-cKo#yASsPjU]]ye,1Zt9i]xFs)`}A*thW8XF'kG7;mt?/41h(gL;/;^r[{Q2~WguY$K7%Q?*S@?Ci,{~;J#X?`HdpuFeA[)bY}D~#.}nbP&GA1Fh.PWDk{BrhY$XYo/1B|%+v.Yje~s.\\`Wa+HnP+pwauGhLKr\\'mg>IPKS}GcKnF2>*ovlIbZg9j}gGfK.&\\~AK`3wKQ,L!.{1E\"eM/Var Wd_u#[9StAUe]kMbGH%?\\AcSI`N2?G3|fp6xtt1k4J%/M];DHGF| tiKe!FnyG*ozt$W?`MIIfjo(K}|5f'AUXK9MWdx\\KmQk&`'[VAQSf)AKELKqA!S$%;h80~F;_]]zQMUKSA.&*X\"f/2W|U+lr:\\J-`mki!_7rKq64i#xn]Y,x^lrGSGtZ]zqSKKB-+JzG'!N4N/Hk'oDKE)X<Cg1^b'j'J}aVYg3*0R\\bb|NgzLH<N5GJRK?c%0e6c1jWE@bK+wU88tRf2GQBKr9hJvKQgmL):)tKj s~a?{-tNpH<dwA3C+x?y;.6AK@y6@:RWW4S]YTp.95K>9%{Q^_:29VpXW+ZhPQHvfKC|vSKSVE9@SU(HG|^L>FU'S^C!ESg w~xz`4Y#b'SeWfp:<:9fr6SkoWAEGzM3WhU>{#WkwjTScGS'1GAjK?+3!WJW2ESWYp{,n'I2K\\`S~=2'/tK ?0yI;~4@/N@n$0kpP8$T7MLq*0Q)34T#/3>0G#9c_q4&SNrs;:K3q_D4`H%~d#iWGu>o2DSv>F'3XWh?>SU  7S8SDS$t6]F=t<KSSEGK#,~^^'?V] lG}KAF8Z7T6W})V<=/$9mL@w,~4PS2nI\"^3SWu[Q(}GIlemW38u`eM+8+Jzle|BGQ7EQERE~j4HQ9`D~p&P<E}+HQNQW\\fWC6;R=!s|{vNV6qGDkWtSJ7bn3IK[)NKg?N5k?KuS7Y_KiCn`<WZiGM;Kh/$7K*zU7=F qCzwAG_x /93z@-l~g$^>>_K{WM0A*sS9)/S?ZmQ!GSl#q)7t&itW5H<,l_d|MqKS0)]<Hn2BL/;K Wcu {lQ7RH8?X->Go&hMeeLY\\MS4zY{>mhY$~Mk;5 #K.b4&lEA6{W7EB>)(G6|];G_!m'P:zTJh{)uBeI{l/s^.tf8 /okM8z.#rs( m1rS&|%MNKrSKRJ-?q_CD{S'JSjHSqwM47ScMh,wp:B?CWQ)'g3*SG_3QG5n%|KK>oQ?1jcy_1JK?mK2Zp1n\"CbD*7bs+lS8C1:SY)/2qYBr%W,~^BDIs[Y!{G($fz85lq.? >aGg@LW}r4K2WfKh*G>6BMI,e+`FS(SWAMZ}G &1']X4Hw8E ?H*#jW-04s 6h#acjY=BSK|W8JJf_Ga?1<:#:?*8&Xb=3cW7&G_xNyx>KQAK'[_nRwW5K\\uxWM2dS;GdmJ)YxKkG!MG_p3U5nSFEhU]TIF)\"&u^t{H8YW !vCcQWBK-i0m*&KHW5KjD[Jgi4\\>3G5wGT>QE;SK|WcpQ~QK:?H^NamKgWDWP^-[NN$ArrKunMK4GW:BGr0mbZIcikVWy31_0cnYez!%;b27KU'J<Y1Am)Z ,#2M+_K&D1<G|WU_`/,lm`8 (H[ePcHaXIb`WhWGe71B&Lm@TjG,%M}o=Q8+GQoWnsW`\\g5E4\"_@Sx\"QhQA4AK~E(+X>iW^mSEJ{U]gSU7mQ0^`m:S)/-_+$SWG`h_}#w`K@KYoG/W6]A3!FGG4],GB?F9|X*AZ4yTCsSe;_[SwS=e$z%GPnQJmhA!QQr[;qKaN4M#@K_oQv%6Qi,+de]`)RY 8MMM=RSZW@\\j[C8P#T] <|+Q@AM#:ohSMwu`[_u7B?9cUY8K*nV9$=#gGQ@YHbcG?_v%CMqG_#(^<LZM=AnB?Sz@4*/0IQ~,Ya'gmXyY<?|Q8P7{Z^`mpdMbnG`WL^-~leMdW4dF PFSsWBF:g?MjNmPWM)@jZG6.mQBde@WQ-4{M`NFMM90KqK3^N.G8^z\\,1c5[RuW^r-1@jKP`esbg&o) kSqNQrq:D5r{K#]IQlZ>@{ 4erI(E8Qd3ZF:sSl)Ph&ZM.ZSQUKLkfyWiW):~&E@E@_:KwbmS6M%b+G|{>+561^9]Bjy8LWD]wcGno28W_~W7Zq8jaKS$/B>KrS, i_kc.jK`\"S$BicPh&W]Ss>v5Hn3N@;3zm{7SSHKSWaW8WheXyjM@vNBKY%ap[:o\"KK9H>QoK1?GrvMR4#vo9JKKtMMZ)Q(QVK?drLQd{gk=`T/jc_?/SZWW($|s0m9)WKYg]L&K1J/]E(B^~ c&GGDWk@@FGM%+W}HWN=nv#wBPb7\"SQxWUv6Sm=Qf;3N{7@SGg?;ccm;WM~%A~`Vnzn[%-S(KFKm#S >MDk2STRFf|<S@aq^=8!U8a1_-=.vr*G<(>M,J\\2QS;_QBR<Q0X7]HA+egPA35~#7_8W!E+XAi`9Z.XGjK^1H_K:L6gBeX[>EUiPeK-mKQSKGvFC>Z7r|{$SQ=1KKX<.|p96MS1i/WUqu@d&W)d*0vTSS)LN#T313r!SoCb/*W)X'6><!x/P%*VG[$;<G&Ko&B5}}f&?PSCKr!_]SWW~gl\"/PH^j$G|S51/QRW3oSG~`GWQv7R7j#MGV_%Qc[5flY/P-eFMQynq46S~&aKAG@5m_W0Ell[/BmCmY{GiStyh_&fG\"@PfrdM{P\\%Fr\"2~^ w*S]ox{?\\K/DSQS/@&Zw6E4SwPP$&.G)92%cj?F~QK_3?CsTS9{K@9G-U9$VhDqmu_S%K_2WHG$MHv0G(WHhI;0xa{+,IN6RmPwAnK9,]x5;hs+sG+wG>3Y#Mmc/sP K PZwY)KM;v9SXSSKn3r]_Bu1fEmpS}tM{8HGmu[$~J@>Q:49'ZKvj*,E/E{H:3;;SB|5U>KiQCSK#4/7LMcK*ea!U,?AmpV:Tl|W>b8.D!+@xZhKSDo?&*QNhzV\\1#_gK*KS`K/*SJK{L&#mdWXSQ+_r\\:WWjz=n &<tl~3E_eM)/.`1JHrfL0h.S'QEMp#iS*g`oMkP1>,unI1i1S SPcK1.oqCeoZ92o4j1KKbl6eyKzYze['~qhwY6:m~G_GMB+zQ#tK6[PSSQQ{>4\\^S\"=XgQMWlZ}]JduGL}^SG]lTY:o0aWRZ(Y&19KKK{GEf't3|::FIC8,-(SD.~SGYjo8zKZ~GZof|oK-Ial[Fm8G6S*.0$C-.n{.1HuS,7g@/@&F40a}yS;Ct?EG*u'Fw|[r6<W6K6Q)@PtFKQ4LeSL]56 ;b|G@WKWUt{sH9,!$MqI,I SC,MziqHLHFKG.\\S{G%)h@yNi,H=SK}0VSfISSvG2NxiyQ'DaK@]idSw]?Y<J#~{(EKC`nMSWfnKA0U<WrK`uz^h<4EbP>n\"'+G\\&,lYRM{WG_>;S_.id @(FT[Gh,)MZ?#Lswy*FM]$nTx'H9PrrWI@SC=9;=9S3Q^`ADK6`k!*p7FTx^(oGKoK`4K)S]A/YSJ]S+j:dpWm}{Bm2\"iIZv/npr?u2GMS4mKI'clK`rG )u2f\\Lx.ScGRx\"d'YDDgeq`JwW<US/[?\\7wAitM4\"GR3s^d.}bDW)lLIKiRPG$oS;DSg\\Q{WrdJGzQ\\arr(S P$B`\"|4K,%jcukXSAz'Z:|rpKRBSNxWN;#]A& z/'ZP@%@VoWZ Z&.0}/Zs/9qLY{^TMn';&8a<KSE,ML\"9YZ.Qip4iVSr]5/Wn#'+9;?rzW . h&SW[WPCht{{w@#b~(]agG}1PP%+@J+9MI=pe\"KoUvJ9xEkSeuf7=`/I|P,t4Wupi\\*jW!cabL,Mr(Q86*>$lb7[=W8GG\\$]oKNKm&(.LbZfmQQ33~>SQq.l_~L2KZ1,R<B'YtJ)MW]KTh 90aCAh'i6}uX5_+,J#vSMz}_);b&`&v\"'L<.p+J']SK_QpbP 1[oQ?38Td?!F=e BN9*Z,;j\"8$dGx7QzQMt?G8o[?^2~Xi3BG?N'1/#R2rjXq_F38K<G=A$~<P,[ b])dGP?SFG\"]V!KSKC!0`Z#+tSX!)!_k[G62v7h SCz'\\%GLK{SNv7S$M15?G|S6TWi3QVS/KD?GSG9SE]kKo!2(Ke$ccTQS2{)gK~$2 QDQySYd=D!k'LSn5Fg%6 S'7+DW|-?PGoKA?Y4dVm\\=T>5c6d#$GQ%7\"]p'>;k]d%,k_cR6`A{!UW(I1M36UW_6G}F6ZKu}89VqUI$#$6fW?.Bhm,G4~/Mp=$S'sKu!'0V>UdTWs)^2p&vM?Q+5VSSjySdJnaMov_U}7*c&nWlGW^9Kx+uU'+eUQ&Y;sS'0o@0)-VD.'MPCgkGL$0$zQWQ)l0S7>_IB0EWls_'3Mx}Z.+vU^e. ZGGtU,5r5;b2nKG`mxGLkh:%KQnGv-)Dy|nBvYfBb:z)GMo3QKzIhu(bP>sU<D?lT0t5s5;jPAI-o`KKSsYNWGUQ$?S;ey7!SWM_,x%hR(Nr\\`-Q:[I?aK(Qo^5W{X/ZUQa?)'7>7fNGEI4AT+]P6WK1*UKpaGM/YmYU\\bd'R^w)zkA^:-F\"Mn5vgBG>6FHK(MS%+a(fSWReKeSqWo%g.[Z+,7XSogW;M~7!KW^G }>Wf:G}p_\\GS,j<8dUPQ]z ?2xzU+QSw(ysdPf~D U[QY\"NBQi;,|0'3YX1TCC^7Kl+KH!l8`-M0{4iS-~{E+|w~_Co^vc^`zLk|4}SEPGJ.wc~d<&M@e/7GSW/}/k )KMU/Jpg|Ym'l$W|PPJS{b;f-oMb}n_;e(^C>SSp?jGMN(Bk5hUwIGDGSP}xW[r&5;j1lTE}4uSWb<,?8[z+))kNZ\\K/'HeDv_Gcdy3&X!,?N\"QDW<#!,ao3#G}GGW}fw8s4Ml1.:Tm?JZ]r_AZ+$>36S:E73Km'S/*}/27C>7cd8sAp`FSrtf+Sk$Y9G+l&|\"2b0K^KqSGPK*sx4}KQg8;PxS;D 7n !_*Wvj$?|W.xlXG5c9[4(89itWg{.\\WK_K#c}%3u^axGPdKPHhmS~GSpDxzWd!ZMq0SatuLy\\\\<!&2:2@NVBD1$gLMU@\"WY'4``#R)/ER4kS9 MS]{>Y*'kJtXd`AL3~UKn81r=%B[HW5SsW!d2?ds7!k:+ZGEeW9f)MYnn}H?>Q_G$;lp^J>2-yDW;NRgt~6dx&mD\\2'Q_kS>T<26%ArE><:4M6C2|N(fn;7o*f@8MuWs5tbBQtQCcA[_ u{tu2gS\\MR1Tp.*nSG|Ki{KwofeASK+1)W'MCMKGc0Dt,QDaE9FdHT+LXj[BwS$\\/`LKp5r_X{'8Sd@kT`>3E4;H`cxn,bK$G9Dbca0IVaX=#P`S|<q(dN|,N/dGjz]1<WS!eUS+f1\"Tyb%s$VuE}*H9A!{ -]E{zSa>>W)SvK=bL}NT)yASA)U?%C}A WY2K\"suFUPSGISwK[~K_7`Ky%.A}vG)MPB(?2FGR|[6^$FD~r75otdNt7hz}oS3_G8>3/WM%KlKD9kM(;+ %EG;#SYFKsGG(Ka|ZxaHw910T }5L?W!Ccs~%1=VS[/MDvCkMtU,Usz{Hp.Kg5y1SabvqW+P$jyUKL~s<F'/s3sl55oG?Qs#PpXx^SlE=kQGtnaMG3N7#%lUK?%F!9QqCA][x8Gly^WG$wM4ZQWx8W'C<M|E4ct\"Ka!=gxhKtSfGh|K=G)p(o,xnM-JSz*Qd)+]>qS5*z':g6~JFK[rfppS]`S,9yP.``g?l(lK??tYMI/WshGZKKE7>b0JF\"$[BvrkW/cuRg&\\GM73W(=uR-8D\"SUWp?pJvf8fNWyWR7D*,S-D5qf1>Mi&rJs0,K+(vpTE]YiR8*lK{c2\\($(W4@N_hUKS$No0KTPL-? ;%U1CWH!(bMC2.#@KKSQb4$<@G(Y7j9/?&0MY7[bcK/Q`%2N1NXS1(_4-GPGJWJ[x$f&)eSa0l+H#xWc.){EeC7i{<~M|;KX^-{{\\C\"S]Q`(5m(E>_3>E*t~7)/K?^M_|,Z@?>>KW42 xDv$(?S5(nC8}Gy`>HTSQGxF[S[$ %W-oVN SBbIU?[[~/u #F0Su*zQ]{-S)@~u:KTfZ_XqQG@qGHB\"^SD0KM{K4}1S~7WmcRGN51j%KS\"40SGB,\",W`HS,2EcD}:2_GY_xs|SKqsF'2;m}q4)*o]5dmXVa(VK3@M\\xCGLKMKTT}vPN1S3B*W>_h{0bK>*LJ()9+QgKK[X/-\"2RqMT63-k^s2G~q9?d$<d)bw=lwWM|F%x@X/\\T2CQ~5v!_?8S(KYw[>)aFzZ8oP?<WcJtshW0E??MIgoG(\\W1;sA0NcSI#N3ZJ/9KS3R*+HeJMW$Y_P;j8IVjkr~h'~7GBDDaAtwUWHUthIe e5|PCsN=!lUWgv^Y@WKLqYK+VXEtvWK!K%;H`l(aGl46.KiRtPIN=d*4R8KS4Wohk<K7[zm2Y3MS[!(w'uG}k}sKD>FwSk[S8K!K{|0D7$vML?xxn!Wn1BM?FWmTQK+GhVWl&\"a/RKXn;fs~v'A8AGFI<=@U{^W6:Kp5r64v$QGywq~:NT+BKW7gDMC&X.~a-WPP&bj7M?(stKQqSL6g'8p/9&_5Iw=42$X_TdM4m*G&7kLe)+PVEINcT$H5rE$*DxRjHAGq3U<a.8K?:<H.yG>i[-P`Q{6KmS@Hk\\Qa,*a9.SNJ:K=hz_KURkCKKFKKKZ2GbBM^wGHf,`c+XZww9N3>nTv-ZNDH7578WWBDS)KAFBTQj`fsS-T Kacn2zl.=-NSGQ PTY(;qF],M0`:S>H[:$=Q(?QD~hK%SGW~K+Jcf1zfMSaAMpKVjS\"8pCdvo.}4qHa9.NFMWxmx9|-?QKd4v&+#B^<Hn-3N`tCme^^U<_qPPQTT-Lb ~l.L9WI[*RUoq[K 2(h-L(KmSj.cn;KnG21cDM<VfQl{b8:Y,}71dk6WGr>MKKg@7@Z@S]WIHbmBv_HZ~WnWz\\}\\Yq9>s5;k/z<dW3<ai[Ik[>\\)_.:^cdxoIWQbS/#n3\\5j{G&bSNQ)Dv$A7xMd+?9Q\\V~tnZ#(Hm6aGcSM3-\"K'gt 6^$olJ_<qS?4*ISWV.IQNw:$8fl7[S~rn:c?e;;twK.BwvH+xqHb@C=\\D3ENS[b?j:HKQ$SzL`zJVKz!!iSNS.=@MJMHWuMWD#jkSF;5Sgd44-/C!V'<&Y`JHEKs,%MS)^fDnGG`R:lG3KQR?[@%j4N7)9yEG1_\\#jCPr!iAZKG%/qKJ)\\g7FWEwv!qh`9/]+`c->{o}vWSZW\\MQ>-M@mVKwR5YGQ|@]`qq3KDeIN)S_QQa!}PIT|Y9G|ATeEauVYQ)=oZHm0G)M3BMvs|+8]~a& >F]SI%etW'yWSQKB~[ZSW{ZEQG/d>5WS[m2jN|xfldQ?$*IS.\\S$VmtvY6HG('s3h]#:-#@?xj{NQMGLSt_}1MGSQK`vcQ$S-\\L(WoX2Q}~PuX-rJ:afSnfMST>mpd/@@bgG{^p~hMW~\"*SEQrz6vSv#XMPRQKmJG0!<KPXcz7V9'y+(MzBa{S'Sd}QI]SrZL'V^fb=$|_h'ogDyKE_Mh2n{1GSRkj*W4tQwy_czh%m+X|j~G^a=7{LS`8GfEtS%zp8HWWoG#QR69)WkHa{IK}>QLi8<FK-Q=zht?tjZV {~K*c5MG`QK:G9x(S6wr?`+]]68#Juv{\\KV9SvK'F2U &ltKm+G@P3+NUisw3iDX1~xi=amdGQ?!1tfMDJC$GLmj?yeKQb~>DDcSo-E{~4qWGU0P\\N>+.NMGR>Wn>y;J&JfZ4=o,Rv'Q:%FG|=X5is[&K,Sw~sJDq\"~}b2GCGG|D\"Dj*2e'(>@Sb9`B,k~`Md(zKr-+m)7zBb#v+Qs8Wyvh{oifbM=KI>9tJH~,Rgq+J!;S*KlqG%HW6d|-J3U/I8BM:a$g))MSfN1|QIf-+gz}$EHw4u9i5[NZWJ54WG0=EL$)-|:5z\\/V-n6a*UMC^jZGYF~>S[:Q<k9}%dNbSh:T#vMXQKEMKLZS\";,S8W@KpMjBClIQy1[WW0o,e&HQ5W|/Hm.PwxY~qNB=6Y`2NKmzwN\"':*IwMp9<6cN2W*2SW5w4LQz7)Qg?ReMhDG6c@mmkQ?QG2xd/\\qJK4WWj<;r=.WVG8Ha`J%5WK_aprz=a=d|,bW?SF.0T6_G:ST}))cNs\"eSwu?{BX<?\\x~k5%3Ba7Bu&iNK tEe%LN&YnWcw&ka?>I-AG]vyHen=dXSW2Tnx9(s\"D%Zk/ - ,h@S5'.SW,;$3?>JaSYMM#WBF[KKshjWGAMI_>jKnI?&\"4,`%!_K]GS1&D\"wi#.Ng9VG4\\C-dM,es{S&SJAgHlXDM$}%^pM=W[\"VFts2.A~R!Gc=o'n:Kc658ryx]yp+ jt{0KE);A#c;K,z^`8K3mVnLUKrGBK@Se8e}SJ=I9X+K^ApG6t,K~Q:7JKclEhG?$VM}'M'MXzl]d\"#[z%aVG6A9?WW)!nzG!~N$k^EG'&UQ@ kMXHS?fGv{3miSCkDMWaKSV,1We0\"5$TBP1K xwc>\"K8`Bi{W>5lSw[v/]TRS,\"^yWSl[>%})5h3][=[-\" SY0NSS/z|wSE6Ix_4vG![\"?YG,YGSL3%sGS_&Atx*M@C9:!y:;h V<eKj/p|3KKr{UbilQ|lQKvCaKMFS2tE9GM~In1X6q&HuS{gGI:#dS`-*X#%9(YPA}Sn{|P{_xB&Wx|x5@cS]p`Ms\\n&>UTodQMThS]n?%}^S]LKec=)r\"g\"h+x| 2U#Q+wd{Gn!HY[WBWISKjL?B:X.~@HhN*<dk{KT1wJU2}}G5K*MGQQWpEm4`|\"rFqr2%6U0=z}[U?ks.?K$(.PC3n[K^_W\\3S;A$@^Mh;V-M?+Gt7@STG'?N^XI @m+YZz'Qp_':ih:W[*zW,[yG \"KKkSF-%RLPdkE?ke0QnN,l5G'T*_737BpY,dGK.I^{Z-r$,AysW_B%ZpqKSPN5l2$70ReS1Svy<wNU%AySwh b`|P^w /ZKE.Pg}gCL=I3{i>$Wkf! HvZ{6GVMo=5g7Cl)R{B`1'7|qTAHr~S@qT<9bup3\"aBGh%zv*p`WM4K:SE5w;Fn5/3Ww-3[5K<nsGKB!Mb8\"(c8aK|TYs`,~gG)L351%SRc3<Ry~?gKXm(9)Syb{!a&E/=\"<`yw 3HfPZ?f@?b,6 g.nzv76Pc0G&PSjS?Wl%kS7HK\"Yo{Z50K:5Q},Q?H6G~MAG4MAt>nWZP6>DS=G ZL-}$97|8l}$}wDWvWh2zsMr f Mq&fl:*xSWn,WY`_;`d:F5Ner/<Xt{N0MerTQV<9KJvtP|`%.t(<0u(IKrStm71W}SPdW]p*0w$)kJ#GnQ5`|U\"fhU\"}g@ljYA!UNkl8im1JR<oQ:;r@Wl=KM5C)9_.(+D.z_9,S<)^xK1]rK>cNB+yrGJ{Kn8_NRMn6XM*|BWGnK&0tSs]%,5`la}9U}fMN]`G_)8L.D]+'K(^>!e5w!&'F~N\\}G'#.kS\"e 4X4{t~1\">6W$BI8xHt&\"MPp9AviiKprZTf.'aH$x^G-:g-kMfx<NMWitEtw[TBH^{pXRb@rMQK?'.9jPEU/YTZQS}V}YclabsQ_q6?Pj~bVSgPfa{b+Q9Fp$AWCh_]d|atM8BFdT4K<k\\6&!Q#q)Xpjn:,^ZTi{Q5FWQtQ:QCol6RG\\/KMK2:WcH'?0/BA\\yim(K3Gf[G:B[zo%CGP>08A#%JcKEwt3JWKdbDSMHKYSmMGEYW5KJHZ{tk\\;({2u,peha[Xx WP@#A!Yf?#K/2?^_K&EA#fqJSf!MS1p1/g%JVWSMw*jQ]=?<-:Q6W3I|DXSlQz#BW[2P~6Kr~S;qWl;W0+#/!zKKq*PZfIKgM!j{FGEU3^$T S1s!NndK.E^iv>-xWV5ILK=uWVMbj.QY'-|ssa;S,K^=iC:w6}?#7fL8HK5TdB^G<Jk,6SNp,4]yUTY.\"%zCl GBP]6>d+(}_|<JEG9~.#J^QVSKB(#MG<g/t!tzjtWj(_zU<Hzx8+^}XS9tY<S]~x&IyGfKK+gW=dSWb3S`HBbtQdlcGIoG:-7G&Gi;SyuZ_V1dF\\gBJ){gRX2wKZYC;e-{xb3bZGS9?Y0cSB5_qRkejSP8SteJcpd?[65EPIETISQ'+$,`csPNgMfhg9a;!pWM+xWu5{SWYD7MF1=9|K6`1#KHj~Be;z\"xSKAu?)CH&!WT#- [#j}K%c%qqoMAtENvKH\"^2DgGxoS1rxC'WDneK!J1^TA+~sKSY\\:dwzc$WKrdem~}fsSQhM3[!a' M$)Q>s.\\>PSJ&s;PyQb+UKKVMVzfvW$xfG+&fdG$K+uPG_0b=@+WQZcZUgCWcSqQ-].L'q,soNJsF+IU/iMn3C`{8\\*GHG .>bSWP}\\SlogK9jLKGbk!Gf5CMSWY56V3eR?&!k#8lS=kMk[GKU?Dj~?5G@R'STc'fgPGS~Us:=,vQ(NVtS^\\iES-w#WS#*Q3+JA=)LeCWqS;>H;86P'$+e`J8~c7G2Sz=i1cE`<cGM.HP%':n~]sy2>y&S08&$kC#em0Z%xLnLg0KQ^C*8:kL<ouYIyi>bizSz&S~VG?|q.=I1SS<$|]fi.<cWJDbWuyVkLGoWY\"WUv3+,|A,4~pr,FMM,wI0Wn]YF+iRP{F_-nC@@95E4!qsL2WeK?U~j3Pa.YGPSM6jk~6Khu05z-Io$~'SU@KKk1;M*1_GY&mM?_vJx<s4!2QkAjS5\"AmW6].}|WD7M0fU@@G,[7ERa|KE\\o|,GQwQW\\oPD8Mp>\\KqM?^uGySS`x~X&?K[_q!FADbx;wTo761_K:SHnHu',%MK\\NcMMv\"qG::w[ud'Zro)& \"@+5rja_#~@hc#kY,&M^wZ1$T`pZsGbxZ)\\DtG|6v,bkJ:}KTKI*Hb9])p],0S~,,K1|=Y`V}$$c[C9S](R<nyK8->/-kf-t%A49G3]feaEKrfV&(M(5%EyW+rZ=H+5GR}Km|Zz]>G.L\\m7. a03M&NXK;sXZKP~(jb6xShv5;h/SUD_G15jwQGu\"12`Me.:Do4MqQ44L4N%K.W~85Dd1?S.da?M<mpUWs3LxLyUANCH5}W&l.@j/f?HoIB|W<Du$5MN4V@Vb>a~WI}W2kU}V$fe;\\S&DdlxR]Q2>]GB'mpL@D2WiG!'M&:W1'_<@k!#?Vp(6M.?5NQ6;;-U\"u~3@SS4*mSSu!0Zor0*y>sK%<SG6+~K&djwK=[[)i 3vMj}x\\o?=GDGsmSD[V-xHem'.[eWekb@]jBoSt\"BK/G~SIzSKK0yHS/',K6vMW*j!](5yah M>MQ/a>og\\L.?aA>+v=,<ruLR\"eKK\"KGmKK!6%}Jj!FcRiz8'CZ!%d$RMrs_h}3s:b!UWV@Pxb!-{*6HCX43v^\\ac!_KKe;&ytFh370RgA/kQK2LK]XN4Ms/k#\"K#%f6*\"Sy$#$M=MGl;F]p^=-vKMG@,jRjtB#|2G DEwQ>_S>\"L5ujK9A%\\. Q5D 8,\\G9tW*W/]ch#lFTz,*MVSdJc#Z8*z*99ZQvXSEPtWD@EQ`_Uy]Qr,rc_D[E0wo00p*2c{)BKyf_G=5N%_</I\"9\\*\\&K,-PM8n710v#Ky{]CM/Wfe;@]q4Q9Q.FuKmeP.G.kR6F~GC yoW[5S-ovCo)Sk{VMpKNE7dgGW}1Gz&DS{'cDF29?/1257SH|[+v2'&tl6GoM<^#fXey0 (Q\\E%CaKrVS[%E#CVzo+K,)9Q@$SGS35<<F+9YKS6^NivtSpy]#%//hwH_RDGBnleSPAG#V3mde<Yc 'l)W @F'`*x8K S{uXYFjP2SM~VRn{Q[aW8r%K\"Q,IwP>H3Gh[SS\"v>QSgGvKs#wm}e )o_u#jkH)$r`.SvoQ~`5)61>E=*tR~%H=0\"gKq#*H_hykFQM!Y#Pf3_IL.grC: P6W?!TWGx |xu;ax/+zr^8Gqt2si,\"/KfnsQC>dSWZD(gKbeV[Pl0GW?>>&vs5GMQiGzbgf8'G1Z)2 F@NG8+Ps-c*3S-Y`NQ_GT+_-K@5%7>?/aeKrEasKSYQ+GsWS538U7!M8L]HsLVkNEQJV[H]UKWSLhD:_zYQJW`l{?]ZM5=<\\{] # HK3RBd6nyG%}l-[+L_xXb2\"f;FKQMkg5n`?XS!u<3Ms<G!.K|GaES]3rG31#pjhMna6!|eA)nCL(fAuE&1@MJMHod)WYAS@WQg8Ndc%W~^3%A[}cN`Gs0K=4yKzzWh>Z5)2b$XSL[ME=pKi)g7qK3GT<mCWV}u@ QSL\"Gq)DCgu(0Mu%K8*SU>6-x\\@b5+)W~,le7MW;1v:]K;>awIe%Tb!cSbwL1[%BitPc8a0~kSs1W)6*^FDEgQSc-K+U[_D-/~bJQ4%Gi\"I(= ^-K ~<,<4WvW6-SA0-*KWK=PX@uW]}SB~RC%u93\\gF){,SMYG>w!}k%fMxI$qpZ*^WLx@ 4E-u8x%SMsUH~H/{G}2p9oSShS1+}SXZJF#Tv\"71SbL.9JLGfCNeGx>Nsaw_L.MKA3y&9>\"yW+}t|wq1?WK zK6N\"aSg1\\(c1LB2K/Vu\"BA\\h%ZKd]tXZTu\"%M0BHWD`,hcmXd3p*IHItdg^`^uAd^u@1\\UP|z*mU3-1SwcW<;9@?KP*y-1Sb;_3[~evPgE!`FIDQaY2[/ClQ!v<\\%CLa8S17KnW\"osQ}B0WK(F2lWX:Y0M*.C.G|>8z3sNTF9 $jSStma{`zWJ6Eh$p-V%VKfXFf(IN[G*K!<Wx>deVpB//k4}3I@q:G|f6@$a{po/x -5?N$ZRNSb=3A[}WWnwKwSQ/,PN!>W,K5?:NCS-BGQq,x]G4m(_5sxA4'>kgK&$l@}(x\"he@v6^|PJ~L*%!Gd0_Ej@\"|`W#RM`wSwM=qG@S/8MeS G8nWQz\\<6huP3SXn(wt4NhrB.3pCXMl9h<BIIflQb[~dAiS}aS\"\\PMpNA)QiSQZEG@a,.`oScQ+/oA~]W3fS1zo@,G#jTJ@+o5GnTZWE@SI& J4lSpIZ<5`<Se9QTC)bSW!2t/S;7bbWQKB5KWG1~0GjM)D\\M0HndJp%'{C%=GN#EYI( pzM]EMN UcATsW9V}=KB`'\"\\2sw{V%b@X#-M[AQ;KH)~BB9Yc3-6YN;S/H<)5`Theu67,3eT(W7+A\"zknquszYCM94hL$Kwp{q@tqP_QGSrG^0nLI8p%9NG,XFt]KQ\\ ^%RcK40^X7#vSHtlP|V.KWN@N }yafG@0qJj1$Id05JMSM<~\\[(vW b[0S~%jK--'oDpKjTGMf`\"Mym:q!\\DSv,%9@QwKN\"7yT(HQS*TlGw*Jdb%>dR\\!QNDL@{h?U]+xn'_tSGe-m~Sw:SxMSGv~2\"BKl_ES0hQX72*kAD`S68{S%Q@T*e)h-JQ*K$_*I\\UXi2E2APGjKGm!ySo9q#SbGT`U.Pt]M5'UY I^mZ^vy|FITQ}\\>_z3#pzQ]Deq|DGZA:#c76KS5MQ>{CA=HUT`?v'zQN$,~14Ub`<PFhR.|IMM^$a{ A}AW?lz\"e9\\KZ><Dyv:W#KGefMKG7zytBQ2WgWc}1gr NMRGQ/8I|!ur`IQbGIGY>G4'lBAS^F[]GQ|f\"~ta*UK0nt9g_[W>Yw'y09`GrjSTM2Y>N|A DaWyPa/lK^={QS>VAP{1sE NQU}dplrd!G=(mV;< ;R&WKKoGx2IA+8po;G3WN@HZb>p+<_VMQPY`Aq4~kYSka[q']gp~ XK(~QnGqS!\\j+UvC.Nq|,\"qZzf-h$IIkJq.cTfA)}KSvJnQ=.%=JYQVmK0-+hn&Sc?KI*iv[b#5$$'y_i+B `w!9qYX78KW\"ArQ.D]d)xKlMjHKmhXF,.Hm)rR1Q9sAigjssS4lx!c*aC19lz0KB!YQb+/)Q'y3W'y}\"\\!WFrB7SV:#~%9q&:~K`!oS?ggDC1aQKi,W-GI^KKo}@5xWYQ,A6BM*1G,<v-u-A6y$W&7GSi;\"Q[cA3XB7p'WGFt0a(KTg<j2dlTDJ!62\"|`f.GSJs''jS_2H^WGTi4q4UXDPzL\\CK{1=iLWD!4|;_eQ}oW&69Ws[v>pdCuoP9#w;>JE%.ENw$]k?Gvf~zQS]gK3`S3SWEQD5ZS]s<%ppASuI,F[W]NfD5MZBFWS(k?#F9hulK)jt<eNW(cM_&NS.r%ZUTUSS!EGGKQQ\"/QWCSoSP,:pSlEB7):)\"s+'KuC!oS7{^b&_G-KaTDgG>ZNSLW&K^pfXnvnU@[,6\\DuG=M|S6[[+S$9KwbMR<5g[, K}8@SWPYl#8Kr<8't:2FDMz0wNCWG6)PK(KEI0s?%G`;Bs4jf~8[WvN~)>6&*eJ@-jQD~M`2I<&WTGl4+DHe`\\G^S{ZS++=C\"mrg>KDW_'6bwT%G2bS?pM]B/-\"nsK[FC_|*1^J&NRRVNYvTNzL}-(FSq_7QMSSGG^=GGb{}WtxQHMM!!<\"{}S(^hQhS2GVNGGm*!pK+()okXqQPlQ1(&wa2UaMtWKbSf]aI3m&vSGiIwPDl)vu:SZE^ tWl\\>5qQ<V/CMG1Ygs$MM$MC*?wZh?4+82&NFyG!uVC9K0c`GSP';tjFIeq3V[Y)2DSi3KBWK(\\sdN|bp@M<MPk\"Lk;K7\\CT&[+M-IWzP-+h?QnSfM$+q\\cmc)^h9K]aWTS\\8GGS5Q4D;U|8W*\"WMGRF2([GXWyiMjsG{$YrFGK2&zSLYN\\NoS5W^zI9\"/]:4kdx)(bK GJx:G0!-+kn&NvS[vQ|W+I!SWTW\"{#Q_INnFS2vv%pGs,fbjQ?zM)2,GIJ6J_:tW3X4:LS+e;fur@\\STKG$=HQGSS)>`QfaWWLHbQK4*<SS;a}61[Km\\G+dT,SN;)7S,{<f&kQ!6BprxNB>2EK?VVxQVKS\"8NQ_?Wc?f~<LM3KQw _BKjK3dt'SY:SG4+23MbZQ(/55;a+gW/8;G\\XKw^;-WF&uBboSuQ~sJW/@@{dt@_'plZ^tqG[Q4GccU~gWr6zGiN#MAg^<P_N@:_1S^<S(jWPF\\g'QGh[;(hC6=Z(K 5MH6kn2d*3x]jt4wCBXu$M(ZwbVWQrQ&s`MC>NxK~;f|L,Pkjr(-x=oJ;+YMW?QJB>GqoKUdrQ=vR7/KS<#i*?9kzSuGK7v]SQ2{SLTH3$$|p1xHEhU\\}ST<QXdW-K6@/pP9EWWS$9iTsp+-_QvzZgq?;W-m=0%hMd=>4pr=]K$}D{txXMe5!h@5plW#<@DGuoc5yX!2Sr>Ft.CUy{dz[S=C=)\\o8$zm)G*xo&gv!*NX b&)JQgNj5z!WMdSktwQ#wV<YFNq}>]q/!?.K-`a>aH\\kE3G,2~7D1. [BpWC@qa%R,-;GiSi?~9s33eExqG*,y'M8BJIp hL)GNdx<y&~$nNi>oG6~6|K@vzApKD5hE_i]b)SPqA6[[m6GxNY<0#SD(WAuQU1s@eGoG6QB/?$`1?<HWuu2C@oFn,,FWFG3XUpK.NDC.T\"j.(RD!?=@>*ij%.:'gNBR^JSAr~L=L#n8mDadKi5z/5MI_!QSWZ9&=QPPHQbg.%qP%]u_=S_}M-U+[G`K>A/0R(Seig\\/KV?Sk!M%ZWlYPEKy6cdH/Cbcm})_M57aWoW?~Z9t-)W\"t)gpvZKCBMDm[=AvG`K`W#x@p;5QwNPXh(_!uwhfVz:{[!SsveZz{s&;K`7w\\I(\\=:$=-3+0F%kxK:/GRvS+M#N7S}Q[SKQ%lK_/)L|Dg02:fG^}|mKZoKvi&d6.UDq9Vz% ;VFjIMWFWs\\UHoVq)b}Slc(#]KrwX_6_vTPIE<Q[}dTZcBB=U>[K@u5E1?*x|gS_B^e{\\>FeDfpT?vC?T,cl-WW>-jQGLVe.(Ci>oU~a)Zpe&%TBaF}RSpK&wo;MNeYpaUey].6o4ZK_,;nS:[g+[./LxJZVf#,bqI/n;BW[WM]]sXd{*XkHW|6;:Z5zS!~%mu_deWB?XRHl/qJWd{vk7=W$Q;x\"sW-GdL<3ugRKKBG_',E;k[SD'U/?)XS;Rfk@D'iLy?ymk7-n/vSDepK]wmzQ<;m]y:XGnw )F]S#Q*pM5\\S1wWuGAT<_pX:'_ 6EP:fKGpb3`6VbarS??g%u,#VMXMm/]SJmQ*G^|L'|Mc#JT\"L9M[:`&3M=(EU~,6GW*KgukPXit$s%eXnVgW^Qt=GZls9SC9&@N1bI<T+2\"S$@C):\"KHSR5C?8`&MEFmw/0#i{5dNW},CPQX%*Jg>rk)rmz8v^W^'|Q) GXSnK[h]u:s#x3tY37TM#v}Wn4kmDv(gnE1MaS-!#SrblGv7c_KwQhZ,JjAT&W3jNWn&G{+MGMyQMoa8&]^K@[^\\W(DM|vK#qYPI}gAC@S|4@ZSKGSQqMSkS<dYR#9;%$Gl*UQSxs}aBdGinW2VtvD}h=~SVK>3|Z/mWL7^Mx\\Bn$WL"

    weights = [int.from_bytes(c.encode(), "big") - 47 - 0x20 for c in chr]
    # weights = [int(weight) for weight in re.findall(r'[+-]\d+', chr)]

    weights += [0] * (SYNAPSES_COUNT - len(weights))
    ai = GreenCircleAI(weights[:SYNAPSES_COUNT])

    while True:
        ai.run()
