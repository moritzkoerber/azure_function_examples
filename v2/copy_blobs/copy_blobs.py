import io
import logging

import azure.functions as func
import pandas as pd

logging.basicConfig()

copy_blobs_bp = func.Blueprint()


@copy_blobs_bp.blob_trigger(
    arg_name="obj",
    path="mycontainer/{name}.csv",  # only copy csv files
    connection="STA_CONN_STRING",  # for local:"StorageConnectionString",
)
@copy_blobs_bp.blob_input(
    arg_name="inputblob",
    path="mycontainer/{name}.csv",
    connection="STA_CONN_STRING",
    data_type="binary",  # binary, stream, or string
)
@copy_blobs_bp.blob_input(
    arg_name="inputblobstr",
    path="mycontainer/{name}.csv",
    connection="STA_CONN_STRING",
    data_type="string",
)
@copy_blobs_bp.blob_output(
    arg_name="outputblob",
    path="myothercontainer/{name}.csv",
    connection="STA_CONN_STRING",
)
def copy_blobs(
    obj: func.InputStream,
    inputblob: bytes,
    inputblobstr: str,
    outputblob: func.Out[bytes],
):
    logging.info("Processing %s", obj.name)

    # type(inputblob) is bytes, type(inputblobstr) is str
    df1 = pd.read_csv(io.BytesIO(inputblob))
    df2 = pd.read_csv(io.StringIO(inputblobstr))
    logging.info("df1: %s\ndf2: %s", df1.head(), df2.head())

    # set inputblob as outputblob to copy it
    outputblob.set(inputblob)
