import io
import logging
import os

import azure.functions as func
import polars as pl

logging.basicConfig()

write_delta_table_bp = func.Blueprint()


@write_delta_table_bp.blob_trigger(
    arg_name="blob", path="mycontainer/{name}.parquet", connection="STA_CONN_STRING"
)
def delta_table_func(blob: func.InputStream):
    # type(blob.read()) is bytes
    df = pl.read_parquet(io.BytesIO(blob.read()))

    df.write_delta(
        "abfss://test/delta_table",
        mode="overwrite",
        storage_options={
            "account_name": os.environ["AZ_STA_NAME"],
            "account_key": os.environ["AZ_STA_KEY"],
        },
    )

    logging.info(df.head())
