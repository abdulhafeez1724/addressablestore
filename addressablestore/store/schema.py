import graphene
from graphene_django.types import DjangoObjectType
from .models import AppUser, Listing
from django.shortcuts import get_object_or_404
import secrets
from .types import NewListingNode

class UserType(DjangoObjectType):
    class Meta:
        model = AppUser

class Query(graphene.ObjectType):
    all_listing = graphene.List(NewListingNode, package_name=graphene.String(), user_id=graphene.Int())
    
    def resolve_all_listing(self, info, package_name=None, user_id=None):
        if package_name:
            users = AppUser.objects.filter(app_package_name=package_name).values_list('id', flat=True)
        elif user_id:
            p_name = AppUser.objects.filter(id=user_id).values_list('app_package_name', flat=True)

            users = AppUser.objects.filter(app_package_name__in=p_name).values_list('id', flat=True)
        else:
            return "Package Name or User ID is reqired"

        listing = Listing.objects.filter(
            listed_by__in=users,
            status='for_sale',
            claim=False
            )
        return listing
        # return NewListingNode(listing=listing)
        # return listing  

    # def resolve_all_transactions(self, info, **kwargs):
    #     return Transaction.objects.all()


class CreateNewListing(graphene.Mutation):
    class Arguments:
        price = graphene.Int(required=True)
        data = graphene.String(required=True)
        category = graphene.String(required=True)
        app_package_name = graphene.String(required=True)

    app_user = graphene.Field(UserType)

    def mutate(self, info, price, data, category, app_package_name):
        app_user = AppUser(
            username=secrets.token_hex(3)[:6],
            app_package_name=app_package_name
        )
        app_user.save()

        listing = Listing(price=price, data=data, category=category, listed_by=app_user)
        listing.save()

        return CreateNewListing(app_user=app_user)
    
class CreateListing(graphene.Mutation):
    class Arguments:
        price = graphene.Int(required=True)
        data = graphene.String(required=True)
        category = graphene.String(required=True)
        user_id = graphene.Int(required=True)

    app_user = graphene.Field(UserType)

    def mutate(self, info, price, data, category, user_id):
        app_user = get_object_or_404(AppUser, id=user_id)

        listing = Listing(price=price, data=data, category=category, listed_by=app_user)
        listing.save()

        return CreateListing(app_user=app_user)

class Mutation(graphene.ObjectType):
    create_new_listing = CreateNewListing.Field()
    create_listing = CreateListing.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
