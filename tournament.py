# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    query = '''DELETE FROM matches;'''
    c.execute(query)
    c.execute("UPDATE player SET matches = 0, wins = 0")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    query = "DELETE FROM player;"
    c.execute(query)
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(ID) FROM player;")
    totalP = c.fetchone()
    DB.close()
    return totalP[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO player(name, wins, matches)  VALUES (%s, 0, 0);", (name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM player ORDER BY wins DESC;")
    playerS = [(players[0], str(players[1]), players[2], players[3]) for players in c.fetchall()]
    DB.close()
    return playerS


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    #Update winner
    c.execute("SELECT wins, matches FROM player WHERE ID = %d;" % winner )
    r = c.fetchall()
    c.execute("UPDATE player SET wins = %s WHERE ID = %s;", (int(r[0][0]) + 1, winner))
    c.execute("UPDATE player SET matches = %s WHERE ID = %s;", (int(r[0][1]) + 1, winner))
    #Update loser
    c.execute("SELECT matches FROM player WHERE ID = %s;", (loser,))
    r = c.fetchall()
    c.execute("UPDATE player SET matches = %s WHERE ID = %s;", (int(r[0][0]) + 1, loser))
    DB.commit()
    DB.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    playerS = playerStandings()
    pairs = []
    for k in range(0, len(playerS), 2):
        pairs.append((playerS[k][0], playerS[k][1],  playerS[k+1][0], playerS[k+1][1]))
    return pairs

