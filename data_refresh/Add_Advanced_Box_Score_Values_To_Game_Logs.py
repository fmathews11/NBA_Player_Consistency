import pandas as pd
from nba_api.stats.endpoints.boxscoreadvancedv3 import BoxScoreAdvancedV3
from modules.logger import create_logger
import time
import numpy as np

logger = create_logger("DataStatusLoger", 'info')
SEASON = 2022

_custom_headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://www.nba.com',
    'Referer': 'https://www.nba.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def main(dataframe_to_modify_path: str) -> None:
    # Create a counter to write the parquet file every 20 iterations
    write_counter = 0
    input_df = pd.read_parquet(dataframe_to_modify_path)
    output_df = pd.DataFrame()
    all_game_ids = input_df.Game_ID.unique().tolist()

    logger.info("Beginning data pull")
    for idx, game_id in enumerate(all_game_ids):

        if not output_df.empty and game_id in set(output_df.Game_ID.unique().tolist()):
            continue

        advanced_box_score_data = BoxScoreAdvancedV3(game_id=game_id, headers=_custom_headers)
        target_data = advanced_box_score_data.get_data_frames()[0]
        df_to_concat = input_df.merge(target_data,
                                      left_on=['Game_ID', 'Player_ID'],
                                      right_on=['gameId', 'personId'])
        output_df = pd.concat([output_df, df_to_concat])

        write_counter += 1
        if write_counter == 20:
            logger.info(f"Saving parquet file iteratively: number {idx} of {len(all_game_ids)}")
            output_df.to_parquet(f"../data/active_player_game_logs_{SEASON}_advanced.gzip",
                                 compression='gzip',
                                 index=False)
            write_counter = 0

        # Sleep
        time.sleep(np.random.randint(2, 4))

    logger.info("Saving final parquet file")
    output_df.to_parquet(f"../data/active_player_game_logs_{SEASON}_advanced.gzip",
                         compression='gzip',
                         index=False)
    logger.info("Finished")

    return


if __name__ == '__main__':
    main('../data/active_player_game_logs_2022.gzip')
