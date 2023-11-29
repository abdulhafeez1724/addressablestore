import graphene
from graphene_django.types import DjangoObjectType
from .models import AppUser, Listing, Transaction
from django.shortcuts import get_object_or_404
import secrets
from .types import NewListingNode

class CatType(graphene.Enum):
    CAR = 'car'
    BUS = 'bus'
    BIKE = 'bike'
    CHARACTER = 'character'
    PARTS = 'parts'
    
class UserType(DjangoObjectType):
    class Meta:
        model = AppUser

class Query(graphene.ObjectType):
    all_listing = graphene.List(NewListingNode, package_name=graphene.String(), user_id=graphene.Int())
    my_listing = graphene.List(NewListingNode, user_id=graphene.Int())
    
    def resolve_all_listing(self, info, package_name, user_id=None):
        if user_id:
            users = AppUser.objects.filter(app_package_name=package_name).exclude(id=user_id).values_list('id', flat=True)
        else:
            users = AppUser.objects.filter(app_package_name=package_name).values_list('id', flat=True)

        listing = Listing.objects.filter(
            listed_by__in=users,
            status='for_sale',
            claim=False
            )
        return listing
    
    def resolve_my_listing(self, info, user_id):
        mylisting = Listing.objects.filter(
            listed_by_id=user_id,
            status='for_sale',
            claim=False
            )
        return mylisting

class CreateNewListing(graphene.Mutation):
    class Arguments:
        price = graphene.Int(required=True)
        data = graphene.String(required=True)
        category = graphene.Argument(CatType, required=True)
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
        category = graphene.Argument(CatType, required=True)
        user_id = graphene.Int(required=True)

    app_user = graphene.Field(UserType)

    def mutate(self, info, price, data, category, user_id):
        app_user = get_object_or_404(AppUser, id=user_id)

        listing = Listing(price=price, data=data, category=category, listed_by=app_user)
        listing.save()

        return CreateListing(app_user=app_user)

class PurchaseNew(graphene.Mutation):
    class Arguments:
        listing_id = graphene.Int(required=True)
        app_package_name = graphene.String(required=True)

    app_user = graphene.Field(UserType)

    def mutate(self, info, app_package_name, listing_id):
        app_user = AppUser(
            username=secrets.token_hex(3)[:6],
            app_package_name=app_package_name
        )
        app_user.save()
        listing = get_object_or_404(Listing, id=listing_id)
        Transaction(buyer=app_user, listing=listing).save()
        listing.status = 'sold_out'
        listing.save()
        
        return PurchaseNew(app_user=listing.listed_by)


class Purchase(graphene.Mutation):
    class Arguments:
        listing_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)

    app_user = graphene.Field(UserType)

    def mutate(self, info, user_id, listing_id):
        app_user = get_object_or_404(AppUser, id=user_id)
        listing = get_object_or_404(Listing, id=listing_id)
        if listing.status != 'for_sale':
            listing.claim = True
            listing.save()
            return Purchase(app_user=app_user)
        transaction = Transaction(buyer=app_user, listing=listing)
        transaction.save()
        listing.status = 'sold_out'
        listing.save()
        
        return Purchase(app_user=transaction.buyer)
    
        
class Mutation(graphene.ObjectType):
    create_new_listing = CreateNewListing.Field()
    create_listing = CreateListing.Field()
    new_purchase = PurchaseNew.Field()
    purchase = Purchase.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)
