from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.services import auth_service as AuthService

IGNORE_ROUTES = ['auth', 'docs', 'openapi.json']

class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        path = request.url._url.split(":8000/")[1]
        route = path.split("/")[0]

        if route not in IGNORE_ROUTES:
            print(">>> Rota protegida! Requisição passando pelo middleware de autenticação....")
            cookie = request.headers.get('Authorization')

            if not cookie:
                return JSONResponse(content="Cookie não encontrado!", status_code=401)

            if not AuthService.is_cookie_valid(cookie):
                return JSONResponse(content="Cookie não é válido!", status_code=401)
            
        response = await call_next(request)

        return response