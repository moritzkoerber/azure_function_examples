import io
import logging

import azure.functions as func
import pandas as pd

logging.basicConfig()

simple_blob_trigger_mi_bp = func.Blueprint()


@simple_blob_trigger_mi_bp.blob_trigger(
    arg_name="blob",
    path="mycontainer/othersubfolder/{name}.csv",
    connection="STA_MI_CONN",
)
def do_something_blob_mi(blob: func.InputStream):
    # type(blob.read()) is bytes
    df = pd.read_csv(io.BytesIO(blob.read()))
    logging.info(df.head())
    logging.info("Processed %s using the managed identity", blob.name)
