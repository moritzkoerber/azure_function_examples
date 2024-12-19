# Azure Function Examples

This repo contains various examples of Azure Functions, for example a v1 http trigger, a v2 http trigger, a v2 blob trigger, blob copying, using a function's managed identity, delta tables, asyncio etc.

The repo features functions of both programming model v1 and v2 – mainly v2 though. The repo also contains an Azure Devops pipeline (yaml) to deploy the underlying infrastructure (via Terraform) and the code to the function apps.

## Functions

```
v1/
└── http_trigger: an http-triggered function using the v1 programming model

v2/
├── copy_blobs: a blob-triggered function that copies the blob to a new location
├── http_trigger: an http-triggered function using the v2 programming model
├── http_trigger_async: an http-triggered function that can be run/triggered asynchronously (with async)
├── http_trigger_async_exec: an http-triggered function that executes its code asynchronously (with async)
├── simple_blob_trigger: a blob-triggered function
├── simple_blob_trigger_managed_identity: a blob-triggered function authenticating through the function's managed identity
├── write_delta_table: a blob-triggered function writing a delta table with polars
└── write_delta_table_managed_identity: a blob-triggered function writing a delta table with polars authenticating through the function's managed identity
```
