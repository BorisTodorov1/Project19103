from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange




class AddProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[Length(max=100)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Product')

class DeleteProductForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    submit = SubmitField('Delete Product')

class EditProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[Length(max=100)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Update Product')