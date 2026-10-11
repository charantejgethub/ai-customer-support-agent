from tools.order_tools import get_my_order_status

print("Rahul accessing his own order:")
print(get_my_order_status(1001, 1))

print("\nRahul trying to access Priya's order:")
print(get_my_order_status(1002, 1))