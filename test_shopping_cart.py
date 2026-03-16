import pytest
from pytest import approx
from shopping_cart import ShoppingCart
import shopping_cart
#Before we work with fixtures we will create a local instance of the shopping cart to use in our tests even though is not the best practice
shopping_cart_instance = ShoppingCart()
def test_basic_assertions():
    #First we need to check if the item appear in the cart after we add it
    shopping_cart_instance.add_item(name="Apple", price=2.3, quantity=3)
    assert shopping_cart_instance.items == {"Apple": {"price": 2.3, "quantity": 3}}
    #Check if the get total is correct
    assert shopping_cart_instance.get_total() == approx(6.9, rel=1e-1)
    #Chek if the item count is correct
    assert shopping_cart_instance.item_count() == 3
def test_edge_cases():
    #Check if adding the same item twice increases the quantity, not duplicates
    shopping_cart_instance.add_item(name="Apple", price=2.3, quantity=2)
    assert shopping_cart_instance.items == {"Apple": {"price": 2.3, "quantity": 5}}
    #get_total() on an empty cart returns 0
    empty_cart = ShoppingCart()
    assert empty_cart.get_total() == 0
    #Check if apply_discount(0) returns the full total
    assert shopping_cart_instance.apply_discount(0) == shopping_cart_instance.get_total()
    #Check if apply_discount(100) returns 0
    assert shopping_cart_instance.apply_discount(100) == 0
def test_error_handling():
    #Check if adding an item with a negative price raises ValueError
    with pytest.raises(ValueError):
            shopping_cart_instance.add_item(name="Banana", price=-1.0, quantity=1)
    #Check if removing an item that doesn't exist raises KeyError
    with pytest.raises(KeyError):
        shopping_cart_instance.remove_item(name='Orange')
    #Check if applying a discount outside 0–100 raises ValueError
    with pytest.raises(ValueError):
        shopping_cart_instance.apply_discount(-10)
    with pytest.raises(ValueError):
        shopping_cart_instance.apply_discount(104)  
@pytest.fixture
def get_shopping_cart():
    #We will create a pre-loades shopping cart with 2 items to use in our tests
    cart = ShoppingCart()
    cart.add_item(name="Milk", price=1.5, quantity=1)
    cart.add_item(name="Bread", price=2.0, quantity=1)
    return cart

#Now we will have parameterized test to check apply discount with several discount values
@pytest.mark.parametrize("discount, expected_total", [
    (80,0.7),
    (20,2.8),
    (100,0),
    (0,3.5),
    (10,3.15),
    (50,1.75),
    (30,2.45)
 ])
def test_apply_discount(get_shopping_cart, discount, expected_total):
    discounted_total =get_shopping_cart.apply_discount(discount)
    assert discounted_total == approx(expected_total,rel=1e-1)
    