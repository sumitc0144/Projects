# Account Route

This project includes a protected route for handling user account details.

## Route Definition

```python
@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="Account")
