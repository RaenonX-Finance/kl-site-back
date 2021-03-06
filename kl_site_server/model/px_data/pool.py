from typing import TYPE_CHECKING

from pandas import DataFrame

from kl_site_common.const import DATA_SOURCES
from kl_site_server.calc import calc_pool, calc_support_resistance_levels
from tcoreapi_mq.message import RealtimeData
from .model import PxData

if TYPE_CHECKING:
    from kl_site_server.model import BarDataDict


class PxDataPool:
    def __init__(
        self, *,
        symbol: str,
        bars: list["BarDataDict"],
        min_tick: float,
        decimals: int,
        latest_market: RealtimeData,
    ):
        if not bars:
            raise ValueError(f"PxData should be initialized with data ({symbol} @ Pool)")

        try:
            source_of_symbol = next(data_source for data_source in DATA_SOURCES if data_source["symbol"] == symbol)
        except StopIteration as ex:
            raise ValueError(f"Symbol `{symbol}` is not included in data source list") from ex

        self.symbol: str = symbol
        self.symbol_name: str = source_of_symbol["name"]
        self.min_tick: float = min_tick
        self.decimals: int = decimals
        self.latest_market: RealtimeData | None = latest_market

        self.dataframe: DataFrame = DataFrame(bars)
        self.dataframe = calc_pool(self.dataframe, self.symbol)

        self.sr_levels_data = calc_support_resistance_levels(self.dataframe, self.symbol)

    def to_px_data(self, period_min: int) -> PxData:
        return PxData(pool=self, period_min=period_min)
