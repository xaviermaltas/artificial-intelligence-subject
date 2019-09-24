# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #"We'll repeate the process the number of iterations that we want"
        for itertations in range (self.iterations):
            #"Copy of the values for having the orginal save"
            valuesBKP = self.values.copy()
            #"We'll iterate for each state"
            for state in self.mdp.getStates():
                lNewQValues = list()
                #"We'll iterate for each possible action from the state"
                #"If the state is a terminal, the value will be 0"
                if self.mdp.isTerminal(state):
                    self.values[state] = 0
                #"If the value is not a Terminal, we'll calculate all the QValues for this state for each action"
                #"and we'll select the max. After that we have to actualizes the values"
                else:
                    for action in self.mdp.getPossibleActions(state):
                        lNewQValues.append(self.computeQValueFromValues(state, action))
                    valuesBKP[state] = max(lNewQValues)
            self.values = valuesBKP.copy()       


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        #"Create a variable for the Qvalue, with initial value 0"
        QValue=0
        #"We'll iterate for each possible action"
        for (nextState,probability) in self.mdp.getTransitionStatesAndProbs(state,action):
            newValue = self.values[nextState]
            #"Calculate the new Qvalue"
            #"Q*(s,a) = sum[T(s,a,s')(R(s,a,s')+gammaV*(s'))]"
            QValue += probability * (self.mdp.getReward(state,action,nextState) + self.discount * newValue)        
        return QValue        

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        #"We'll iterate for each possible action from the state"
        actions = self.mdp.getPossibleActions(state)
        
        #"Create and initializate the variable policies"
        policies = util.Counter()
        
        #"If there no possbile acctions, we'll return none"
        if len(actions) == 0:
        	return None    
        else:    
            for accio in actions:
                #Save the Qvalue for each action
                policies[accio] = self.getQValue(state,accio)                          
            return policies.argMax()  
            #We'll return the action where the Qvalue is max

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
