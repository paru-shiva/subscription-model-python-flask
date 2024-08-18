from flask import Flask, jsonify, request
from database import db_session
from database import init_db
from models import Customer, Product, Subscription
from flask_cors import CORS
import datetime
from sqlalchemy import update

app = Flask(__name__)

CORS(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


init_db()


"""s = Subscription(889, "primevid", "2024-03-03", "2023-04-04", 9)
   db_session.add(s)"""

"""User.query.all()
   User.query.filter(User.name == 'admin').first()"""

"""
User.query.filter(User.name == 'admin').first()

"""


@app.route("/")
def home_route():
    return "<p>I am from Home route.</p>"


@app.route("/get-customers")
def add_subscription():
    customers_list = Customer.query.all()
    modified_list = []

    for ei in customers_list:
        each_obj = {}
        each_obj["customer_id"] = ei.customer_id
        each_obj["customer_name"] = ei.customer_name
        modified_list.append(each_obj)

    db_session.commit()
    return jsonify(modified_list)


@app.route("/get-products")
def get_products():
    products_list = Product.query.all()
    modified_list = []
    for ei in products_list:
        each_obj = {}
        each_obj["product_name"] = ei.product_name
        modified_list.append(each_obj)

    db_session.commit()
    return jsonify(modified_list)


@app.route("/get-subscriptions")
def get_subscriptions():
    subscriptions_list = Subscription.query.all()
    modified_list = []
    for ei in subscriptions_list:
        each_obj = {}
        each_obj["product_name"] = ei.product_name
        each_obj["no_of_subscriptions"] = ei.no_of_subscriptions
        each_obj["no_of_days"] = (ei.end_date - ei.start_date).days
        modified_list.append(each_obj)

    db_session.commit()
    return jsonify(modified_list)


@app.route("/new-subscription", methods=["GET", "POST"])
def new_subscription():
    if request.method == "POST":
        customerId = request.json["customer_id"]
        productName = request.json["product_name"]
        startDate = request.json["start_date"]
        endDate = request.json["end_date"]
        noOfProducts = request.json["no_of_subscriptions"]

        required_list = Subscription.query.filter(
            Subscription.customer_id == customerId,
            Subscription.product_name == productName,
        )

        for ei in required_list:
            if (ei.end_date - datetime.date.today()).days > 0:
                return jsonify(
                    {"result": f"*You have already subscribed till {ei.end_date}"}
                )

        endYear = int(endDate.split("-")[0])
        endMonth = int(endDate.split("-")[1])
        endDay = int(endDate.split("-")[2])

        startYear = int(startDate.split("-")[0])
        startMonth = int(startDate.split("-")[1])
        startDay = int(startDate.split("-")[2])

        if (
            datetime.date(startYear, startMonth, startDay)
            - datetime.date(endYear, endMonth, endDay)
        ).days >= 0:
            return jsonify({"result": "*end date must be grater"})

        s = Subscription(customerId, productName, startDate, endDate, noOfProducts)
        db_session.add(s)
        db_session.commit()
        return jsonify({"result": "Subscription Added Successfully."})

    else:
        return "get req triggered"


@app.route("/extend-subscription", methods=["GET", "POST"])
def extend_subscription():
    if request.method == "POST":
        customerId = request.json["customer_id"]
        productName = request.json["product_name"]
        endDate = request.json["end_date"]

        required_list = Subscription.query.filter(
            Subscription.customer_id == customerId,
            Subscription.product_name == productName,
        )

        endYear = int(endDate.split("-")[0])
        endMonth = int(endDate.split("-")[1])
        endDay = int(endDate.split("-")[2])

        extensionDate = datetime.date(endYear, endMonth, endDay)

        if (datetime.date.today() - extensionDate).days >= 0:
            return jsonify({"result": f"*Please choose upcoming days."})

        activeSubscription = False
        activeSubscriptionDate = None

        for ei in required_list:
            if (ei.end_date - datetime.date.today()).days > 0:
                activeSubscriptionDate = ei.end_date
                activeSubscription = True

        if not activeSubscription:
            return jsonify(
                {"result": f"*You dont have an active subscription to extend."}
            )

        elif (extensionDate - activeSubscriptionDate).days > 0:
            Subscription.query.filter(
                Subscription.customer_id == customerId,
                Subscription.product_name == productName,
            ).update({"end_date": extensionDate})
            db_session.commit()
            return jsonify({"result": f"Extended Successfully."})

        else:
            return jsonify(
                {
                    "result": f"*You have active subscription till {activeSubscriptionDate}."
                }
            )

    else:
        return "get req triggered"


@app.route("/end-subscription", methods=["GET", "POST"])
def end_subscription():
    if request.method == "POST":
        customerId = request.json["customer_id"]
        productName = request.json["product_name"]

        required_list = Subscription.query.filter(
            Subscription.customer_id == customerId,
            Subscription.product_name == productName,
        )

        activeSubscription = False

        for ei in required_list:
            if (ei.end_date - datetime.date.today()).days > 0:
                activeSubscription = True

        if not activeSubscription:
            return jsonify({"result": f"*You dont have an active subscription."})

        else:
            print(datetime.date.today())
            Subscription.query.filter(
                Subscription.customer_id == customerId,
                Subscription.product_name == productName,
            ).update({"end_date": datetime.date.today()})
            db_session.commit()
            return jsonify({"result": f"*You Ended the Subscription"})

    else:
        return "get req triggered"
