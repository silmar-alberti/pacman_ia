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
import sys

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

        "*** YOUR CODE HERE ***"

        self.ghostEvaluation(successorGameState)

        if successorGameState.isWin():
            return float("inf")


        distfromghost = self.ghostEvaluation(successorGameState)

        score = successorGameState.getScore() + distfromghost

        distFood = self.getFoodDist(successorGameState)

        if action == Directions.STOP:
            score -= 1
        score -= distFood*1.8

        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
            score += 100

        capsuleplaces = currentGameState.getCapsules()
        if successorGameState.getPacmanPosition() in capsuleplaces:
            score += 300

        return score

    def getFoodDist(self,gameState):
        newFood = gameState.getFood()
        newPos = gameState.getPacmanPosition()
        foodlist = newFood.asList()
        closestfood = 1000
        for foodpos in foodlist:
            thisdist = util.manhattanDistance(foodpos, newPos)
            if (thisdist < closestfood):
                closestfood = thisdist

        return thisdist

    def ghostEvaluation(self, state):
        ghostsArray = state.getGhostStates()
        pos = state.getPacmanPosition()
        minDist = sys.maxint
        for ghost in ghostsArray:
            ghostposition = ghost.getPosition()
            distfromghost = util.manhattanDistance(ghostposition, pos)
            if(distfromghost < minDist):
                minDist = distfromghost

        return minDist


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
      to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

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
      Your minimax agent (question 7)
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
        a =  self.maxplayer(gameState, 0)
        return a[1]

    def maxplayer(self, gameState, depth):
        if depth == self.depth:
            return (self.evaluationFunction(gameState), None)

        actionList = gameState.getLegalActions(0)
        bestScore = -sys.maxint
        bestAction = None

        if len(actionList) == 0:
            return (self.evaluationFunction(gameState), None)

        for action in actionList:
            newState = gameState.generateSuccessor(0, action)
            newScore = self.minplayer(newState, 1, depth)
            if (newScore > bestScore):
                bestScore, bestAction = newScore, action

        return (bestScore, bestAction)

    def minplayer(self, gameState, agentIndex, depth):
        actionList = gameState.getLegalActions(agentIndex)
        bestScore = sys.maxint


        if len(actionList) == 0:
            return self.evaluationFunction(gameState)

        for action in actionList:
            newState = gameState.generateSuccessor(agentIndex, action)
            if (agentIndex +1 == gameState.getNumAgents()):
                newScore = self.maxplayer(newState, depth + 1)[0]
            else:
                newScore = self.minplayer(newState, agentIndex + 1, depth)

            if (newScore < bestScore):
                bestScore= newScore

        return bestScore



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 8)
    """

    def getAction(self, gameState):

        def maxplayer(gameState, depth):
            if depth == self.depth:
                return (self.evaluationFunction(gameState),None)

            actionList = gameState.getLegalActions(0)
            bestScore = -sys.maxint
            bestAction = None

            if len(actionList) == 0:
                return (self.evaluationFunction(gameState),None)

            for action in actionList:
                newState = gameState.generateSuccessor(0, action)
                newScore = medPlayer(newState, 1, depth)
                if (newScore > bestScore):
                    (bestScore , bestAction) = (newScore,action)

            return (bestScore,bestAction)

        def medPlayer( gameState, agentIndex, depth):
            actionList = gameState.getLegalActions(agentIndex)
            bestScore = 0

            if len(actionList) == 0:
                return self.evaluationFunction(gameState)

            for action in actionList:
                newState = gameState.generateSuccessor(agentIndex, action)
                if (agentIndex + 1 == gameState.getNumAgents()):
                    newScore = maxplayer(newState, depth + 1)[0]
                else:
                    newScore = medPlayer(newState, agentIndex + 1, depth)

                bestScore = newScore + bestScore

            return bestScore / len(actionList)

        a = maxplayer(gameState, 0)[1]
        return a


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 9).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

    def getMinFoodDist(gameState):
        newFood = gameState.getFood()
        newPos = gameState.getPacmanPosition()
        foodlist = newFood.asList()
        nearFoods = 0
        medFoodDist = 0
        closestfood = sys.maxint

        for foodpos in foodlist:
            thisdist = util.manhattanDistance(foodpos, newPos)
            if (thisdist < closestfood):
                closestfood = thisdist
            if thisdist == 1:
                nearFoods +=1
            medFoodDist += thisdist

        if len(foodlist) > 2:
            medFoodDist = medFoodDist/ len(foodlist)
        else:
            medFoodDist = thisdist



        return thisdist, nearFoods, medFoodDist



    def ghostEvaluation(state):
        ghostsArray = state.getGhostStates()
        pos = state.getPacmanPosition()
        minDist = sys.maxint

        for ghost in ghostsArray:
            ghostposition = ghost.getPosition()
            distfromghost = util.manhattanDistance(ghostposition, pos)
            if (distfromghost < minDist):
                minDist = distfromghost

        return minDist

    if currentGameState.isWin():
        return sys.maxint
    if currentGameState.isLose():
        return -sys.maxint -1

    distfromghost = ghostEvaluation(currentGameState)

    newFood = currentGameState.getFood()
    numFoods = len(newFood.asList())

    score = currentGameState.getScore()

    distFood,nearFood,medFoodDist = getMinFoodDist(currentGameState)

    score =  -  (medFoodDist-1) +\
             - numFoods \
            + 0.2 * distfromghost\
            + 1.5 * score\
            + 0.5 * nearFood\


    return score



# Abbreviation
better = betterEvaluationFunction

