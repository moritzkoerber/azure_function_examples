import asyncio

import aiohttp
import azure.functions as func

http_async_exec_bp = func.Blueprint()


@http_async_exec_bp.route(route="http_trigger_async_exec")
def http_trigger_async_execution(req: func.HttpRequest) -> func.HttpResponse:
    async def query_current_time(session: aiohttp.ClientSession, tz: str):
        async with session.get(
            f"http://worldtimeapi.org/api/timezone/{tz}"
        ) as response:
            data = await response.json()
            print(f"In timezone {tz} it is currently {data['datetime']}")

    async def main():
        timezones = ["Europe/Berlin", "America/New_York", "Asia/Tokyo"]
        async with aiohttp.ClientSession() as s:
            async with asyncio.TaskGroup() as tg:
                for tz in timezones:
                    tg.create_task(query_current_time(s, tz))

    asyncio.run(main())
    return func.HttpResponse(status_code=200)
