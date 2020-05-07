import pandas as pd
import os


class Reader:

    @staticmethod
    def read_level(level):
        if str(level) + '.csv' in os.listdir(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'levels')):

            return pd.read_csv(
                os.path.join(os.path.dirname(os.path.dirname(__file__)), f'levels/{level}.csv'),
                header=None,
                keep_default_na=False
            ).values
        else:
            raise ValueError(f'Level: {level}.csv not found')
