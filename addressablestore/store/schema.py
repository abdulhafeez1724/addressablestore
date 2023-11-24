import graphene
from graphene_django.types import DjangoObjectType
from .models import AppUser, MarketplaceItem
from django.utils.crypto import get_random_string
from django.utils.timezone import now

class UserType(DjangoObjectType):
    class Meta:
        model = AppUser

class MarketplaceItemType(DjangoObjectType):
    class Meta:
        model = MarketplaceItem

class CreateUser(graphene.Mutation):
    class Arguments:
        created_at = graphene.DateTime()

    user = graphene.Field(UserType)

    def mutate(self, info, created_at=None):
        if created_at is None:
            created_at = now()

        unique_id = get_random_string(length=6, allowed_chars='0123456789')
        user = AppUser(unique_id=unique_id, created_at=created_at)
        user.save()
        return CreateUser(user=user)

class CreateMarketplaceItem(graphene.Mutation):
    class Arguments:
        data = graphene.String()
        category = graphene.String()
        status = graphene.String()
        price = graphene.Int()
        listed_by_id = graphene.Int()

    item = graphene.Field(MarketplaceItemType)

    def mutate(self, info, data, category, status, price, listed_by_id):
        user = AppUser.objects.get(pk=listed_by_id)
        item = MarketplaceItem(data=data, category=category, status=status, price=price, listed_by=user)
        item.save()
        return CreateMarketplaceItem(item=item)

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_marketplace_items = graphene.List(MarketplaceItemType)

    def resolve_all_users(self, info, **kwargs):
        return AppUser.objects.all()

    def resolve_all_marketplace_items(self, info, **kwargs):
        return MarketplaceItem.objects.all()

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_marketplace_item = CreateMarketplaceItem.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
