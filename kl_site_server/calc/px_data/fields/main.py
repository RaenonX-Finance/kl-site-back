import numpy as np
from pandas import DataFrame

from .candlestick import calc_candlestick
from .diff import calc_diff
from .ema import calc_ema
from .epoch_sec_time import calc_epoch_sec_time
from .market_date import calc_market_date
from .strength import calc_strength
from .tie_point import calc_tie_point


def calc_model(df: DataFrame, period_min: int) -> DataFrame:
    df = calc_diff(df)
    df = calc_candlestick(df)
    df = calc_ema(df)
    df = calc_tie_point(df, period_min)

    # Remove NaNs
    df = df.fillna(np.nan).replace([np.nan], [None])

    # Keep last 1000 rows only
    df = df.tail(1000)

    return df


def calc_pool(df_1k: DataFrame, symbol: str) -> DataFrame:
    df_1k = calc_epoch_sec_time(df_1k)
    df_1k = calc_market_date(df_1k, symbol)
    df_1k = calc_strength(df_1k)

    # Remove NaNs
    df_1k = df_1k.fillna(np.nan)

    return df_1k
