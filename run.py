from app import app, db
from app.auth.login import Index, Login
from app.auth.register import Register
from app.bucketlist.bucketlists import Bucketlist, SearchBucketlist
from app.bucketlist.bucketlists import OneBucketlist
from app.items.bucketlist_items import BucketListItems, SearchBucketlistItems
from app.items.bucketlist_items import OneBucketListItem
from app.models.bucketlist_models import Bucketlists, Items, Users
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api

manager = Manager(app)
migrate = Migrate(app, db)
api = Api(app, prefix="/api/v1")

api.add_resource(Index,
                 '/',
                 endpoint='home')
api.add_resource(Login,
                 '/auth/login/',
                 endpoint='login')
api.add_resource(Register,
                 '/auth/register/',
                 endpoint='register')
api.add_resource(Bucketlist,
                 '/bucketlists/',
                 endpoint='bucketlists')
api.add_resource(OneBucketlist,
                 '/bucketlists/<bucketlist_id>/',
                 endpoint='one_bucketlist')
api.add_resource(SearchBucketlist,
                 '/bucketlists?q=<query>',
                 endpoint='search_bucketlists')
api.add_resource(BucketListItems,
                 '/bucketlists/<bucketlist_id>/items/',
                 endpoint='items')
api.add_resource(OneBucketListItem,
                 '/bucketlists/<bucketlist_id>/items/<item_id>',
                 endpoint='one_item')
api.add_resource(SearchBucketlistItems,
                 '/bucketlists/<bucketlist_id>/items?q=<query>',
                 endpoint='search_items')


def make_shell_context():
    '''Returns application and database instances
    to the shell importing them automatically
    on `python manager.py shell`.
    '''
    return dict(app=app, api=api, db=db, Users=Users,
                Bucketlists=Bucketlists, Items=Items)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
