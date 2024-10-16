import aiohttp
import azure.functions as func

http_async_bp = func.Blueprint()


@http_async_bp.route(route="http_trigger_async", auth_level=func.AuthLevel.ANONYMOUS)
async def http_trigger_async(req: func.HttpRequest) -> func.HttpResponse:
    url = req.params.get("url") or req.get_json().get("url")
    if not url:
        return func.HttpResponse(
            "Please pass a valid worldtimeapi url",
            status_code=500,
        )
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as response:
            data = await response.json()
            return func.HttpResponse(f"It is currently {data['datetime']}")
