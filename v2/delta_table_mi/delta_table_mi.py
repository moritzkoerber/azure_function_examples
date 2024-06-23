import io
import logging
import os

import azure.functions as func
import polars as pl

logging.basicConfig()

bp = func.Blueprint()


@bp.blob_trigger(
    arg_name="blob", path="mycontainer/delta/{name}.parquet", connection="STA_MI_CONN"
)
def delta_table_func_mi(blob: func.InputStream):
    # type(blob.read()) is bytes
    df = pl.read_parquet(io.BytesIO(blob.read()))
    df.write_delta(
        "abfss://test/test_mi/delta_table",
        mode="overwrite",
        storage_options={
            "account_name": os.environ["AZ_STA_NAME"],
            "azure_msi_endpoint": os.environ["IDENTITY_ENDPOINT"],
        },
    )
    print(df)
