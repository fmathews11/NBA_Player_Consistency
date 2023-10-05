import pandas as pd


def coerce_numeric_columns_to_numeric_datatype(input_dataframe: pd.DataFrame) -> pd.DataFrame:
    """Changes data types of numeric columns only and returns a copied version of the original data frame"""

    df = input_dataframe.copy()

    for column in df.columns.tolist():
        # Skip anything resembling a date
        if "DATE" in column.upper():
            continue

        # Attempt to coerce to numeric, skip if unsuccessful
        try:
            df[column] = pd.to_numeric(df[column])
        except ValueError as e:
            message = str(e)
            if message.startswith("Unable to parse"):
                continue
            raise
    return df


def identify_home_and_away_team(input_string: str) -> tuple[str, str]:
    """This function is designed to 'read' the MATCHUP field in a box score dataframe
    and parse out the home and away team.

    The value returned as a tuple in which the first element will ALWAYS be the home team,the second element
    will represent the away team."""

    if "@" in input_string:
        home_team, away_team = input_string.split("@")[1].strip(), input_string.split("@")[0].strip()
    else:
        home_team, away_team = input_string.split("vs.")[0].strip(), input_string.split("vs.")[1].strip()

    return home_team, away_team


def add_home_and_away_team_to_player_game_logs(input_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Parses out the home and away teams and adds a column for each, returning a dataframe with the `MATCHUP` field
    removed, and `HOME_TEAM` and `AWAY_TEAM` columns added
    """

    df = input_dataframe.copy()
    home_away_df = df[['Game_ID', 'MATCHUP']].drop_duplicates()
    home_away_list = home_away_df.MATCHUP.map(identify_home_and_away_team).tolist()
    home_teams = [i[0] for i in home_away_list]
    away_teams = [i[1] for i in home_away_list]
    home_away_df['HOME_TEAM'] = home_teams
    home_away_df['AWAY_TEAM'] = away_teams
    home_away_df = home_away_df.drop("MATCHUP", axis=1)
    return home_away_df.merge(df, left_on='Game_ID', right_on='Game_ID', how='inner').drop("MATCHUP", axis=1)


def clean_player_game_log_data(input_dataframe: pd.DataFrame) -> pd.DataFrame:

    """Applies several cleaning & transformation functions to a data frame of player game logs"""

    df = input_dataframe.copy()
    # Coerce game date to pd.DateTime
    df.GAME_DATE = pd.to_datetime(df.GAME_DATE)
    # Coerce appropriate columns to numeric
    df = coerce_numeric_columns_to_numeric_datatype(df)
    # Identify home and away team
    df = add_home_and_away_team_to_player_game_logs(df)
    return df
