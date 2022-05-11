from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from ingredients.models import Ingredient
from tags.models import Tag


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
