from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Cart, CartItem
from books.serializers import CartBookSerializer

class CartItemSerializer(ModelSerializer):
    cart_book_isbn = CartBookSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = (
            "cart_book_isbn",
        )

class CartListSerializer(ModelSerializer):
    cart_total_items = SerializerMethodField();
    cart_total_price = SerializerMethodField();
    cartitem_set = CartItemSerializer(many = True);

    class Meta:
        model = Cart
        fields = (
            "cart_user_email",
            "cart_total_items", 
            "cart_total_price",
            "cartitem_set"
        )

    def get_cart_total_items(self, cart):
        return cart.cart_total_items();

    def get_cart_total_price(self, cart):
        return cart.cart_total_price();