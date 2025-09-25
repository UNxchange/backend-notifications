# app/api/graphql/router.py
from strawberry.fastapi import GraphQLRouter
from app.api.graphql.schema import schema
from app.api.graphql.schemas.queries import Context

# Crear el router GraphQL
graphql_router = GraphQLRouter(
    schema,
    context_getter=lambda: Context(),
    graphiql=True  # Habilita GraphQL Playground en desarrollo
)