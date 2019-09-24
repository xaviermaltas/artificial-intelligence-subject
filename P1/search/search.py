# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    #Creation of the stack
    stack = util.Stack() 
    #We push the initial state node into the stack
    stack.push([[problem.getStartState(), '', 0]])
    visited = []

    while not stack.isEmpty():
        #While the stack is not empty, we pop the last node out of it and put it in the path.
        path = stack.pop()
        #Save the first parameter of the last node of our path
        lastNode = path[len(path)-1][0]

        #See if the current node is the goal
        if (problem.isGoalState(lastNode)): 		
                        #We return all the movements done until the discovery of the goal.		
			return [node[1] for node in path][1:]	
        #if our lastnode is not in the visited list
        if not (lastNode in visited):     
			visited.append(lastNode) #We introduce it to that list as we visit him		
			for x in reversed(problem.getSuccessors(lastNode)): #We get the childs of the current node using reverse in order to get an optimal order for dfs
				if not (x[0] in visited): #If child is not in visited one's list
					currentpath = path[:] #We copy the path into our currentpath variable 
					currentpath.append(x) #And we add the child to that path					
					stack.push(currentpath) #We push this path into the stack
	

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    queue = util.Queue() #In this case we will use a queque instead of a stack
			 #This is becouse we want the first in element to be the first out element so we can implement a bfs
    queue.push([[problem.getStartState(), '', 0]])
    visited = []

    while not queue.isEmpty():
        path = queue.pop() #Here we pop the element, beeing the first one as previously said.
        lastNode = path[len(path)-1][0]

#After this point, it does exactly the same as in the dfs case, the diference is that it will be using another order for visiting the nodes (BFS).
        if (problem.isGoalState(lastNode)): 				
			return [node[1] for node in path][1:]	

        if not (lastNode in visited):     
			visited.append(lastNode)				
			for x in problem.getSuccessors(lastNode):
				if not (x[0] in visited):
					currentpath = path[:]
					currentpath.append(x)					
					queue.push(currentpath)
	
  

    util.raiseNotDefined()
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    queue = util.PriorityQueue() #In this case we will use the priority queque
    queue.push([[problem.getStartState(), '', 0]],0)
    visited = []

    while not queue.isEmpty():
        path = queue.pop()  
        lastNode = path[len(path)-1][0]
       
        
        if (problem.isGoalState(lastNode)): 				
            return [node[1] for node in path][1:]	

        if not (lastNode in visited):     
            visited.append(lastNode)				
            for x in problem.getSuccessors(lastNode):
                if not (x[0] in visited):
                    currentpath = path[:] 
                    currentpath.append(x)
                    cost = 0;      
                    for x in currentpath: #We get the cost of each path geting the cost of each move in the path
                        cost += x[2]                      
                    queue.push(currentpath, cost) #We push the current path into the queque with the path cost


    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    queue = util.PriorityQueue() #In this case we will also use the priority queque
    queue.push([[problem.getStartState(), '', 0]],0)
    visited = []

    while not queue.isEmpty():
        path = queue.pop()
        lastNode = path[len(path)-1][0]

        
        if (problem.isGoalState(lastNode)): 				
            return [node[1] for node in path][1:]	

        if not (lastNode in visited):     
            visited.append(lastNode)				
            for x in problem.getSuccessors(lastNode):
                if not (x[0] in visited):
                    currentpath = path[:] 
                    currentpath.append(x)
                    cost = 0;      
                    for x in currentpath:   
                        cost += x[2]
                    cost+=heuristic(x[0], problem)  #To the previous cost we add the value of the heuristic.                  
                    queue.push(currentpath, cost)#We push the current path into the queque with the path cost

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
