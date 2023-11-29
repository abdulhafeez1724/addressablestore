from graphene_django.types import DjangoObjectType
from .models import Listing


class NewListingNode(DjangoObjectType):
    class Meta:
        model = Listing
