import graphene
from graphene_django.types import DjangoObjectType
from .models import AppUser, Listing, Transaction
from django.shortcuts import get_object_or_404


class UserType(DjangoObjectType):
    class Meta:
        model = AppUser

class ListingType(DjangoObjectType):
    class Meta:
        model = Listing


class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_listing = graphene.List(ListingType)
    all_transactions = graphene.List(TransactionType)

    def resolve_all_users(self, info, **kwargs):
        return AppUser.objects.all()

    def resolve_all_listing(self, info, **kwargs):
        return Listing.objects.all()

    def resolve_all_transactions(self, info, **kwargs):
        return Transaction.objects.all()
    
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

class CreateNewListing(graphene.Mutation):
    class Arguments:
        price = graphene.Int(required=True)
        pname = graphene.String(required=True)
        data = graphene.String(required=True)
        category = graphene.String(required=True)

    def mutate(self, info, price, pname, data, category):
        user = AppUser(
            username="this11",
            pname=pname
        )
        # user = get_object_or_404(AppUser, id=userid)
        listing = Listing(
            data= data,
            category=category,
            price=price,
            listed_by = user
        )
        listing.save()
        return user

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
    create_listing = CreateListingMutation.Field()
    create_transaction = CreateTransactionMutation.Field()

schema = graphene.Schema(query=Query , mutation=Mutation)
