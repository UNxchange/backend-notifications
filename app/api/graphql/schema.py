# app/api/graphql/schema.py
import strawberry
from app.api.graphql.schemas.queries import Query
from app.api.graphql.schemas.mutations import Mutation

# Crear el schema GraphQL principal
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)