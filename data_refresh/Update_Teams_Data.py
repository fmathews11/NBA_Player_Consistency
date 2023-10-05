# Likely won't be used very often, if at all, but it makes sense to have this.
# This will be used to refresh the parquet file which houses all the team metadata.

from nba_api.stats.static import teams
import pandas as pd
from modules.logger import create_logger

logger = create_logger('DataRefreshLogger', 'info')


def main():
    nba_teams = teams.get_teams()
    output_df = pd.json_normalize(nba_teams)
    output_df.to_parquet("../data/teams_data.gzip", compression='gzip')
    logger.info("Parquet file written - data refreshed")
    return


if __name__ == '__main__':
    main()
