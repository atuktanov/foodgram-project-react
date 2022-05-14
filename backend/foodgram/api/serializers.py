from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from ingredients.models import Ingredient
from recipes.models import IngredientAmount, Recipe
from tags.models import Tag
from users.models import Subscription
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    measurement_unit = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Ingredient
        fields = '__all__'

    def get_name(self, obj):
        return f'{obj.name} ({obj.measurement_unit.name})'


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit.name')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = (
            UniqueTogetherValidator(
                queryset=IngredientAmount.objects.all(),
                fields=['ingredient', 'recipe']),)


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    # tags = serializers.ListField(write_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.ListField(write_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
            'cooking_time')

    # def validate(self, data):
    #     ingredients = data.get('ingredients')
    #     if not ingredients:
    #         raise serializers.ValidationError({
    #             'ingredients': 'Нельзя создать рецепт без ингредиентов'})
    #     ingredient_list = []
    #     for ingredient_item in ingredients:
    #         ingredient = get_object_or_404(
    #             Ingredient, id=ingredient_item['id'])
    #         if ingredient in ingredient_list:
    #             raise serializers.ValidationError(
    #                 'Нельзя дублировать ингредиенты')
    #         ingredient_list.append(ingredient)
    #         if int(ingredient_item['amount']) <= 0:
    #             raise serializers.ValidationError(
    #                 {'ingredients': (
    #                     'Количество ингредиента должно быть больше 0')})
    #     return data

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError({
                'ingredients': 'Нельзя создать рецепт без ингредиентов'})
        ingredient_list = []
        for ingredient_item in value:
            ingredient = get_object_or_404(
                Ingredient, id=ingredient_item['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Нельзя дублировать ингредиенты')
            ingredient_list.append(ingredient)
            if int(ingredient_item['amount']) <= 0:
                raise serializers.ValidationError(
                    {'ingredients': (
                        'Количество ингредиента должно быть больше 0')})
        return value

    def add_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientAmount.objects.create(
                recipe=recipe, ingredient_id=ingredient['id'],
                amount=ingredient['amount'])

    def create(self, validated_data):
        import logging
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        logging.error(tags)
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.add_ingredients(ingredients, recipe)
        return recipe

    # def update(self, instance, validated_data):
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.text = validated_data.get('text', instance.text)
    #     instance.cooking_time = validated_data.get(
    #         'cooking_time', instance.cooking_time)
    #     instance.tags.clear()
    #     tags_data = validated_data.pop('tags')
    #     instance.tags.set(tags_data)
    #     IngredientAmount.objects.filter(recipe=instance).all().delete()
    #     self.add_ingredients(validated_data.get('ingredients'), instance)
    #     instance.save()
    #     return instance

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        super().update(instance, validated_data)
        IngredientAmount.objects.filter(recipe=instance).all().delete()
        self.add_ingredients(ingredients_data, instance)
        # instance.save()
        return instance


class RecipeSerializerGet(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        source='ingredientamount_set', read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(cart__user=user, id=obj.id).exists()


class RecipeSerializerShort(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            subscriber=obj.subscriber, author=obj.author).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeSerializerShort(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
