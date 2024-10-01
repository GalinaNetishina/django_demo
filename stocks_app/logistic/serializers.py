from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ["prod", "quantity", "price"]

    prod = serializers.CharField(source="product.title", read_only=True)


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ["address", "positions"]

    def create(self, validated_data):
        positions = validated_data.pop("positions")

        stock = super().create(validated_data)

        for prod in positions:
            StockProduct.objects.create(stock=stock, **prod)

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop("positions")

        stock = super().update(instance, validated_data)

        for prod in positions:
            StockProduct.objects.update_or_create(
                stock=stock, product=prod["product"], defaults={"stock": stock, **prod}
            )
        return stock
