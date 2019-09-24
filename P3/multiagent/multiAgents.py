# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        
        newPos = successorGameState.getPacmanPosition() #new Pacman Position
        newFood = successorGameState.getFood() #Remaining food
        newGhostStates = successorGameState.getGhostStates() #Get the state of the Ghosts
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] #number of moves that Ghost will remain scared

        "*** YOUR CODE HERE ***"

        #Get the position of a Ghost
        #if the distance between the ghost and pacman is less than 2 the value will be 0 --> Dead
        newGhostPos = successorGameState.getGhostPosition(1) 
        if util.manhattanDistance(newGhostPos, newPos) < 2:				
            return 0
        
        #while pacman is alive, the evaluation value will be the score
        value = successorGameState.getScore()
        
        #calculate the new distance between Ghost and Pacman
        ghostDistance = (util.manhattanDistance(newGhostPos, newPos))
        
        #Creation of a list of Remaining Food
        lista = []
        
        #Append of all the remaining food position to the list
        for idcol, columna in enumerate(newFood):
            #print "column", idcol, columna
            for idfil, fila in enumerate(columna):
                #print "row", idfil, fila
                if(fila == True):
                    lista.append((idcol,idfil))
                    
        print "LISTA: ", lista
        
        #Creation of a list with distances between the remaining elements and Pacman
        distance = []
        #Calculation of the distances
        for pos in lista:
            distance.append(util.manhattanDistance(pos, newPos))
        
        minDistFood = 0
        if(len(distance) > 0):
            minDistFood = min(distance)        
        
        if(ghostDistance == 0):
            value = value + 10*(minDistFood**-1)
          
        if(minDistFood == 0):
            value = value - 10*(ghostDistance**-1)

        else:
            value = value - 10*(ghostDistance**-1) + 10*(minDistFood**-1)

        
        print "getScore\n", successorGameState.getScore()
        return value

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def minimax(gameState, depth, agent):
            #We increase in one unit the value of the agent till we arrive to the number of agents. Then we return it to 0, Pacman Movement.
            agent+=1
            if agent >= gameState.getNumAgents():
                agent = 0
                depth += 1

            #If we win, lose or arrive to the maximum depth, we'll return the evaluated value  
            if (depth==self.depth or gameState.isWin() or gameState.isLose()):
                value = self.evaluationFunction(gameState)

            #If the agent is the Pacman (number 0), we'll execute the maxFunction
            elif (agent == 0):
                value = maxFunction(gameState, depth, 0)

            #On the other hand, if it is bigger thant 0 (Ghost), we'll execute the minFunction
            else:
                value = minFunction(gameState, depth, agent)

            #Return of the value
            return value    
        
        #Pacman movements
        def maxFunction(gameState, depth, agent):
            #We initilaize the variable
            result = ["", -float("inf")]
            #We get all the legal pacman actions
            pacmanActions = gameState.getLegalActions(agent)
            
            #It there's no action, return the evaluation value
            if not pacmanActions:
                return self.evaluationFunction(gameState)
                
            #We iterate for each possible action
            for action in pacmanActions:
                state = gameState.generateSuccessor(agent, action)
                value = minFunction(state, depth, agent+1)

                #Checking if it's a list or not
                if type(value) is list:
                    check = value[1]
                else:
                    check = value

                #If the value is bigger than the actual, we'll replace it   
                if check > result[1]:
                    result = [action, check]       
                           
            #Return the value              
            return result

        #Ghosts movements
        def minFunction(gameState, depth, agent):
            #Initialize variable result
            result = ["", float("inf")]
            #We get all the legal Actions of the Ghost
            ghostActions = gameState.getLegalActions(agent)
            
            if not ghostActions:
                return self.evaluationFunction(gameState)
            
            #We iterate for each Action   
            for action in ghostActions:
                state = gameState.generateSuccessor(agent, action)
                value = minimax(state, depth, agent)

                #We chech if it's a list or not            
                if type(value) is list:
                    check = value[1]
                else:
                    check = value
                #If the value is lower that the actual, we'll change it 
                if check < result[1]:
                    result = [action, check]

            #Return the value         
            return result
             
        finalValue = maxFunction(gameState, 0, 0)
        return finalValue[0]  
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        def minimax(gameState, depth, agent, alpha, beta):
            #We increase in one unit the value of the agent till we arrive to the number of agents. Then we return it to 0, Pacman Movement.
            agent+=1
            if agent >= gameState.getNumAgents():
                agent = 0
                depth += 1

            #If we win, lose or arrive to the maximum depth, we'll return the evaluated value   
            if (depth==self.depth or gameState.isWin() or gameState.isLose()):
                value = self.evaluationFunction(gameState)

            #If the agent is the Pacman (number 0), we'll execute the maxFunction   
            elif (agent == 0):
                value = maxFunction(gameState, depth, 0, alpha, beta)

            #On the other hand, if it is bigger thant 0 (Ghost), we'll execute the minFunction  
            else:
                value = minFunction(gameState, depth, agent, alpha, beta)

            #Return of the value
            return value    
        

        #Pacman Movements
        def maxFunction(gameState, depth, agent, alpha, beta):
            #Initilize the variable
            result = ["", -float("inf")]
            #We get all the legal pacman actions
            pacmanActions = gameState.getLegalActions(agent)
            
            #It there's no action, return the evaluation value
            if not pacmanActions:
                return self.evaluationFunction(gameState)
                
            #We iterate for each possible action
            for action in pacmanActions:
                state = gameState.generateSuccessor(agent, action)
                value = minFunction(state, depth, agent+1, alpha, beta)

                #Checking if it's a list or not
                if type(value) is list:
                    check = value[1]
                else:
                    check = value

                #If the value is bigger than the actual, we'll replace it         
                if check > result[1]:
                    result = [action, check]       
                 
                #If the value is bigger than Beta, don't explore the branch (prunning)
                if check > beta:
                    return [action, check]
                #New Alpha value is the biggest value between last Alpha and the checkedValue
                alpha = max(alpha, check)         

            #Return the result              
            return result


            
        #Ghosts Movements 
        def minFunction(gameState, depth, agent, alpha, beta):
            #Initialize variable result
            result = ["", float("inf")]
            #We get all the legal Actions of the Ghost
            ghostActions = gameState.getLegalActions(agent)
            
            if not ghostActions:
                return self.evaluationFunction(gameState)
            
            #We iterate for each Action   
            for action in ghostActions:
                state = gameState.generateSuccessor(agent, action)
                value = minimax(state, depth, agent, alpha, beta)

                #We chech if it's a list or not        
                if type(value) is list:
                    check = value[1]
                else:
                    check = value
                #If the value is lower that the actual, we'll change it  
                if check < result[1]:
                    result = [action, check]

                #If the value is lower than Alpha, don't explore the branch (prunning) 
                if check < alpha:
                    return [action, check]
                beta = min(beta, check)                    

            #Return the result         
            return result
             
                    
        finalResult = maxFunction(gameState, 0, 0, -float("inf"), float("inf"))
        return finalResult[0] 
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

