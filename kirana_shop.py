import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import sys
import re

# Constants
DATA_FILE = "kirana_shop_data.json"
DATE_FORMAT = "%Y-%m-%d"

class Language(Enum):
    ENGLISH = 1
    MARATHI = 2

class MenuOption(Enum):
    ADD_PRODUCT = 1
    VIEW_PRODUCTS = 2
    UPDATE_STOCK = 3
    DELETE_PRODUCT = 4
    NEW_CUSTOMER = 5
    NEW_BILL = 6
    VIEW_SALES = 7
    EXIT = 8

@dataclass
class Product:
    product_id: str
    name: str
    category: str  # Grocery, Patal Bhaji, Spices, etc.
    price: float
    stock: int
    mfg_date: str
    expiry_date: str
    gst_rate: float  # 5%, 12%, 18% (Maharashtra GST)

@dataclass
class Customer:
    customer_id: str
    name: str
    phone: str
    address: str
    credit_balance: float = 0.0  # Common in local Kirana shops
    is_regular: bool = False

@dataclass
class Bill:
    bill_id: str
    customer_id: str
    date: str
    items: List[Dict[str, float]]  # {product_id: quantity}
    total: float
    gst: float
    discount: float = 0.0  # Festival discounts

class KiranaShop:
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.customers: Dict[str, Customer] = {}
        self.bills: Dict[str, Bill] = {}
        self.language: Language = Language.ENGLISH
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as file:
                    data = json.load(file)
                    # Load products
                    for product_id, product_data in data.get('products', {}).items():
                        self.products[product_id] = Product(**product_data)
                    # Load customers
                    for customer_id, customer_data in data.get('customers', {}).items():
                        self.customers[customer_id] = Customer(**customer_data)
                    # Load bills
                    for bill_id, bill_data in data.get('bills', {}).items():
                        self.bills[bill_id] = Bill(**bill_data)
            except Exception as e:
                print(f"Error loading data: {e}")

    def save_data(self):
        data = {
            'products': {p.product_id: asdict(p) for p in self.products.values()},
            'customers': {c.customer_id: asdict(c) for c in self.customers.values()},
            'bills': {b.bill_id: asdict(b) for b in self.bills.values()}
        }
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=2)

    def toggle_language(self):
        self.language = Language.MARATHI if self.language == Language.ENGLISH else Language.ENGLISH
        print("Switched to Marathi!" if self.language == Language.MARATHI else "Switched to English!")

    def add_product(self):
        print("\n" + "="*50)
        print("नवीन उत्पादन जोडा / Add New Product".center(50))
        print("="*50)

        name = input("उत्पादनाचे नाव / Product Name: ")
        category = input("प्रकार / Category (Grocery/Patal Bhaji/Spices): ")
        price = float(input("किंमत / Price (₹): "))
        stock = int(input("स्टॉक / Stock: "))
        mfg_date = input("उत्पादन तारीख (YYYY-MM-DD): ")
        expiry_date = input("समाप्ती तारीख (YYYY-MM-DD): ")
        gst_rate = float(input("GST दर (5/12/18%): "))

        product_id = f"PROD{len(self.products) + 1:04d}"
        new_product = Product(
            product_id=product_id,
            name=name,
            category=category,
            price=price,
            stock=stock,
            mfg_date=mfg_date,
            expiry_date=expiry_date,
            gst_rate=gst_rate
        )
        self.products[product_id] = new_product
        self.save_data()
        print(f"उत्पादन जोडले! ID: {product_id}")

    def new_bill(self):
        print("\n" + "="*50)
        print("नवीन बिल / Generate Bill".center(50))
        print("="*50)

        customer_phone = input("ग्राहक मोबाइल / Customer Phone: ")
        customer = next((c for c in self.customers.values() if c.phone == customer_phone), None)

        if not customer:
            print("नवीन ग्राहक / New Customer!")
            name = input("नाव / Name: ")
            address = input("पत्ता / Address: ")
            customer_id = f"CUST{len(self.customers) + 1:04d}"
            customer = Customer(
                customer_id=customer_id,
                name=name,
                phone=customer_phone,
                address=address
            )
            self.customers[customer_id] = customer

        # Add products to bill
        items = []
        while True:
            print("\nउत्पादन जोडा / Add Product (ID or 'done'): ")
            product_id = input("उत्पादन ID: ")
            if product_id.lower() == 'done':
                break
            if product_id not in self.products:
                print("चुकीचे ID! / Invalid ID!")
                continue
            quantity = float(input("प्रमाण / Quantity: "))
            items.append({"product_id": product_id, "quantity": quantity})

        # Calculate total
        total = sum(
            self.products[item["product_id"]].price * item["quantity"]
            for item in items
        )
        gst = sum(
            (self.products[item["product_id"]].price * item["quantity"]) *
            (self.products[item["product_id"]].gst_rate / 100)
            for item in items
        )

        # Apply Gudi Padwa discount (example)
        today = datetime.now().strftime("%m-%d")
        if today == "03-22":  # Gudi Padwa
            discount = total * 0.1  # 10% off
            print("गुढी पाडवा सवलत! / Gudi Padwa Discount!")
        else:
            discount = 0.0

        bill_id = f"BILL{len(self.bills) + 1:04d}"
        new_bill = Bill(
            bill_id=bill_id,
            customer_id=customer.customer_id,
            date=datetime.now().strftime(DATE_FORMAT),
            items=items,
            total=total + gst - discount,
            gst=gst,
            discount=discount
        )
        self.bills[bill_id] = new_bill
        self.save_data()

        # Print bill
        print("\n" + "="*50)
        print("बिल / BILL".center(50))
        print("="*50)
        print(f"बिल क्रमांक / Bill ID: {bill_id}")
        print(f"ग्राहक / Customer: {customer.name}")
        for item in items:
            product = self.products[item["product_id"]]
            print(f"{product.name} x{item['quantity']} = ₹{product.price * item['quantity']}")
        print("-"*50)
        print(f"एकूण / Total: ₹{total}")
        print(f"GST: ₹{gst}")
        print(f"सवलत / Discount: ₹{discount}")
        print(f"पेयोग / Payable: ₹{new_bill.total}")
        print("="*50)

    def display_menu(self):
        menu_items = {
            MenuOption.ADD_PRODUCT: ("नवीन उत्पादन जोडा", "Add Product"),
            MenuOption.VIEW_PRODUCTS: ("उत्पादन पहा", "View Products"),
            MenuOption.UPDATE_STOCK: ("स्टॉक अपडेट", "Update Stock"),
            MenuOption.NEW_CUSTOMER: ("नवीन ग्राहक", "New Customer"),
            MenuOption.NEW_BILL: ("नवीन बिल", "Generate Bill"),
            MenuOption.VIEW_SALES: ("विक्री तपशील", "View Sales"),
            MenuOption.EXIT: ("बाहेर पडा", "Exit")
        }

        print("\n" + "="*50)
        print("किराणा दुकान व्यवस्थापन / Kirana Shop Management".center(50))
        print("="*50)
        for option, (marathi, english) in menu_items.items():
            print(f"{option.value}. {marathi if self.language == Language.MARATHI else english}")
        print("="*50)
        print("Press 'L' to toggle Marathi/English")

    def run(self):
        while True:
            self.display_menu()
            choice = input("निवडा / Enter Choice: ")

            if choice.lower() == 'l':
                self.toggle_language()
                continue

            try:
                choice = int(choice)
                menu_option = MenuOption(choice)

                if menu_option == MenuOption.ADD_PRODUCT:
                    self.add_product()
                elif menu_option == MenuOption.NEW_BILL:
                    self.new_bill()
                elif menu_option == MenuOption.EXIT:
                    print("बाहेर पडत आहे... / Exiting...")
                    break
                else:
                    print("Coming soon!")
                    self._press_enter_to_continue()

            except ValueError:
                print("चुकीची निवड! / Invalid choice!")

    def _press_enter_to_continue(self):
        input("\nEnter दाबा / Press Enter...")

if __name__ == "__main__":
    shop = KiranaShop()
    try:
        shop.run()
    except KeyboardInterrupt:
        print("\nClosing...")
        shop.save_data()
        sys.exit(0)