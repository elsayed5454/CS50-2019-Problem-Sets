import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Make a list of dicts having the symbol, sum of shares, sum of cost
    stocks = db.execute(
        "SELECT symbol, SUM(shares) FROM history WHERE user_id = :id GROUP BY symbol HAVING SUM(shares) > 0;", id=session.get("user_id"))

    # Get the cash remained
    cash = db.execute("SELECT cash FROM users where id = :id", id=session.get("user_id"))[0]['cash']
    total_cost = cash

    # Looping through the stocks
    for stock in stocks:
        # Get the price of symbol and increasing the total cost
        price = lookup(stock['symbol'])['price']
        total_cost += price * stock['SUM(shares)']
        # Add name of symbol to dict and reformat the price and cost of shares
        stock['name'] = lookup(stock['symbol'])['name']
        stock['price'] = usd(price)
        stock['cost'] = usd(price * stock['SUM(shares)'])

    # Reformat the total cost and cash
    total_cost = usd(total_cost)
    cash = usd(cash)

    # Redirect user to homepage
    return render_template("index.html", stocks=stocks, cash=cash, total_cost=total_cost)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST
    if request.method == "POST":

        # Ensure symbol is not blank
        if not request.form.get("symbol"):
            return apology("Missing symbol!")

        # Ensure symbol is valid
        dict = lookup(request.form.get("symbol"))
        if not dict:
            return apology("Invalid symbol!")

        # Ensure shares is not blank
        if not request.form.get("shares"):
            return apology("Missing shares!")

        # Ensure shares is valid
        if not request.form.get("shares").isdigit():
            return apology("Invalid shares!")

        # Ensure shares is not negative
        if (int)(request.form.get("shares")) < 0:
            return apology("Invalid shares!")

        # Ensure that user can afford that no of shares
        user = db.execute("SELECT * FROM users where id = :id", id=session.get("user_id"))
        cost = float(request.form.get("shares")) * dict['price']
        if user[0]['cash'] < cost:
            return apology("You can't afford that!")

        # Inserting transaction into history table
        db.execute("INSERT INTO history (user_id, symbol, price, shares, time) VALUES(:id, :symbol, :price, :shares, datetime('now','localtime'));",
                   id=user[0]['id'], price=dict['price'], shares=request.form.get("shares"), symbol=dict['symbol'])

        # Update user cash
        db.execute("UPDATE users SET cash = cash - :cost where id = :id", cost=cost, id=user[0]['id'])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Ensure username is not in database and its length is at least 1
    username = request.args.get("username")
    if len(username) > 0 and not db.execute("SELECT * FROM users WHERE username = :username", username=username):
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change password for user"""

    # User reached route via POST
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = :id", id=session.get("user_id"))

        # Ensure password is not blank
        if not request.form.get("old password"):
            return apology("Missing password!")

        # Ensure old password is correct
        if not check_password_hash(rows[0]["hash"], request.form.get("old password")):
            return apology("Invalid old password")

        # Ensure new password is not blank
        if not request.form.get("new password"):
            return apology("Missing new password!")

        # Ensure old password doesn't match new password
        if request.form.get("old password") == request.form.get("new password"):
            return apology("Passwords match!")

        # Update password
        db.execute("UPDATE users SET hash=:hash WHERE id=:id", id=session.get(
            "user_id"), hash=generate_password_hash(request.form.get("new password")))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("change_password.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Make a list of dicts having the symbol, shares, cost and time
    stocks = db.execute("SELECT symbol, shares, price, time FROM history WHERE user_id = :id GROUP BY time;",
                        id=session.get("user_id"))

    # Reformat the cost in stocks
    for stock in stocks:
        stock['price'] = usd(stock['price'])

    # Redirect user to history page
    return render_template("history.html", stocks=stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST
    if request.method == "POST":

        # Ensure symbol is not blank
        if not request.form.get("symbol"):
            return apology("Missing symbol!")

        # Ensure symbol is valid
        dict = lookup(request.form.get("symbol"))
        if not dict:
            return apology("Invalid symbol!")

        # Reformat the price
        dict['price'] = usd(dict['price'])

        # Redirect user to another template
        return render_template("lookup.html", dict=dict)

    # User reached route via GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST
    if request.method == "POST":

        # Ensure username is not blank
        if not request.form.get("username"):
            return apology("Missing username!")

        # Ensure username is not in database
        exist = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if exist:
            return apology("Username exists!")

        # Ensure password is not blank
        if not request.form.get("password"):
            return apology("Missing password!")

        # Ensure confirmation is not blank
        if not request.form.get("confirmation"):
            return apology("Missing confirmation!")

        # Ensure password matches confirmation
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords don't match!")

        # Insert the new user into userss
        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get(
            "username"), hash=generate_password_hash(request.form.get("password")))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Make a list of dicts having the symbol, sum of shares, sum of cost
    stocks = db.execute("SELECT symbol, SUM(shares) FROM history WHERE user_id = :id GROUP BY symbol;", id=session.get("user_id"))

    # User reached route via POST
    if request.method == "POST":

        # Ensure symbol is valid
        if not request.form.get("symbol"):
            return apology("Missing symbol!")

        # Ensure shares are valid
        if not request.form.get("shares"):
            return apology("Missing shares!")

        # Get symbol and shares from user
        symbol = request.form.get("symbol")
        shares = (int)(request.form.get("shares"))

        # Looping through stocks to find the right symbol
        for stock in stocks:
            if symbol == stock['symbol']:
                # Ensure the number of shares to be sold
                if shares <= stock['SUM(shares)']:
                    break
                else:
                    return apology("You don't own that number of shares!")

        # Inserting transaction into history table
        db.execute("INSERT INTO history (user_id, symbol, price, shares, time) VALUES(:id, :symbol, :price, :shares, datetime('now','localtime'));",
                   id=session.get("user_id"), symbol=symbol, price=lookup(symbol)['price'], shares=-shares)

        # Update user cash
        db.execute("UPDATE users SET cash = cash + :cost where id = :id",
                   cost=shares * lookup(symbol)['price'], id=session.get("user_id"))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
