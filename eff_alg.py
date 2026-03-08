from typing import Dict, List
orders = [
    {"orderId": 1, "product": "Laptop",   "quantity": 2, "status": "pending"},
    {"orderId": 2, "product": "Mouse",    "quantity": 5, "status": "shipped"},
    {"orderId": 3, "product": "Laptop",   "quantity": 3, "status": "delivered"},
    {"orderId": 4, "product": "Keyboard", "quantity": 4, "status": "pending"},
    {"orderId": 5, "product": "Mouse",    "quantity": 1, "status": "pending"},
]


def total_pending_quantity(orders:List[Dict])->int:
    total_pending_quantity =0
    for order in orders:
        try:
            if order['status'] == 'pending':
                total_pending_quantity += order['quantity']
        except KeyError:
            print("Order is missing 'status' or 'quantity' as keys.")
    return total_pending_quantity


def most_ordered_product(orders:List[Dict])->str:
    #here we will use a dictionary to save the total quantity of each product and query in time complexity O(1)
    try:
        orders_count={dic["product"]:0 for dic in orders}
    except KeyError:
        print("One of the orders is missing the 'product' key.")
        return None
    for order in orders:
        try:
            #it doesnt matter if the order is pending or not, we want to count all the orders
            orders_count[order['product']]+=order['quantity']
        except KeyError:
            print("Order is missing 'quantity' as a key.")
    return max(orders_count, key=orders_count.get)



def update_order_status(orders:List[Dict], order_id:int, new_status:str)->List[Dict]:
    """given that we dont have the orders list sorted previously, the best way to find the order_id is to loop through the list and 
    check if the order_id matches, this will give us a time complexity of O(n) in the worst case, 
    but we can not do better than that without sorting the list beforehand and the sorting procces would take time complexity of O(n log n)"""
    #we first check if the new_status is valid, if not we return the original orders list without making any changes
    valid_statuses = {"pending", "shipped", "delivered"}
    if new_status not in valid_statuses:
        print(f"Invalid status: {new_status}. Valid statuses are: {valid_statuses}")
        return orders
    for order in orders:
        try:
            if order['orderId'] == order_id:
                order['status'] = new_status
                return orders
        except KeyError:
            print("Order is missing 'orderId' or 'status' as keys.")




def group_by_status(orders:List[Dict])->Dict[str, List[int]]:
    #We define the posible statuses to avoid adding invalid statuses to the grouped_orders dictionary
    valid_statuses = {"pending", "shipped", "delivered"}
    grouped_orders = {key:[] for key in valid_statuses}
    for order in orders:
        try:
            status= order['status']
            if status not in valid_statuses:
                print(f"Invalid status: {status}. Valid statuses are: {valid_statuses}")
                continue
            else:
                grouped_orders[status].append(order['orderId'])
        except KeyError:
            print("Order is missing 'orderId' or 'status' as keys.")
    return grouped_orders

    


if __name__ == "__main__":
    print(total_pending_quantity(orders))   
    print(most_ordered_product(orders))    
    print(update_order_status(orders, 2, "delivered"))
    print(group_by_status(orders))
