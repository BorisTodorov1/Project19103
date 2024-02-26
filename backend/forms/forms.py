from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, NumberRange



class AddCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    definition = StringField('Definition')  # Add any other fields you want
    submit = SubmitField('Add Category')

class DeleteCategoryForm(FlaskForm):
    category_id = IntegerField('Category ID', validators=[DataRequired()])
    submit = SubmitField('Delete Category')

class AddProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[Length(max=100)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Add Product')
    category = SelectField('Category', coerce=int, choices=['Restoration', 'Maintenance', 'Upgrades'], validators=[DataRequired()])

class DeleteProductForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    submit = SubmitField('Delete Product')

class EditProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[Length(max=100)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Update Product')

class PlaceOrderForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    location = StringField('Location', validators=[DataRequired()])
    payment_method = SelectField('Payment Method', choices=[('Credit Card', 'Credit Card'), ('Cash on Delivery', 'Cash on Delivery')], validators=[DataRequired()])
    submit = SubmitField('Place Order')