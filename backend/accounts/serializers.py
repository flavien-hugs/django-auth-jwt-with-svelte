# accounts.serializers.py

from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from accounts.models.users import User


class UserRegistrationSerializer(
    serializers.ModelSerializer[User]
):
    """
    Serializers registration requests and creates a new user
    """

    password = serializers.CharField(
        max_length=120, min_lenth=9,
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'full_name',
            'phone', 'password'
        ]


    def create(self, validated_data):
        """
        Return user after creation.
        """

        user = User.objects.create_user(
            full_name=validated_data['full_name'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )
        user.bio = validated_data.get('bio', '')
        user.save(update_fields=['bio',])
        return user


class UserLoginSerializer(serializers.ModelSerializer[User]):
    phone = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        """
        Get user token
        """

        user = User.objects.get(phone=obj.phone)
        return {
            'refresh': user.tokens['refresh'],
            'access': user.tokens['access']
        }

    class Meta:
        model = User
        fields = ['phone', 'password', 'tokens', 'is_staff']

    def validate(self, data):

        """
        Validate and return user login.
        """

        phone = data.get('phone', None)
        password = data.get('password', None)

        if phone is None:
            raise serializers.ValidationError(
                'An phone number is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user is not currently activated.'
            )

        return user


class UserSerializer(serializers.ModelSerializer[User]):
    """
    Handle serialization and deserialization of User objects.
    """

    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True
    )

    class Meta:
        model = User
        fields = (
            'email',
            'phone',
            'password',
            'tokens',
            'bio',
            'full_name',
            'birth_date',
            'is_staff',
        )
        read_only_fields = ('tokens', 'is_staff')

    def update(self, instance, validated_data):
        """
        Perform an update on a User.
        """

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class LogoutSerializer(serializers.Serializer[User]):

    refresh = serializers.CharField()

    def validate(self, attrs):
        """
        Validate token.
        """
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        """
        Validate save backlisted token.
        """

        try:
            RefreshToken(self.token).blacklist()

        except TokenError as ex:
            raise exceptions.AuthenticationFailed(ex)
