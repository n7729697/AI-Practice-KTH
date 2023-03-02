#!/usr/bin/env python3
import random
import math
import time

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR

TimeLimit = 0.05

class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})
    
    def search_best_next_move(self, initial_tree_node):
        """
        Use your minimax model to find best possible next move for player 0 (green boat)
        :param model: Minimax model
        :type model: object
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str.
        """
        initial_time = time.time()
        depth = 0
        timeout = False
        seen_nodes = dict()
        best_move = 0

        while not timeout:
            try:
                move = self.best_search(initial_tree_node, depth, initial_time, seen_nodes)
                depth += 1
                best_move = move
            except:
                timeout = True
        return ACTION_TO_STR[best_move]


    def best_search(self, node, depth, initial_time, seen_nodes):
        """
        Performs an alpha-beta pruning search for iterating depth
        :param node: Root node
        :type node: game_tree.Node
        :param depth: depth layers
        :type depth: int
        :param initial_time: initial time time of the search
        :type initial_time: datetime.time
        :param seen_nodes: nodes visited before
        :type seen_nodes: dict
        :return: Best scoring move
        :rtype: int
        """
        alpha = float('-inf')
        beta = float('inf')

        children = node.compute_and_get_children()
        scores = []

        for child in children:
            score = self.alpha_beta_search(child, child.state, depth, alpha, beta, 1, initial_time, seen_nodes)
            scores.append(score)

        best_score_id = scores.index(max(scores))
        #print("Best score: ", scores[best_score_id])

        return children[best_score_id].move

    def heuristics(self, node):
        """
        Heuristic function for a node with respect to hook position and fish position.
        :param node: Given node
        :type node: game_tree.Node
        :return: Heuristic result = score*distance + score now
        :rtype: float
        """
        #compute ManhhatManhattan distance from the hook to a fish
        def h2f_distance(fish_position, hook_position):
            y = abs(fish_position[1] - hook_position[1])
            dx = abs(fish_position[0] - hook_position[0])
            x = min(dx, 20 - dx) # 20*20 grid 
        
            return x + y

        total_score = node.state.player_scores[0] - node.state.player_scores[1]

        h = 0
        for i in node.state.fish_positions:
            distance = h2f_distance(node.state.fish_positions[i], node.state.hook_positions[0]) + 1
            if distance == 0 and node.state.fish_scores[i] > 0:
                return float('inf')
            h = max(h, node.state.fish_scores[i] / distance)

        return total_score + h

    def alpha_beta_search(self, node, state, depth, alpha, beta, player, initial_time,seen_nodes):
        """
        Performs the alpha beta pruning search algorithm
        :param node: Given node
        :type node: game_tree.Node
        :param state: state
        :type state: game_tree.Node
        :param depth: depth layers
        :type depth: int
        :param alpha: alpha pruning
        :type alpha: float
        :param beta: beta pruning
        :type depth: float
        :param player: player 1 or 0
        :type depth: int
        :param initial_time: initial time of the search
        :type initial_time: datetime.time
        :param seen_nodes: nodes visited before
        :type depth: dict
        :return: v in alpha-beta pruning
        :rtype: float
        """

        def hash_key(state):
            """
            Computes the string hash of a given state using the hook positions and fish positions and scores
            :param state: Node state
            :type state: game_tree.State
            :return: Hashed state
            :rtype: str
            """
            pos_dic = dict()
            for pos, score in zip(state.get_fish_positions().items(), state.get_fish_scores().items()):
                score = score[1]
                pos = pos[1]
                x = pos[0]
                y = pos[1]
                k = str(x) + str(y)
                pos_dic.update({k:score})

            return str(state.get_hook_positions())+str(pos_dic)
        
        if time.time() - initial_time > TimeLimit:
            raise TimeoutError
        else:
            k = hash_key(state)
            if k in seen_nodes and seen_nodes[k][0] >= depth:
                return seen_nodes[k][1]
            children = node.compute_and_get_children()
            children.sort(key=self.heuristics, reverse = True)
            if depth == 0 or len(children) == 0:
                v = self.heuristics(node)
            elif player == 0:
                v = float('-inf')
                for child in children:
                    v = max(v, self.alpha_beta_search(child, child.state, depth - 1, alpha, beta, 1, initial_time,seen_nodes))
                    alpha = max(alpha, v)
                    if alpha >= beta:
                        break
            else:
                v = float('inf')
                for child in children:
                    v = min(v, self.alpha_beta_search(child, child.state, depth - 1, alpha, beta, 0, initial_time,seen_nodes))
                    beta = min(beta, v)
                    if beta <= alpha:
                        break

            key = hash_key(state)
            seen_nodes.update({key:[depth,v]})
        return v