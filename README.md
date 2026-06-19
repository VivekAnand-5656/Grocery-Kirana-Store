🛒 Grocery Store Backend API

A full-featured Grocery Store Backend built with FastAPI and MongoDB. This project supports customer and seller management, product management, cart, wishlist, orders, authentication, and payment integration.

🚀 Features

Authentication

* User Registration
* User Login
* JWT Authentication
* Role-Based Access Control (Customer & Seller)

Seller Features

* Update Profile
* Add Product
* Update Product
* Delete Product
* View Own Products
* Manage Orders
* Total Earnings
* Total Orders
* My Profile

Customer Features

* Update Profile
* My Profile
* View Products
* Search Products
* Add to Cart
* Remove from Cart
* Add to Wishlist
* Remove from Wishlist
* Buy Products
* Place Order
* Filter Product
* View Order History

Order Management

* Create Orders
* Update Order Status
* Order Tracking
* Seller Order Dashboard

Additional Features

* MongoDB Aggregation 
* Secure Password Hashing
* API Documentation with Swagger

---

🛠 Tech Stack

* FastAPI
* MongoDB
* Motor (Async MongoDB Driver)
* JWT Authentication
* Pydantic 
* Python

---

📂 Project Structure

```bash
Backend/
│
├── src/
│   ├── Auth/    
│   ├── Config/
│   ├── Public/
│   ├── Customer/
│   ├── Dependencies/
│   ├── Enums/
│   ├── Seller/  
│
├── main.py
├── requirements.txt
└── README.md
```

------ Installation ------

------- Create Virtual Environment

```bash
python -m venv venv
```

------- Activate Environment

```bash
venv\Scripts\activate
```

------ Install Dependencies

```bash
pip install -r requirements.txt
```
------- Run Server

```bash
uvicorn main:app --reload
```

Server will start at:

```bash
http://127.0.0.1:8000
```

---
------- API Documentation

Swagger UI:

```bash
http://127.0.0.1:8000/docs
```

Redoc:

```bash
http://127.0.0.1:8000/redoc
```

---

-------- Environment Variables

Create a `.env` file:

```env
MONGO_URI=
SECRET_KEY=
ALGORITHM=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

---

------- Screenshots

Add screenshots of:

* Swagger Documentation
* Product APIs
* Cart APIs
* Order APIs
* Wishlist APIs

---

------- Future Improvements

* Razorpay Integration
* Coupon System
* Product Reviews
* Email Notifications
* Admin Dashboard

---

 --------- Author

Live Demo API URL :- https://grocery-kirana-store.onrender.com

Vivek Anand

Backend Developer | FastAPI | MongoDB | JavaScript
