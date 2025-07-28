import streamlit as st


def login():
    st.title("📱 Refurbished Phone Seller App")
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email and password:
            st.session_state["logged_in"] = True
        else:
            st.warning("Please enter email and password.")


condition_map = {
    "Like New": {"X": "New", "Y": "3 Stars", "Z": "New"},
    "Good": {"X": "Good", "Y": "2 Stars", "Z": "As New"},
    "Fair": {"X": "Scrap", "Y": "1 Star", "Z": "Good"},
}


def calculate_price(cost, platform):
    if platform == "X":
        price = cost / 0.9
    elif platform == "Y":
        price = (cost + 2) / 0.92
    elif platform == "Z":
        price = cost / 0.88
    return round(price, 2)


phones = [
    {"brand": "iPhone", "model": "12", "condition": "Like New", "cost": 300, "stock": 2, "sold_b2b": False},
    {"brand": "Samsung", "model": "S20", "condition": "Fair", "cost": 150, "stock": 0, "sold_b2b": False},
    {"brand": "OnePlus", "model": "8T", "condition": "Good", "cost": 200, "stock": 1, "sold_b2b": True},
    {"brand": "Nokia", "model": "6.1", "condition": "Fair", "cost": 100, "stock": 5, "sold_b2b": False},
    {"brand": "Xiaomi", "model": "Note 9", "condition": "Good", "cost": 180, "stock": 3, "sold_b2b": False},
]


def dashboard():
    st.title("📦 Inventory Dashboard")
    st.write("Showing only phones in stock and not sold B2B.")

    headers = ["Brand", "Model", "Condition", "Stock", "Cost Price"]
    platforms = ["X", "Y", "Z"]

    headers += [f"{p} Price" for p in platforms]
    headers += [f"{p} Condition" for p in platforms]
    headers += [f"{p} Listed?" for p in platforms]

    table = []

    for phone in phones:
        if phone["stock"] <= 0 or phone["sold_b2b"]:
            continue

        row = [phone["brand"], phone["model"], phone["condition"], phone["stock"], f"${phone['cost']}"]
        for p in platforms:
            price = calculate_price(phone["cost"], p)
            row.append(f"${price}")

        for p in platforms:
            mapped_condition = condition_map[phone["condition"]][p]
            row.append(mapped_condition)

        for p in platforms:
            price = calculate_price(phone["cost"], p)
            is_profitable = price > phone["cost"]
            row.append("✅" if is_profitable else "❌")

        table.append(row)

    st.dataframe(table, use_container_width=True, hide_index=True)

if "logged_in" not in st.session_state:
    login()
else:
    dashboard()
