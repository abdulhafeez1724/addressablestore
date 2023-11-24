import graphene
from graphene_django.types import DjangoObjectType
from .models import LoginUser, MarketplaceItem

class UserType(DjangoObjectType):
    class Meta:
        model = LoginUser

class MarketplaceItemType(DjangoObjectType):
    class Meta:
        model = MarketplaceItem

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_marketplace_items = graphene.List(MarketplaceItemType)

    def resolve_all_users(self, info, **kwargs):
        return LoginUser.objects.all()

    def resolve_all_marketplace_items(self, info, **kwargs):
        return MarketplaceItem.objects.all()

schema = graphene.Schema(query=Query)