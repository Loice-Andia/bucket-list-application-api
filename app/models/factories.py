import factory
from factory.alchemy import SQLAlchemyModelFactory
import bucketlist_models


class UsersFactory(SQLAlchemyModelFactory):
    class Meta:
        model = bucketlist_models.Users


class BucketlistsFactory(SQLAlchemyModelFactory):
    class Meta:
        model = bucketlist_models.Bucketlists


class ItemsFactory(SQLAlchemyModelFactory):
    class Meta:
        model = bucketlist_models.Items

    bucketlist = factory.SubFactory(BucketlistsFactory)
