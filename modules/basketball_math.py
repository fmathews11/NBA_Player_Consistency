def calculate_usage_rate(player_fga: int,
                         player_fta: int,
                         player_to: int,
                         team_fga: int,
                         team_fta: int,
                         team_to: int,
                         player_minutes: int) -> float:

    """
    Estimates the percentage of team plays USED by a player when he was on the floor.
    The term "used" means the number of possessions where the player:
      - made a shot
      - missed a shot (the ideal formula would incorporate whether the missed shot resulted in an OR/DR
      - Turned the ball over"
      - Fouled in the act of shooting, resulting in a trip to the charity stripe.

      No matter where you look, there are many different interpretations or iterations of this formula.
      Some include assists (weighted much lower) while others don't.  Some include pace, where others dont.

      Here I'm using the formula as described by Basketball Reference.  It seems to be a good "middle ground"
      with respect to complexity and being all-encompassing.

      :param player_fga: int - The number of field goals attempted by the player
      :param player_fta: int - The number of free throws attempted by the player
      :param player_to: int - The number of turnovers attempted by the player
      :param team_fga: int - The number of field goals attempted by the team
      :param team_fta: int - The number of free throws attempted by the team
      :param team_to: int - The number of turnovers committed by the team
      :param player_minutes: - The total number of minutes played by the player

      :return: float - A value representing the player's usage percentage
      """

    # 240 total team minutes in an NBA game.  Keeping the variable name to be explicit
    total_team_minutes = 240

    numerator = 100 * ((player_fga + (0.44 * player_fta) + player_to) * (total_team_minutes / 5))
    denominator = (player_minutes * (team_fga + (0.44 * team_fta) + team_to))
    return numerator/denominator

def test_func(param:int) -> None:

    """

    :param param:
    :return:
    """