from rest_framework import serializers
from .models import Category, Route, Tag, Buses, User, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ['id', 'destination', 'category_id']


class TagSeriazlier(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class BusesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    tags = TagSeriazlier(many=True)

    def get_image(self, obj):
        request = self.context['request']
        path = '/static/%s' % obj.image.name

        return request.build_absolute_uri(path)

    class Meta:
        model = Buses
        fields = ['id', 'time', 'price', 'route_name', 'driver_name', 'tags']


class BusesDetailSerializer(BusesSerializer):
    class Meta:
        model = Buses
        fields = BusesSerializer.Meta.fields + ['content']




class AuthBusesDetailSerializer(BusesDetailSerializer):
    like = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    def get_like(self, buses):
        request = self.context.get('request')
        if request:
            return buses.like_set.filter(user=request.user, active=True).exists()

    def get_rating(self, lesson):
        request = self.context.get('request')
        if request:
            r = lesson.rating_set.filter(user=request.user).first()
            if r:
                return r.rate

    class Meta:
        model = Buses
        fields = BusesDetailSerializer.Meta.fields + ['like', 'rating']



class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(source='avatar')

    def get_avatar(self, obj):
        request = self.context['request']
        if obj.avatar and not obj.avatar.name.startswith("/static"):

            path = '/static/%s' % obj.avatar.name

            return request.build_absolute_uri(path)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'username', 'password', 'email',
                  'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'user', 'buses']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        exclude = ['active']

