 📈 Stocker

### Cloud-Based Stock Trading Platform using Flask and AWS

Stocker is a **cloud-native stock trading platform** designed for modern digital finance. It enables users to perform **real-time stock transactions, track their investment portfolios, and analyze market performance** through an intuitive web interface.

The platform is built using **Flask (Python)** for backend development and deployed on **AWS EC2** for scalable cloud hosting. Data is stored in **Amazon DynamoDB**, providing fast and reliable access to user information, transactions, and stock holdings.

By integrating cloud services with a responsive frontend, Stocker delivers a **secure, scalable, and efficient trading environment**.

---

# 🚀 Features

### 🔐 Secure User Authentication

* Encrypted password storage
* Secure session management
* Role-based access (Admin / Trader)
* Protection of sensitive financial data

### ⚡ Real-Time Trade Execution

* Buy and sell stocks instantly
* Optimized backend for low-latency processing
* Cloud infrastructure ensures quick response times

### 📊 Portfolio Tracking

* Monitor holdings in a visual dashboard
* Track profit and loss
* Analyze investment performance in real time

### 📜 Transaction History

* View complete trade history
* Monitor stock purchases and sales
* Maintain transparent investment records

### ☁️ Cloud-Native Architecture

* Hosted on **AWS EC2**
* Data stored in **Amazon DynamoDB**
* Scalable and highly available infrastructure

---

# 🏗️ System Architecture

```
User Browser
      │
      ▼
Flask Web Application
      │
      ▼
AWS EC2 Instance
      │
      ▼
Amazon DynamoDB Database
      │
      ▼
Amazon SNS Notifications
      │
      ▼
AWS CloudWatch Monitoring
```

---

# 🛠️ Tech Stack

### Backend

* Python
* Flask
* boto3 (AWS SDK)

### Frontend

* HTML
* CSS
* Bootstrap
* JavaScript

### Cloud Services

* AWS EC2
* AWS DynamoDB
* AWS IAM
* AWS SNS
* AWS CloudWatch

---

# 📂 Project Structure

```
stocker-main
│
├── app.py
├── setup_dynamodb.py
├── requirements.txt
│
├── static
│   ├── css
│   ├── js
│   └── img
│
├── templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard_admin.html
│   ├── dashboard_trader.html
│   ├── buy_stock.html
│   ├── sell_stock.html
│   └── service-details-*.html
```

---

# ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/akshay002-ln/Stocker-A-Cloud-based-stock-trading-application-using-Flask-and-AWS.git
cd Stocker-A-Cloud-based-stock-trading-application-using-Flask-and-AWS
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure AWS Credentials

Set environment variables:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
```

---

### 5️⃣ Create DynamoDB Tables

Run:

```bash
python setup_dynamodb.py
```

This will create the required tables:

* stocker_users
* stocker_stocks
* stocker_transactions
* stocker_portfolio

---

### 6️⃣ Run the application

```bash
python app.py
```

Open browser:

```
http://localhost:5000
```

---

# ☁️ AWS Deployment

### 1️⃣ Launch EC2 Instance

* Ubuntu Server
* t2.micro instance

### 2️⃣ Install dependencies

```bash
sudo apt update
sudo apt install python3-pip python3-venv git
```

### 3️⃣ Clone project on EC2

```bash
git clone <repo-url>
```

### 4️⃣ Run Flask

```bash
python app.py
```

Access application using:

```
http://EC2_PUBLIC_IP:5000
```

---

# 📊 DynamoDB Tables

| Table                | Description              |
| -------------------- | ------------------------ |
| stocker_users        | Stores user accounts     |
| stocker_stocks       | Stores stock market data |
| stocker_transactions | Stores trade history     |
| stocker_portfolio    | Stores user holdings     |

---

# 🔔 AWS SNS Notifications

SNS topics are used to send **email alerts** for important trading events.

Examples:

* Stock purchase confirmation
* Trade execution alerts
* Portfolio updates

---

# 📈 Monitoring

AWS **CloudWatch** is used for:

* Application monitoring
* Server performance tracking
* Error logging
* System metrics

---

# 🎯 Learning Outcomes

This project demonstrates:

* Cloud-native application development
* AWS cloud deployment
* Secure authentication systems
* Real-time data processing
* Portfolio analytics dashboard
* Integration of multiple AWS services

---

# 👨‍💻 Team Members

| Name                            | Role      |
| ------------------------------- | --------- |
| Chilumuru Naga Sai Vijay Kumar  | Team Lead |
| Akshay Chatla                   | Member    |
| Naga Praneetha Kanna            | Member    |
| Venkata Snehanjali Cheemakurthi | Member    |

---

# 📜 License

This project is developed for **educational and cloud computing training purposes**.
