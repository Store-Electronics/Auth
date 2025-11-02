from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Product

User = get_user_model()

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ["id", "name", "price", "stock", "brand", "model"]
        read_only_fields = ["price"]

    def get_price(self, obj):
        request = self.context.get("request")
        if (
            request
            and request.user
            and request.user.is_authenticated
            and getattr(request.user, "is_business", False)
        ):
            return obj.price_business
        return obj.price

    def create(self, validated_data):
        price = validated_data.get("price")
        price_business = validated_data.get("price_business")
        if price is None or price <= 0:
            raise serializers.ValidationError("Price must be a positive number")
        if price_business < 0:
            raise serializers.ValidationError("Business price cannot be negative")
        if validated_data.get("stock") < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        price = validated_data.get('price', instance.price)
        price_business = validated_data.get('price_business', instance.price_business)
        stock = validated_data.get('stock', instance.stock)

        if price <= 0:
            raise serializers.ValidationError("Price must be a positive number")
        if price_business < 0:
            raise serializers.ValidationError("Business price cannot be negative")
        if stock < 0:
            raise serializers.ValidationError("Stock cannot be negative")

        instance.name = validated_data.get('name', instance.name)
        instance.price = price
        instance.price_business = price_business
        instance.stock = stock
        instance.brand = validated_data.get('brand', instance.brand)
        instance.model = validated_data.get('model', instance.model)
        instance.save()
        return instance