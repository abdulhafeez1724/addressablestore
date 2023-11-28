import graphene
from graphene_django.types import DjangoObjectType
from .models import AppUser, Listing, Transaction

class ListingType(DjangoObjectType):
    class Meta:
        model= Listing

class NewListingNode(DjangoObjectType):
    #retrieving listings by user_id
    mylisting = graphene.List("store.types.NewListingNode", user_id=graphene.Int())
    #retrieving listings by package_name
    listing = graphene.List("store.types.NewListingNode", package_name=graphene.String())
    class Meta:
        model = Listing
    
    def resolve_mylisting(self, info, user_id=None):
        # print(users)
        mylisting = None
        if user_id:
            #get listings for the specified user_id with conditions
            mylisting = Listing.objects.filter(
                listed_by_id=user_id,
                status='for_sale',
                claim=False
                )
        #obtained listings
        return mylisting
    
    def resolve_listing(self, info, package_name=None):
        listing = None
        if package_name:
            #AppUser model to get user IDs for the specified package_name
            users = AppUser.objects.filter(app_package_name=package_name).values_list('id', flat=True)

            listing = Listing.objects.filter(
                listed_by__in=users,
                status='for_sale',
                claim=False
                )
        return listing

   