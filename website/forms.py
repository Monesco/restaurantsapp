from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField
from wtforms.validators import DataRequired


class RestaurantForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired()])
    totalReviews = FloatField('Total number of reviews', validators=[DataRequired()])
    address_line_1 = StringField('Address Line 1', validators=[DataRequired()])
    address_line_2 = StringField('Address Line 2')
    number = StringField('Number', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    zipcode = StringField('Zipcode', validators=[DataRequired()])
    style = StringField('Style', validators=[DataRequired()])
    thumbnail_url=StringField('Thumbnail Url',validators=[DataRequired()])
    menu_url=StringField('Menu Url',validators=[DataRequired()])

class ReviewForm(FlaskForm):
    reviewText= TextAreaField('Review',validators=[DataRequired()])
    rating = StringField('Rating', validators=[DataRequired()])