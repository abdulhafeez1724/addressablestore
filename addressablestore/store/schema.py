import graphene
from graphene_django.types import DjangoObjectType
from .models import AppUser, Listing


class UserType(DjangoObjectType):
    class Meta:
        model = AppUser

class ListingType(DjangoObjectType):
    class Meta:
        model = Listing

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_listing = graphene.List(ListingType)

    def resolve_all_users(self, info, **kwargs):
        return AppUser.objects.all()

    def resolve_all_listing(self, info, **kwargs):
        return Listing.objects.all()

class CreateAppUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        app_package_name = graphene.String(required=True)

    app_user = graphene.Field(UserType)

    def mutate(self, info, username, app_package_name):
        app_user = AppUser(username=username, app_package_name=app_package_name)
        app_user.save()

        return CreateAppUserMutation(app_user=app_user)

class CreateListingMutation(graphene.Mutation):
    class Arguments:
        data = graphene.String(required=True)
        category = graphene.String(required=True)
        status = graphene.String()
        price = graphene.Int(required=True)
        listed_by = graphene.Int(required=True)
        claim = graphene.Boolean(required=True)
    
    listing = graphene.Field(ListingType)

    def mutate(self, info, data, category, status=None, price=None, listed_by=None, claim=None):
        app_user = AppUser.objects.get(pk=listed_by)
        listing = Listing(data=data, category=category, status=status, price=price, listed_by=app_user, claim=claim)
        listing.save()

        return CreateListingMutation(listing=listing)



class Mutation(graphene.ObjectType):
    create_app_user = CreateAppUserMutation.Field()
    create_listing = CreateListingMutation.Field()

schema = graphene.Schema(query=Query , mutation=Mutation)
