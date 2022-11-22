### Main ENV
from gym import spaces
import numpy as np
import random
from itertools import groupby
from itertools import product



class TicTacToe():

    def __init__(self):
        """initialising the board"""
        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] # , [1,2,3,....,8,9]
        self.reset()

#############################################################################################
    def is_winning(self, curr_state):
        
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        """ winning_pattern = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]"""
        
        winning_pattern = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        
        for pattern in winning_pattern:
            if not np.isnan(curr_state[pattern[0]]) and not np.isnan(curr_state[pattern[1]]) and not np.isnan(curr_state[pattern[2]]):
                pattern_state = curr_state[pattern[0]] + curr_state[pattern[1]] + curr_state[pattern[2]]
                if pattern_state == 15:
                    return True
        return False


    def is_terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up
        if self.is_winning(curr_state) == True:
            return True, 'Win'

        elif len(self.allowed_positions(curr_state)) ==0:
            return True, 'Tie'

        else:
            return False, 'Resume'

#############################################################################################

    def allowed_positions(self, curr_state):
        """
        Takes state as an input and returns all indexes that are blank
        curr_state = [1, 2, 3, 4, nan, 8, nan, 9, nan]
        return = [4,6,8]
        """

        return [i for i, val in enumerate(curr_state) if np.isnan(val)]


    def allowed_values(self, curr_state):
        """
        Takes the current state as input and returns all possible (UNUSED) values that can be placed on the board
        curr_state = intermediate_state = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        used_values = [val for val in curr_state if not np.isnan(val)] # [1,2,3,4,9]

        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]
        return (agent_values, env_values)

#############################################################################################

    def action_space(self, curr_state):
        """
        Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values
        state = next_state = intermediate_state = [1, 2, 3, 4, nan, 8, nan, 9, nan]
        for AGENT we have left with [5,7] values
        we have space of [4,6,8] (idx position)
        action_space should give for AGENT as (4, 4),(4, 6),(4, 8),(6, 4),(6, 6),(6, 8),(8, 4),(8, 6),(8, 8)
        and for ENV [6] same concept! (4,6),(6,6),(8,6)
        
        """
        

        agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
        env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
        return (agent_actions, env_actions)




    def state_transition(self, curr_state, curr_action):
        
        """Takes current state and action and returns the board position just after agent's move.
        Example: 
        Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], 
        action- [7, 9] or [position, value]

        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        
        curr_state[curr_action[0]] = curr_action[1]
        return curr_state


    def step(self, curr_state, curr_action):
        
        """Takes current state and action and returns the next state, reward and whether the state is terminal. 
        Hint: First, check the board position after agent's move, whether the game is won/loss/tied. 
        Then incorporate environment's move and again check the board status.

        Example: 
        Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], 
        action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False)"""
        
        final_state = False
        # action taken by AGENT
        intermediate_state = self.state_transition(curr_state, curr_action) # intermediate_state = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        final_state, game_status = self.is_terminal(intermediate_state) # Returns win, lose, tie (True) or reusme(False)

        if final_state == True:
            if game_status == 'Win':
                reward=10
            else:
                reward=0
        else:
            # action taken by ENV
            # if intermediate_state is [1, 2, 3, 4, nan, nan, nan, 9, nan] 
            pos = random.choice(self.allowed_positions(intermediate_state)) # then it will return [4,5,6,8] as remaining available position
            val = random.choice(self.allowed_values(intermediate_state)[1]) #[1] Is for ENV and [0] for agent; taking random one value 
            intermediate_state[pos]= val
            # ENV action taken; Checking the status of game
            final_state, game_status = self.is_terminal(intermediate_state) # Returns win, lose, tie (True) or reusme(False)

            if final_state == True:
                if game_status == 'Win':
                    reward=-10
                else:
                    reward=0
            else: # if game is draw or Tie then -1 reward
                reward=-1

        return intermediate_state, reward, final_state

    def reset(self):
        return self.state
