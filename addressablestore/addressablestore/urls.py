from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from store.schema import schema as storeschema
from .schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
     path("local", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
     path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=storeschema))),
]
