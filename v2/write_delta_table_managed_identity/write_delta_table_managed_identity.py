import io
import logging
import os

import azure.functions as func
import polars as pl

logging.basicConfig()

write_delta_table_mi_bp = func.Blueprint()


@write_delta_table_mi_bp.blob_trigger(
    arg_name="blob",
    path="mycontainer/delta_mi/{name}.parquet",
    connection="STA_MI_CONN",
)
def delta_table_func_mi(blob: func.InputStream):
    # type(blob.read()) is bytes
    df = pl.read_parquet(io.BytesIO(blob.read()))

    df.write_delta(
        "abfss://mycontainer/delta_table_mi",
        mode="overwrite",
        storage_options={
            "account_name": os.environ["AZ_STA_NAME"],
            "azure_msi_endpoint": os.environ["IDENTITY_ENDPOINT"],
        },
    )

    logging.info(df.head())
