from flask import Flask, render_template, request, redirect, url_for, flash, session
import boto3
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import json

app = Flask(__name__)
app.secret_key = "stocker_secret_2024"

# ================= AWS CONFIGURATION =================

AWS_REGION = "ap-south-1"

session_aws = boto3.Session(region_name=AWS_REGION)

dynamodb = session_aws.resource('dynamodb')
sns = session_aws.client('sns')

# ================= TABLES =================

USER_TABLE = "stocker_users"
STOCK_TABLE = "stocker_stocks"
TRANSACTION_TABLE = "stocker_transactions"
PORTFOLIO_TABLE = "stocker_portfolio"

USER_ACCOUNT_TOPIC_ARN = "arn:aws:sns:us-east-1:604665149129:StockerUserAccountTopic"
TRANSACTION_TOPIC_ARN = "arn:aws:sns:us-east-1:604665149129:StockerTransactionTopic"

# ================= HELPERS =================

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)

# ================= SNS =================

def send_notification(topic_arn, subject, message):
    try:
        sns.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )
    except Exception as e:
        print("SNS Error:", e)

# ================= DATABASE FUNCTIONS =================

def get_user_by_email(email):

    table = dynamodb.Table(USER_TABLE)

    response = table.get_item(Key={'email': email})

    return response.get("Item")


def create_user(username, email, password, role):

    table = dynamodb.Table(USER_TABLE)

    user = {
        "id": str(uuid.uuid4()),
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }

    table.put_item(Item=user)

    return user


def get_all_stocks():

    table = dynamodb.Table(STOCK_TABLE)

    response = table.scan()

    return response.get("Items", [])


def get_stock_by_id(stock_id):

    table = dynamodb.Table(STOCK_TABLE)

    response = table.get_item(Key={'id': stock_id})

    return response.get("Item")


def get_traders():

    table = dynamodb.Table(USER_TABLE)

    response = table.scan(
        FilterExpression=Attr('role').eq("trader")
    )

    return response.get("Items", [])


def get_user_by_id(user_id):

    table = dynamodb.Table(USER_TABLE)

    response = table.scan(
        FilterExpression=Attr('id').eq(user_id)
    )

    users = response.get("Items", [])

    return users[0] if users else None


def get_transactions():

    table = dynamodb.Table(TRANSACTION_TABLE)

    transactions = table.scan().get("Items", [])

    for t in transactions:

        t["user"] = get_user_by_id(t["user_id"])
        t["stock"] = get_stock_by_id(t["stock_id"])

    return transactions


def get_user_transactions(user_id):

    table = dynamodb.Table(TRANSACTION_TABLE)

    response = table.scan(
        FilterExpression=Attr('user_id').eq(user_id)
    )

    transactions = response.get("Items", [])

    for t in transactions:
        t["stock"] = get_stock_by_id(t["stock_id"])

    return transactions


def get_portfolios():

    table = dynamodb.Table(PORTFOLIO_TABLE)

    portfolios = table.scan().get("Items", [])

    for p in portfolios:

        p["user"] = get_user_by_id(p["user_id"])
        p["stock"] = get_stock_by_id(p["stock_id"])

    return portfolios


def get_user_portfolio(user_id):

    table = dynamodb.Table(PORTFOLIO_TABLE)

    response = table.query(
        KeyConditionExpression=Key("user_id").eq(user_id)
    )

    portfolio = response.get("Items", [])

    for p in portfolio:

        p["stock"] = get_stock_by_id(p["stock_id"])

    return portfolio


def get_portfolio_item(user_id, stock_id):

    table = dynamodb.Table(PORTFOLIO_TABLE)

    response = table.get_item(
        Key={
            "user_id": user_id,
            "stock_id": stock_id
        }
    )

    return response.get("Item")


def create_transaction(user_id, stock_id, action, quantity, price):

    table = dynamodb.Table(TRANSACTION_TABLE)

    transaction = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "stock_id": stock_id,
        "action": action,
        "quantity": quantity,
        "price": Decimal(str(price)),
        "status": "completed",
        "transaction_date": datetime.now().isoformat()
    }

    table.put_item(Item=transaction)

    return transaction


def update_portfolio(user_id, stock_id, quantity, average_price):

    table = dynamodb.Table(PORTFOLIO_TABLE)

    quantity = Decimal(str(quantity))
    average_price = Decimal(str(average_price))

    existing = get_portfolio_item(user_id, stock_id)

    if existing and quantity > 0:

        table.update_item(
            Key={"user_id": user_id, "stock_id": stock_id},
            UpdateExpression="set quantity=:q, average_price=:p",
            ExpressionAttributeValues={
                ":q": quantity,
                ":p": average_price
            }
        )

    elif existing and quantity <= 0:

        table.delete_item(
            Key={"user_id": user_id, "stock_id": stock_id}
        )

    elif quantity > 0:

        table.put_item(
            Item={
                "user_id": user_id,
                "stock_id": stock_id,
                "quantity": quantity,
                "average_price": average_price
            }
        )

# ================= LOGIN HELPER =================

def login_required(role=None):

    def wrapper(func):

        from functools import wraps

        @wraps(func)
        def decorated(*args, **kwargs):

            if "email" not in session:
                return redirect(url_for("login"))

            if role and session.get("role") != role:
                flash("Unauthorized access")
                return redirect(url_for("login"))

            return func(*args, **kwargs)

        return decorated

    return wrapper


# ================= ROUTES =================

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        user = get_user_by_email(email)

        if user and user["password"] == password and user["role"] == role:

            session["email"] = user["email"]
            session["role"] = user["role"]
            session["user_id"] = user["id"]

            send_notification(
                USER_ACCOUNT_TOPIC_ARN,
                "User Login",
                f"{user['username']} logged in"
            )

            if role == "admin":
                return redirect(url_for("dashboard_admin"))
            else:
                return redirect(url_for("dashboard_trader"))

        flash("Invalid credentials")

    return render_template("login.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        if get_user_by_email(email):
            flash("User already exists")
            return redirect(url_for("login"))

        create_user(username, email, password, role)

        send_notification(
            USER_ACCOUNT_TOPIC_ARN,
            "New User Signup",
            f"{username} created an account"
        )

        return redirect(url_for("login"))

    return render_template("signup.html")


# ================= DASHBOARDS =================

@app.route('/dashboard_admin')
@login_required("admin")
def dashboard_admin():

    traders = get_traders()
    transactions = get_transactions()
    portfolios = get_portfolios()

    return render_template(
        "dashboard_admin.html",
        traders=traders,
        transactions=transactions,
        portfolios=portfolios
    )


@app.route('/dashboard_trader')
@login_required("trader")
def dashboard_trader():

    stocks = get_all_stocks()
    user = get_user_by_email(session["email"])

    return render_template(
        "dashboard_trader.html",
        user=user,
        market_data=stocks
    )


# ================= ADMIN SERVICES =================

@app.route('/service01')
@login_required("admin")
def service01():

    traders = get_traders()

    return render_template(
        "service-details-1.html",
        traders=traders
    )


@app.route('/service02')
@login_required("admin")
def service02():

    transactions = get_transactions()

    return render_template(
        "service-details-2.html",
        transactions=transactions
    )


@app.route('/service03')
@login_required("admin")
def service03():

    portfolios = get_portfolios()

    return render_template(
        "service-details-3.html",
        portfolios=portfolios
    )


# ================= TRADER SERVICES =================

@app.route('/service04')
@login_required("trader")
def service04():

    stocks = get_all_stocks()

    return render_template(
        "service-details-4.html",
        stocks=stocks
    )


@app.route('/service05')
@login_required("trader")
def service05():

    user_id = session["user_id"]

    portfolio = get_user_portfolio(user_id)

    transactions = get_user_transactions(user_id)

    return render_template(
        "service-details-5.html",
        portfolio=portfolio,
        transactions=transactions
    )
# ===== BUY STOCK =====
@app.route('/buy_stock/<stock_id>', methods=["GET","POST"])
@login_required("trader")
def buy_stock(stock_id):

    stock = get_stock_by_id(stock_id)

    if request.method == "POST":

        quantity = int(request.form["quantity"])

        user_id = session["user_id"]

        price = float(stock["price"])

        create_transaction(user_id, stock_id, "buy", quantity, price)

        update_portfolio(user_id, stock_id, quantity, price)

        send_notification(
            TRANSACTION_TOPIC_ARN,
            "Stock Purchased",
            f"User purchased {quantity} shares of {stock['symbol']}"
        )

        flash("Stock purchased successfully")

        return redirect(url_for("service05"))

    return render_template(
        "buy_stock.html",
        stock=stock
    )

# ===== SELL STOCK =====

@app.route('/sell_stock/<stock_id>', methods=["GET","POST"])
@login_required("trader")
def sell_stock(stock_id):

    stock = get_stock_by_id(stock_id)

    user_id = session["user_id"]

    portfolio_entry = get_portfolio_item(user_id, stock_id)

    if not portfolio_entry:
        flash("You do not own this stock")
        return redirect(url_for("service04"))

    if request.method == "POST":

        quantity = int(request.form["quantity"])

        if quantity > int(portfolio_entry["quantity"]):
            flash("Not enough shares to sell")
            return redirect(request.url)

        price = float(stock["price"])

        create_transaction(user_id, stock_id, "sell", quantity, price)

        new_quantity = int(portfolio_entry["quantity"]) - quantity

        update_portfolio(
            user_id,
            stock_id,
            new_quantity,
            portfolio_entry["average_price"]
        )

        send_notification(
            TRANSACTION_TOPIC_ARN,
            "Stock Sold",
            f"User sold {quantity} shares of {stock['symbol']}"
        )

        flash("Stock sold successfully")

        return redirect(url_for("service05"))

    return render_template(
        "sell_stock.html",
        stock=stock,
        portfolio_entry=portfolio_entry
    )

# ================= LOGOUT =================

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for("index"))


# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)