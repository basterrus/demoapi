from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Party, Playlist, Track


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    return_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password', 'return_password']

    def save(self, *args, **kwargs):
        user = User(
            username=self.validated_data['username'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['return_password']
        if password != password2:
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        user.set_password(password)
        user.save()
        return user


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username", write_only=True)
    password = serializers.CharField(label="Password", style={'input_type': 'password'}, trim_whitespace=False,
                                     write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                raise serializers.ValidationError('Невозможно войти с предоставленными учетными данными.', code='authorization')
        else:
            raise serializers.ValidationError('Должен включать «имя пользователя» и «пароль».', code='authorization')

        attrs['user'] = user
        return attrs


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'
