import graphene
from graphene_django.types import DjangoObjectType
from .models import AppUser, Listing, Transaction
from django.shortcuts import get_object_or_404
import secrets

class UserType(DjangoObjectType):
    class Meta:
        model = AppUser

class NewListingType(DjangoObjectType):
    class Meta:
        model = Listing

class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_new_listing = graphene.List(NewListingType)
    all_transactions = graphene.List(TransactionType)

    def resolve_all_users(self, info, **kwargs):
        return AppUser.objects.all()

    def resolve_all_listing(self, info, **kwargs):
        return Listing.objects.all()
    
    def resolve_all_new_listing(self, info, **kwargs):
        return Listing.objects.all()

    def resolve_all_transactions(self, info, **kwargs):
        return Transaction.objects.all()
    
class CreateAppUserMutation(graphene.Mutation):
    class Arguments:
        app_package_name = graphene.String(required=True)

    app_user = graphene.Field(UserType)

    def mutate(self, info, app_package_name):
        username = secrets.token_hex(3)[:6]

        app_user = AppUser(username=username, app_package_name=app_package_name)
        app_user.save()
        return CreateAppUserMutation(app_user=app_user)


class CreateNewListing(graphene.Mutation):
    class Arguments:
        price = graphene.Int(required=True)
        data = graphene.String(required=True)
        category = graphene.String(required=True)
        app_user_id = graphene.Int(required=True)

    listing = graphene.Field(NewListingType)

    def mutate(self, info, price, data, category, app_user_id):
        app_user = AppUser.objects.get(id=app_user_id)

        listing = Listing(price=price, data=data, category=category, app_user=app_user)
        listing.save()

        return CreateNewListing(listing=listing)
    
class CreateTransactionMutation(graphene.Mutation):
    class Arguments:
        seller_id = graphene.Int(required=True)
        buyer_id = graphene.Int(required=True)
        listing_id = graphene.Int(required=True)

    transaction = graphene.Field(TransactionType)

    def mutate(self, info, seller_id, buyer_id, listing_id):
        seller = AppUser.objects.get(pk=seller_id)
        buyer = AppUser.objects.get(pk=buyer_id)
        listing = Listing.objects.get(pk=listing_id)

        transaction = Transaction(seller=seller, buyer=buyer, listing=listing)
        transaction.save()

        return CreateTransactionMutation(transaction=transaction)

class Mutation(graphene.ObjectType):
    create_app_user = CreateAppUserMutation.Field()
    create_new_listing = CreateNewListing.Field()
    create_transaction = CreateTransactionMutation.Field()

schema = graphene.Schema(query=Query , mutation=Mutation)
