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
    myDepth = 0
    nodeChecks = 0
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

        """
        if self.terminalTest(gameState):
            return None
        #print "get action called"
        self.myDepth = 0
        
        actions = gameState.getLegalActions(0)
        #print "first list of actions: ", actions
        maxIndex = -1

        maxUtil = -99999999
        #print "first minimax completed"
        for i in range(0, len(actions)):
            newUtil = self.minimax(self.nextAgent(0, gameState), gameState.generateSuccessor(0,actions[i]))
            print "ive finished one branch"
            if newUtil > maxUtil:
                maxIndex = i
                maxUtil = newUtil



        "ive returned an action"
        if maxIndex > -1:
            #print "max action: ", actions[maxIndex]
        
            return actions[maxIndex]
        
        
        else:
            print "index is -1"
            return None
        """
        myPly = 0
        actions = gameState.getLegalActions(0)
        maxIndex = -1
        maxUtil = -99999
        if len(actions) == 1:
            return actions[0]
        else:
            for i in range(0,len(actions)):
                newState = gameState.generateSuccessor(0, actions[i])
                utility = self.minimax2(1,newState,1)
                print "various utility: ",utility,"various action: ",actions[i]
                if utility > maxUtil:
                    maxIndex = i
                    maxUtil = utility
        print "max utility:",maxUtil
        return actions[maxIndex]





        util.raiseNotDefined()
    def terminalTest(self, gameState):
        depthBoolean = False
        winBoolean = False
        loseBoolean = False
        if self.myDepth == self.depth:
            depthBoolean = True
            #print "reached depth"
        if gameState.isWin():
            winBoolean = True
            #print "ive won"
        if gameState.isLose():
            loseBoolean = True
            #print "ive lost"


        if depthBoolean or winBoolean or loseBoolean:
            self.myDepth = 0
            return True
        else:
            return False
            
            
    def nextAgent(self, agentIndex, gameState):
        n = gameState.getNumAgents()
        if agentIndex == n-1:
            self.myDepth += 1
            return 0
        else:
            return agentIndex + 1   
            
            
    def minimax(self, agent, gameState):
        actions = gameState.getLegalActions(agent)

        if self.terminalTest(gameState) or len(actions) == 0:
            utility = self.evaluationFunction(gameState)
            return utility
        
        utilList = []
        for a in actions:
            print "agent ", agent, "makes action ",a
            s = gameState.generateSuccessor(agent, a)
            self.nodeChecks += 1
            print "node checks: ",self.nodeChecks
            print "my depth: ",self.myDepth
            utilList.append(self.minimax(self.nextAgent(agent, gameState),s))

        #print utilList
        #print "agent: ", agent
        if agent == 0: #is pacman, a max agent
            print "ive returned a max"
            return max(utilList)
        else: #is ghost, a min agent
            print "ive returned a min"
            return min(utilList)
            
    def minimax2(self, agent, gameState, myPly):
        myDepth = myPly//gameState.getNumAgents() #floor division

        if myDepth == self.depth or gameState.isWin() or gameState.isLose(): #Termination Function
            print "Terminated at depth ",myDepth," out of ",self.depth
            utility = self.evaluationFunction(gameState)
            return utility
        
        utilityList = []
        actions = gameState.getLegalActions(agent)
        newAgent = (agent+1)%gameState.getNumAgents() #generates new agent number

        #populates list with utilities
        for a in actions:
            newState = gameState.generateSuccessor(agent, a)
            utilityList.append(self.minimax2(newAgent,newState,myPly+1))

        #checks if agent is max or min agent and returns max or min
        if agent == 0:
            return max(utilityList)
        else:
            return min(utilityList)
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        myPly = 0
        actions = gameState.getLegalActions(0)
        maxIndex = -1
        maxUtil = -99999
        alpha = -99999
        beta = 99999
        if len(actions) == 1:
            return actions[0]
        else:
            for i in range(0,len(actions)):
                newState = gameState.generateSuccessor(0, actions[i])
                utility = self.alphabeta(1,newState,1,alpha,beta)
                
                #print "various utility: ",utility,"various action: ",actions[i]
                if utility > maxUtil:
                    maxIndex = i
                    maxUtil = utility
                    alpha = max (alpha, utility)
        #print "max utility:",maxUtil
        return actions[maxIndex]
        util.raiseNotDefined()
        
    def alphabeta(self, agent, gameState, myPly, alpha, beta):
        myDepth = myPly//gameState.getNumAgents() #floor division

        if myDepth == self.depth or gameState.isWin() or gameState.isLose(): #Termination Function
            #print "Terminated at depth ",myDepth," out of ",self.depth
            utility = self.evaluationFunction(gameState)
            return utility
        
        
        actions = gameState.getLegalActions(agent)
        nodes = len(actions) #debug code
        newAgent = (agent+1)%gameState.getNumAgents() #generates new agent number

        #checks if agent is max or min agent and returns max or min
        if agent == 0: #agent is MAX
            v = -99999            
            for a in actions:
                newState = gameState.generateSuccessor(agent, a)
                nodes -= 1 #debug code
                v = max(v, self.alphabeta(newAgent,newState,myPly+1,alpha,beta))
                print "beta =", beta
                if v > beta:
                    print "pruning triggered where v=", v, " beta =",beta, " pruned ", nodes, " nodes"
                    return v
                alpha = max(alpha, v)
            return v
            
        else: #agent is MIN
            v = 99999
            for a in actions:

                newState = gameState.generateSuccessor(agent, a)
                nodes -= 1 #debug code
                v = min(v, self.alphabeta(newAgent,newState,myPly+1, alpha, beta))
                

                if v < alpha:
                    #print "pruning triggered where v=", v, " alpha =",alpha, " pruned ", nodes, " nodes"
                    return v
                beta = min(beta, v)
            return v

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

