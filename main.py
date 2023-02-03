import math
import random
import time
class Node:
    def __init__(self, parent, turn, is_rolling_node, score=0, enemy_score=0, score_at_risk=0):
        self.is_rolling_node = is_rolling_node
        self.parent = parent
        self.score = score
        self.enemy_score = enemy_score
        self.score_at_risk = score_at_risk
        self.visits = 1
        self.reward = 0.5
        self.children = []
        self.is_expanded = False
        self.player_turn = turn
        self.result = None
class mcts:
    def __init__(self, score, enemy_score, score_at_risk, iterations):
        self.iterations = iterations
        self.player_turn = True
        self.root = Node(None, self.player_turn, False, score = score, enemy_score = enemy_score, score_at_risk = score_at_risk)
    def select_UCT(self,node):
        child = node.children[0]
        UCT_roll = child.reward/child.visits + math.sqrt(2*math.log(child.parent.visits)/child.visits)

        child = node.children[1]
        UCT_pass = 1-child.reward/child.visits + math.sqrt(2*math.log(child.parent.visits)/child.visits)

            
        if UCT_roll>=UCT_pass:
            return node.children[0]
        else:
            return node.children[1]
            
        
    def expand_decision_node(self,node):
        node_roll = Node(node, node.player_turn, True, node.score, node.enemy_score, node.score_at_risk)
        node_pass = Node(node, not node.player_turn, False,node.score, node.enemy_score, 0)
        node.children = [node_roll, node_pass]
        node.is_expanded = True
    def expand_roll_node(self,node):
        new_node = Node(node, not node.player_turn, False, node.score, node.enemy_score, 0)
        if node.player_turn is True:
            new_node.score -= node.score_at_risk
        else:
            new_node.enemy_score -= node.score_at_risk
        node.children.append(new_node)
        for i in range (2,7):
            new_node = Node(node, node.player_turn, False, node.score, node.enemy_score, node.score_at_risk)
                    
            if node.player_turn is True:
                new_node.score += i
            else:
                new_node.enemy_score += i
            new_node.score_at_risk += i
            if new_node.score >= 100:
                new_node.result = True
            elif new_node.enemy_score >= 100:
                new_node.result = False
            node.children.append(new_node)
        node.is_expanded = True
 
        
    def roll(self):
        return random.randint(1,6)
            
    def select(self,node):
        if node.result is not None:
            return node
        if node.visits == 0:
            return node
        if not node.is_expanded:
            if node.is_rolling_node:
                self.expand_roll_node(node)
                roll = self.roll()
                node = node.children[roll-1]
                return node                
            else:
                self.expand_decision_node(node)
                return self.select_UCT(node)
 
        if node.is_rolling_node:
            roll = self.roll()-1
            node = node.children[roll]
            return self.select(node)
        else:
            return self.select(self.select_UCT(node))
    def simulate(self, node):
        if node.result is True:
            return 1
        if node.result is False:
            return 0
        else:
            score=node.score
            enemy_score=node.enemy_score
            score_at_risk = node.score_at_risk
            player_turn = node.player_turn
            if node.is_rolling_node:
                action = 'roll'
            else:
                action = "decision"
                
            while score<100 and enemy_score<100:
                if action == "roll":
                    roll = self.roll()
                    if roll != 1:
                        if player_turn:
                            score+=roll
                        else:
                            enemy_score+=roll
                        score_at_risk += roll
                        action = "decision"
                    else:
                        if player_turn:
                            score -= score_at_risk
                        else:
                            enemy_score-=score_at_risk
                        score_at_risk=0
                        player_turn = not player_turn
                        action = "roll"
                        
                else:
                    decision = random.randint(0,1)
                    if decision ==0:
                        player_turn = not player_turn
                        score_at_risk =0
                    else:
                        action = "roll"
            if score >= 100:
                return 1
            elif enemy_score >= 100:
                return 0
                
    def backpropagate(self, node, reward):
        while node is not None:
            if node.player_turn:
                node.reward += reward
            else:
                node.reward += 1-reward
            node.visits += 1
            node = node.parent
    def iteration(self):
        node = self.root
        node = self.select(node)
        reward = self.simulate(node)
        self.backpropagate(node, reward)
    def go(self):
        i = 0
        while i < self.iterations:
            self.iteration()
            i+=1
            reward_roll = self.root.children[0].reward/self.root.children[0].visits
            reward_pass = self.root.children[1].reward/self.root.children[1].visits
        print("rzucic  --- szansa na wygrana: {}, iteracje: {}.".format(round(reward_roll,2),self.root.children[0].visits))
        print("pasowac --- szansa na wygrana: {}, iteracje: {}.".format(round(1-reward_pass,2),self.root.children[1].visits))
score = 0
enemy_score = 0
score_at_risk = 0
iterations = 10000

pig = mcts(score, enemy_score, score_at_risk, iterations)
pig.go()

            
            
            
            
            
