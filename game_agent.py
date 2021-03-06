"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import itertools

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    center_result = center_score(game, player)

    return float(own_moves - opp_moves * 2 - center_result * center_result)

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves - opp_moves + center_score(game, player))

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves - center_score(game, player))

def center_score(game, player):
    """Outputs a score equal to square of the distance from the center of the
    board to the position of the player.

    This heuristic is only used by the autograder for testing.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    return float((h - y)**2 + (w - x)**2)

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return -1, -1

        _, best_move = max([(self.score(game.forecast_move(m), self), m) for m in legal_moves])

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            return best_move

        # Return the best move from the last completed search iteration
        return best_move

    def time_check(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return

    def min_value(self, game, depth):
        self.time_check()

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return float("-inf")

        if depth == 1:
            return min([self.score(game.forecast_move(m), self) for m in legal_moves])

        return min([self.max_value(game.forecast_move(m), depth-1) for m in legal_moves])

    def max_value(self, game, depth):
        self.time_check()

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return float("-inf")

        if depth == 1:
            return max([self.score(game.forecast_move(m), self) for m in legal_moves])

        return max([self.min_value(game.forecast_move(m), depth - 1) for m in legal_moves])

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        self.time_check()

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return float("-inf"), (-1, -1)

        if depth == 1:
            _, move = max([(self.score(game.forecast_move(m), self), m) for m in legal_moves])
            return  move

        _, move = max([(self.min_value(game.forecast_move(m), depth-1), m) for m in legal_moves])

        return move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return -1, -1

        _, best_move = max([(self.score(game.forecast_move(m), self), m) for m in legal_moves])

        self.time_left = time_left

        for depth in itertools.count(start=0, step=1):
            try:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.
                best_move = self.alphabeta(game, depth)
            except SearchTimeout:
                return best_move

        # Return the best move from the last completed search iteration
        return best_move

    def time_check(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return

    def ab_min_value(self, game, depth, alpha, beta):
        self.time_check()

        if alpha >= beta:
            return alpha

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return float("inf")

        current_min = float("+inf")

        if depth <= 1:
            for current_move in legal_moves:
                min_from_child = self.score(game.forecast_move(current_move), self)

                if min_from_child <= alpha:
                    return min_from_child

                current_min = min(current_min, min_from_child)

            return current_min

        for current_move in legal_moves:
            min_from_child = self.ab_max_value(game.forecast_move(current_move), depth-1, alpha, beta)

            current_min = min(current_min, min_from_child)

            if current_min <= alpha:
                return current_min

            beta = min(beta, current_min)

        return current_min

    def ab_max_value(self, game, depth, alpha, beta):
        self.time_check()

        if alpha >= beta:
            return beta

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return float("-inf")

        current_max = float("-inf")

        if depth <= 1:
            for current_move in legal_moves:
                max_from_child = self.score(game.forecast_move(current_move), self)

                if max_from_child >= beta:
                    return max_from_child

                current_max = max(current_max, max_from_child)

            return current_max

        for current_move in legal_moves:
            max_from_child = self.ab_min_value(game.forecast_move(current_move), depth-1, alpha, beta)

            current_max = max(current_max, max_from_child)

            if current_max >= beta:
                return current_max

            alpha = max(alpha, current_max)

        return current_max

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        self.time_check()

        legal_moves = game.get_legal_moves()

        current_max = float("-inf")
        maximizing_move = (-1, -1)

        if not legal_moves:
            return maximizing_move

        if alpha >= beta:
            return -1, -1

        maximizing_move = legal_moves[0]

        if depth <= 1:
            for current_move in legal_moves:
                max_from_child = self.score(game.forecast_move(current_move), self)

                if max_from_child > current_max:
                    current_max = max_from_child
                    maximizing_move = current_move

                if current_max >= beta:
                    return maximizing_move

            return maximizing_move

        for legal_move in legal_moves:
            max_from_child = self.ab_min_value(game.forecast_move(legal_move), depth-1, alpha, beta)

            if max_from_child > current_max:
                current_max = max_from_child
                maximizing_move = legal_move

            if current_max >= beta:
                return maximizing_move

            alpha = max(current_max, alpha)

        return maximizing_move
