from django.contrib.auth.models import User


class UserServices:
    @staticmethod
    def create_fake_user() -> User:
        # Generate a random username
        random_username = "".join(random.choices(string.ascii_letters, k=10))

        # Generate a random password
        random_password = "".join(
            random.choices(string.ascii_letters + string.digits, k=10)
        )

        # Create and return the user
        fake_user = User.objects.create_user(
            username=random_username,
            password=random_password,
            is_active=False,  # You might want to set this to False for a fake user
        )

        return fake_user

    @staticmethod
    def create_user(username: str, password: str) -> User:
        # Create and return the user
        user = User.objects.create_user(
            username=username, password=password, is_active=True
        )

        return user
