import azure.functions as func

http_bp = func.Blueprint()


@http_bp.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> str:
    return f"Hello, {req.params.get('name')}!"
