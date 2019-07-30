"""empty message

Revision ID: a07d939cee17
Revises: 
Create Date: 2019-07-23 15:39:52.566527

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'a07d939cee17'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('cell_phone', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('secret_question', sa.String(), nullable=True),
    sa.Column('secret_answer', sa.String(), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('avatar_url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('flask_dance_oauth',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('token', sqlalchemy_utils.types.json.JSONType(), nullable=False),
    sa.Column('provider_user_id', sa.String(length=256), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('provider_user_id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('imageUrl', sa.String(), nullable=False),
    sa.Column('pet_size', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('count_rate', sa.Integer(), nullable=False),
    sa.Column('avg_rating', sa.Float(), nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['seller_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('comment__product',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product_poster_id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['product_poster_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('product_id', 'product_poster_id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_datetime', sa.DateTime(), nullable=False),
    sa.Column('current_status', sa.String(), nullable=False),
    sa.Column('order_quantity', sa.Integer(), nullable=False),
    sa.Column('final_price', sa.Float(), nullable=False),
    sa.Column('total', sa.Integer(), nullable=False),
    sa.Column('processed_datetime', sa.DateTime(), nullable=True),
    sa.Column('note', sa.String(), nullable=True),
    sa.Column('payment_type', sa.String(), nullable=False),
    sa.Column('buyer_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['buyer_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rating__product',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('rater_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['rater_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('product_id', 'rater_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rating__product')
    op.drop_table('order')
    op.drop_table('comment__product')
    op.drop_table('token')
    op.drop_table('product')
    op.drop_table('flask_dance_oauth')
    op.drop_table('user')
    # ### end Alembic commands ###