 Kirana Shop Management System 🛒

A simple bilingual (English + Marathi) Kirana Shop Management System built using Python. Designed for local Indian shopkeepers to handle product inventory, billing, GST, discounts (like Gudi Padwa), and customer management – all in one place.

---

## 🧰 Features

- 🔄 Bilingual Support: English and Marathi
- 🛍️ Add, update, and manage products
- 📦 Track stock levels
- 🧾 Generate bills with GST and festival discounts
- 👤 Add and maintain customer records
- 📊 Save sales and billing data
- 💾 Offline JSON-based data persistence

---

 📂 File Structure

```
kirana_shop/
│
├── kirana_shop.py          # Main Python script
├── kirana_shop_data.json   # Auto-generated data storage file
└── README.md               # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or above installed on your system

### How to Run

```bash
python kirana_shop.py
```

Use the menu to navigate options and press `L` to toggle between Marathi and English.

---

 🧑‍💻 Usage

1. Add products with details like price, stock, GST rate, and expiry date.
2. Register customers with phone, address, and optional credit balance.
3. Generate bills by adding multiple products, auto-calculating GST and applying discounts if applicable.
4. All data is automatically saved to `kirana_shop_data.json`.

---

 🎯 Ideal For

- Local shopkeepers
- Students learning file handling, OOP, and real-world project implementation in Python
- Small business inventory and billing tracking

---

 📌 Future Enhancements

- GUI integration using Tkinter or PyQt
- Exporting bills to PDF
- Analytics dashboard for sales reports
- Multi-user login support

---

 🧾 License

This project is open-source and free to use under the [MIT License](LICENSE).

---

🙏 Acknowledgements

- Marathi translations and cultural support
- Inspired by real needs of Indian Kirana stores
