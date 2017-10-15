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
        #print successorGameState
        newPos = successorGameState.getPacmanPosition()
        #print newPos
        newFood = successorGameState.getFood()
        #print newFood
        newGhostStates = successorGameState.getGhostStates()
        newGhostPositions = [ghostState.getPosition() for ghostState in newGhostStates]
        #print newGhostPositions
        #print newGhostStates
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #print newScaredTimes

        "*** YOUR CODE HERE ***"
        #print "returning: ", successorGameState.getScore()
        
        result = 0
        if newPos in newFood.asList(): result += 10
        if self.isAdjacent(newPos, newGhostPositions): result -= 100
        if newPos in newGhostPositions: result -= 9000
        result += successorGameState.getScore()
        result += 10 * (1/float(self.findNearestDistance(newPos, newFood.asList()))) 
        
        
        
        
        #return successorGameState.getScore()
        return result
    
    def isAdjacent(self, newPos, nGPs):
        north = newPos[0], newPos[1] + 1
        south = newPos[0], newPos[1] - 1
        east = newPos[0] + 1, newPos[1]
        west = newPos[0] - 1, newPos[1]
        
        if north in nGPs or south in nGPs or east in nGPs or west in nGPs: return True
        return False
        
        
    def findNearestDistance(self, position, foodList):
        myQ = util.PriorityQueue()
        for f in foodList:
        
            myQ.push(f, util.manhattanDistance(position, f))
    
    
        shortList = []
        c = 0
        while not myQ.isEmpty():
            if c < 10:
                coords = myQ.pop()
                #print "coords: ", coords
                x,y = coords
                shortList += (x,y)
                c += 1
                #print "shortlist: ", shortList
            if c == 5:
                break
    
        #print "shortlist: ",shortList
        #2. Examine the shortlist and find the nearest food
        nearest = None
        mazeDist = 999999
        pair = (1,1)
        for i in range(0,len(shortList) - 1):
            if i % 2 == 0:
                pair = shortList[i],shortList[i+1]
                mD = util.manhattanDistance(position, pair)
            
                if mD < mazeDist:
                
                    mazeDist = mD 
                    nearest = pair
                
        x1,y1 = pair
    
   
    
        return mazeDist

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
    myDepth = 1

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
        """
        ghostStates = gameState.getGhostStates()
        ghostPositions = [ghostState.getPosition() for ghostState in ghostStates]
        
        
            
        if self.index == 0:
            myDepth += 1
            return max(map(getAction, generateSuccessor(gameState, 
        """
         
        
        actions = gameState.getLegalActions(0)
        maxIndex = 0

        maxUtil = self.minimax(1, gameState.generateSuccessor(0, actions[0]))
        
        for i in range(1, len(actions)):
            newUtil = self.minimax(1, gameState.generateSuccessor(0,actions[i]))
            if newUtil > maxUtil:
                maxIndex = i
                maxUtil = newUtil
        return actions[maxIndex]
        
        
        
        util.raiseNotDefined()
    
    def nextAgent(self, agentIndex, gameState):
        n = gameState.getNumAgents()
        if agentIndex == n-1:
            return 0
        else:
            return agentIndex + 1
        
    
    def minimax(self, agent, gameState):
        #print "agent: ", agent
        #print "food list: ",gameState
        if self.myDepth == self.depth or gameState.isWin() or gameState.isLose():
        #if self.myDepth == self.depth or gameState.getNumFood == 0 or gameState.getPacmanPosition() in ghostPositions:
            self.myDepth = 0
            return self.evaluationFunction(gameState)
        
        
        actions = gameState.getLegalActions(agent)
        utilList = []
        for a in actions:
            s = gameState.generateSuccessor(agent, a)
            utilList.append(self.minimax(self.nextAgent(agent, gameState),s))
            if agent == 0: #is pacman, a max agent
                return max(utilList)
            else: #is ghost, a min agent
                return min(utilList)
        
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
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

