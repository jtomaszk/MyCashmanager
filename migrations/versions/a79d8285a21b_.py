"""initial revision

Revision ID: a79d8285a21b
Revises: None
Create Date: 2016-03-03 13:23:59.788908

"""

# revision identifiers, used by Alembic.
revision = 'a79d8285a21b'
down_revision = None

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import database


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType, nullable=False),
                    sa.Column('name', sa.String(length=200), nullable=True),
                    sa.Column('email', sa.String(length=200), nullable=True),
                    sa.Column('picture', sa.String(length=200), nullable=True),
                    sa.Column('oauth2_id', sa.String(length=200), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('category',
                    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType, nullable=False),
                    sa.Column('name', sa.String(length=200), nullable=True),
                    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType, nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('currency',
                    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType, nullable=False),
                    sa.Column('name', sa.String(length=200), nullable=True),
                    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType, nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('account',
                    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType, nullable=False),
                    sa.Column('name', sa.String(length=200), nullable=True),
                    sa.Column('deleted', sa.Boolean(), nullable=True),
                    sa.Column('currency_id', sqlalchemy_utils.types.uuid.UUIDType, nullable=True),
                    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType, nullable=True),
                    sa.Column('balance', database.numeric_type.SqliteNumeric(), nullable=True),
                    sa.ForeignKeyConstraint(['currency_id'], ['currency.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('cycle',
                    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType, nullable=False),
                    sa.Column('account_id', sqlalchemy_utils.types.uuid.UUIDType, nullable=True),
                    sa.Column('category_id', sqlalchemy_utils.types.uuid.UUIDType, nullable=True),
                    sa.Column('transaction_type', sa.Enum('INCOME', 'OUTCOME', name='cycle_transaction_types'), nullable=True),
                    sa.Column('name', sa.String(length=200), nullable=False),
                    sa.Column('date_start', sa.Date(), nullable=False),
                    sa.Column('date_end', sa.Date(), nullable=True),
                    sa.Column('date_last', sa.Date(), nullable=True),
                    sa.Column('date_next', sa.Date(), nullable=True),
                    sa.Column('count', sa.Integer(), nullable=True),
                    sa.Column('max_count', sa.Integer(), nullable=True),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.Column('repeat_type', sa.Enum('days', 'weeks', 'months', 'years', name='repeat_types'), nullable=True),
                    sa.Column('repeat_every', sa.Integer(), nullable=True),
                    sa.Column('amount', database.numeric_type.SqliteNumeric(), nullable=True),
                    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
                    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('transaction',
                    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType, nullable=False),
                    sa.Column('transaction_type', sa.Enum('INCOME', 'OUTCOME', 'TRANSFER', name='transaction_types'), nullable=True),
                    sa.Column('transfer_id', sqlalchemy_utils.types.uuid.UUIDType, nullable=True),
                    sa.Column('cycle_id', sqlalchemy_utils.types.uuid.UUIDType, nullable=True),
                    sa.Column('category_id', sqlalchemy_utils.types.uuid.UUIDType, nullable=True),
                    sa.Column('account_id', sqlalchemy_utils.types.uuid.UUIDType, nullable=True),
                    sa.Column('amount', database.numeric_type.SqliteNumeric(), nullable=True),
                    sa.Column('amount_orig', database.numeric_type.SqliteNumeric(), nullable=True),
                    sa.Column('orig_currency_id', sqlalchemy_utils.types.uuid.UUIDType, nullable=True),
                    sa.Column('date', sa.DateTime(), nullable=True),
                    sa.Column('running_total', database.numeric_type.SqliteNumeric(), nullable=True),
                    sa.Column('comment', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
                    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
                    sa.ForeignKeyConstraint(['cycle_id'], ['cycle.id'], ),
                    sa.ForeignKeyConstraint(['orig_currency_id'], ['currency.id'], ),
                    sa.ForeignKeyConstraint(['transfer_id'], ['transaction.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_transaction_account_id'), 'transaction', ['account_id'], unique=False)
    op.create_index(op.f('ix_transaction_category_id'), 'transaction', ['category_id'], unique=False)
    op.create_index(op.f('ix_transaction_cycle_id'), 'transaction', ['cycle_id'], unique=False)
    op.create_index(op.f('ix_transaction_transfer_id'), 'transaction', ['transfer_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transaction_transfer_id'), table_name='transaction')
    op.drop_index(op.f('ix_transaction_cycle_id'), table_name='transaction')
    op.drop_index(op.f('ix_transaction_category_id'), table_name='transaction')
    op.drop_index(op.f('ix_transaction_account_id'), table_name='transaction')
    op.drop_table('transaction')
    op.drop_table('cycle')
    op.drop_table('account')
    op.drop_table('currency')
    op.drop_table('category')
    op.drop_table('user')
    ### end Alembic commands ###