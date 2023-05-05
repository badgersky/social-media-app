from django.core.management.base import BaseCommand, CommandError
from posts.models import Tweet
from users.models import CustomUser


class Command(BaseCommand):
    help = "Creating "

    def add_arguments(self, parser):
        parser.add_argument("user_id", nargs="+", type=int)

    def handle(self, *args, **options):
        for user_id in options["user_id"]:
            try:
                user = CustomUser.objects.get(pk=user_id)
            except CustomUser.DoesNotExist:
                raise CommandError(f'User {user_id} does not exist')

            for num in range(20):
                title = f'title{str(num)}'
                content = f'content{str(num)}, ' * 20
                Tweet.objects.create(title=title, content=content, user=user)

            self.stdout.write(
                self.style.SUCCESS(f'Successfully created posts for user {user_id}')
            )
