import io
import logging

import azure.functions as func
import pandas as pd

logging.basicConfig()

bp = func.Blueprint()


@bp.blob_trigger(
    arg_name="blob",
    path="mycontainer/subfolder/{name}.csv",
    connection="STA_CONN_STRING",
)
def do_something_blob(blob: func.InputStream):
    # type(blob.read()) is bytes
    df = pd.read_csv(io.BytesIO(blob.read()))
    logging.debug(df.head())
    logging.debug("Processed %s", blob.name)
