import azure.functions as func
from copy_blobs.copy_blobs import copy_blobs_bp
from http_trigger.http_trigger import http_bp
from http_trigger_async.http_trigger_async import http_async_bp
from http_trigger_async_exec.http_trigger_async_execution import http_async_exec_bp
from simple_blob_trigger.simple_blob_trigger import simple_blob_trigger_bp
from simple_blob_trigger_managed_identity.simple_blob_trigger_managed_identity import (
    simple_blob_trigger_mi_bp,
)
from write_delta_table.write_delta_table import write_delta_table_bp
from write_delta_table_managed_identity.write_delta_table_managed_identity import (
    write_delta_table_mi_bp,
)

app = func.FunctionApp()

app.register_functions(copy_blobs_bp)
app.register_functions(http_bp)
app.register_functions(http_async_bp)
app.register_functions(http_async_exec_bp)
app.register_functions(simple_blob_trigger_bp)
app.register_functions(simple_blob_trigger_mi_bp)
app.register_functions(write_delta_table_bp)
app.register_functions(write_delta_table_mi_bp)
