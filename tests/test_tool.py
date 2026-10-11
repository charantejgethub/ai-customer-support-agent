from tools.order_tools import get_order_status

result = get_order_status(1001)

print(result)

from tools.product_tools import get_product_info
from tools.customer_tools import get_customer_orders
from tools.ticket_tools import create_support_ticket


print("\nPRODUCT INFORMATION")
print(get_product_info("Samsung"))


print("\nCUSTOMER ORDERS")
print(get_customer_orders(1))


print("\nCREATE SUPPORT TICKET")
print(
    create_support_ticket(
        1,
        "My product arrived damaged"
    )
)