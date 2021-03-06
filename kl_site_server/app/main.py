from datetime import datetime, timedelta
from typing import Type

from kl_site_common.const import DATA_PERIOD_DAYS, DATA_PERIOD_MINS
from kl_site_common.utils import print_log
from kl_site_server.client import TouchanceDataClient
from kl_site_server.model import TouchancePxRequestParams
from tcoreapi_mq.model import configs_sources_as_symbols

from .socket import register_handlers


latest_date: datetime = datetime.utcnow() + timedelta(hours=1)


def start_server_app(
    client_cls: Type[TouchanceDataClient] | None = TouchanceDataClient, *,
    period_mins: list[int] | None = None,
    period_days: list[int] | None = None
):
    client = client_cls()
    client.start()

    for symbol_obj in configs_sources_as_symbols():
        print_log(f"[Server] Requesting Px data of [yellow]{symbol_obj.symbol_complete}[/yellow]")
        params = TouchancePxRequestParams(
            symbol_obj=symbol_obj,
            period_mins=(
                period_mins if period_mins is not None else [period_min["min"] for period_min in DATA_PERIOD_MINS]
            ),
            period_days=(
                period_days if period_days is not None else [period_day["day"] for period_day in DATA_PERIOD_DAYS]
            ),
            history_range_1k=(latest_date - timedelta(days=35), latest_date),
            history_range_dk=(latest_date - timedelta(days=365 * 3), latest_date),
        )

        client.request_px_data(params)

    register_handlers(client)
