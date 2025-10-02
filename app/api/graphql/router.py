# app/api/graphql/router.py
from strawberry.fastapi import GraphQLRouter
from app.api.graphql.schema import schema
from app.api.graphql.schemas.queries import Context
from app.db.session import get_db
from typing import AsyncGenerator

# Context getter que maneja correctamente el ciclo de vida de la sesión
async def get_context() -> AsyncGenerator[Context, None]:
    db = next(get_db())
    try:
        yield Context(db)
    finally:
        db.close()

# Crear el router GraphQL con context getter que cierra sesiones
graphql_router = GraphQLRouter(
    schema,
    context_getter=get_context,
    graphiql=True  # Habilita GraphQL Playground en desarrollo
)