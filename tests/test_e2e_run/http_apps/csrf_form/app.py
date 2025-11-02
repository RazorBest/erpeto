from flask import Flask, request, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Needed for CSRF

SECRET1 = "alpha"
SECRET2 = "beta"


class MyForm(FlaskForm):
    field1 = StringField("Field 1", validators=[DataRequired()])
    field2 = StringField("Field 2", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():
    form = MyForm()
    if form.validate_on_submit() and form.field1.data == SECRET1 and form.field2.data == SECRET2:
        return "SUCCESS", 200
    return render_template_string(
        """
        <form method="post">
            {{ form.csrf_token }}
            {{ form.field1.label }} {{ form.field1 }}<br>
            {{ form.field2.label }} {{ form.field2 }}<br>
            {{ form.submit }}
        </form>

        <p>The secret is not alpha</p>
    """,
        form=form,
    )


if __name__ == "__main__":
    app.run(debug=False)
