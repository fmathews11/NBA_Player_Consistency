from nba_api.stats.static import players
from modules.logger import create_logger
import pandas as pd
from nba_api.stats.endpoints import playergamelog
import time
import numpy as np

# Get all active players
active_players = players.get_active_players()
# Establish season constant
SEASON = 2022
# Create Logger
logger = create_logger("DataStatusLoger", 'info')


def main():
    # Create a counter to write the parquet file every 20 iterations
    write_counter = 0

    # Instantiate final output dataframe
    master_df = pd.DataFrame()

    for idx, player in enumerate(active_players):
        logger.debug(f"Getting data for {player['first_name']} {player['last_name']}")
        temp_df = playergamelog.PlayerGameLog(player_id=player['id'], season=SEASON).get_data_frames()[0]
        temp_df['First_Name'] = player['first_name']
        temp_df['Last_Name'] = player['last_name']
        master_df = pd.concat([master_df, temp_df])

        write_counter += 1
        if write_counter == 20:
            logger.info(f"Saving parquet file iteratively: number {idx} of {len(active_players)}")
            master_df.to_parquet(f"../data/active_player_game_logs_{SEASON}.gzip", compression='gzip', index=False)
            write_counter = 0

        # Sleep
        time.sleep(np.random.randint(2, 4))

    logger.info("Reconfiguring column order")
    column_names = master_df.columns.tolist()
    column_names.insert(1, column_names.pop(column_names.index('First_Name')))
    column_names.insert(2, column_names.pop(column_names.index('Last_Name')))
    master_df = master_df.loc[:, column_names]

    logger.info("Saving final parquet file")
    master_df.to_parquet(f"../data/active_player_game_logs_{SEASON}.gzip", compression='gzip', index=False)
    logger.info("Finished")
    return


if __name__ == '__main__':
    main()
