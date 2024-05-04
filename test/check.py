# def generate_receipt(business_name, date, transactions, total, payment_method, amount_paid, line_width=32):
#     """
#     Generates a formatted receipt with configurable line width.
#
#     Parameters:
#     - business_name (str): The name of the business or individual.
#     - date (str): The date of the transaction.
#     - transactions (list of tuples): A list of transactions where each tuple contains (quantity, description, unit price, total price).
#     - total (float): Total amount for the receipt.
#     - payment_method (str): Payment method used.
#     - amount_paid (float): Amount paid by the customer.
#     - line_width (int): The width of each line in characters.
#
#     Returns:
#     - str: A formatted receipt.
#     """
#     # Function to center text within a given width
#     def center_text(text, width):
#         return text.center(width)
#
#     # Function to align text to the right
#     def right_align(text, width):
#         return text.rjust(width)
#
#     # Function to format a line item
#     def format_line_item(qty, desc, unit_price, total_price, width):
#         first_line = f"{qty:.2f} x {unit_price:,.2f}".ljust(width // 2) + f"{total_price:,.2f}".rjust(width // 2)
#         second_line = desc[:width]  # Truncate description if it's too long
#         return first_line, second_line
#
#     # Initialize receipt with business header
#     receipt = center_text(business_name, line_width) + "\n"
#     receipt += "=" * line_width + "\n"
#
#     # Add transactions
#     for qty, desc, unit_price, total_price in transactions:
#         item_line, desc_line = format_line_item(qty, desc, unit_price, total_price, line_width)
#         receipt += item_line + "\n"
#         receipt += desc_line + "\n"
#         receipt += "-" * line_width + "\n"
#
#     # Add totals and payment details
#     receipt += "=" * line_width + "\n"
#     receipt += "СУМА"
#     receipt += right_align(f"СУМА              {total:,.2f}", line_width) + "\n"
#     receipt += right_align(f"{payment_method}              {amount_paid:,.2f}", line_width) + "\n"
#     receipt += right_align(f"Решта                  {amount_paid - total:,.2f}", line_width) + "\n"
#     receipt += "=" * line_width + "\n"
#
#     # Add footer with date and thanks message
#     receipt += center_text(date, line_width) + "\n"
#     receipt += center_text("Дякуємо за покупку!", line_width) + "\n"
#
#     return receipt
def generate_receipt(business_name, date, transactions, total, payment_method, amount_paid, line_width=50):
    """
    Generates a formatted receipt with enhanced formatting.

    Parameters:
    - business_name (str): The name of the business or individual.
    - date (str): The date of the transaction.
    - transactions (list of tuples): A list of transactions where each tuple contains (quantity, description, unit price, total price).
    - total (float): Total amount for the receipt.
    - payment_method (str): Payment method used.
    - amount_paid (float): Amount paid by the customer.
    - line_width (int): The width of each line in characters.

    Returns:
    - str: A formatted receipt.
    """

    def format_money(amount):
        return f"{amount:,.2f}"

    # Header
    receipt = business_name.center(line_width) + "\n"
    receipt += "=" * line_width + "\n"

    # Body
    for qty, description, unit_price, total_price in transactions:
        item_line = f"{qty:.2f} x {format_money(unit_price)}".ljust(line_width - 20)
        item_line += format_money(total_price).rjust(20)
        receipt += item_line + "\n"
        receipt += description + "\n"
        receipt += "-" * line_width + "\n"

    # Footer
    receipt += "=" * line_width + "\n"
    receipt += f"{'СУМА'.rjust(line_width - 20)}{format_money(total).rjust(20)}\n"
    receipt += f"{payment_method.rjust(line_width - 20)}{format_money(amount_paid).rjust(20)}\n"
    receipt += f"{'Решта'.rjust(line_width - 20)}{format_money(amount_paid - total).rjust(20)}\n"
    receipt += "=" * line_width + "\n"
    receipt += date.center(line_width) + "\n"
    receipt += "Дякуємо за покупку!".center(line_width) + "\n"

    return receipt


if __name__ == "__main__":
    transactions = [
        (3.00, "Mavic 3T", 298870.00, 896610.00),
        (20.00, "Дрон FPV з акумулятором 6S чорний", 31000.00, 620000.00),
    ]
    print(
        generate_receipt(
            "ФОП Джонсонюк Борис", "14.08.2023 14:42", transactions, 1516610.00, "Картка", 1516610.00, line_width=50
        )
    )
