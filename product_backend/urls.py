from django.urls import path
from graphene_django.views import GraphQLView

from graphene_django.views import GraphQLView

urlpatterns = [
    # other urls...
    path('graphql/', GraphQLView.as_view(graphiql=True)),
]
