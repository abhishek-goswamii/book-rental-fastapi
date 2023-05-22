"""all table

Revision ID: 3dd791488e07
Revises: 
Create Date: 2023-05-22 10:57:10.785269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3dd791488e07'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('firstname', sa.String(), nullable=False),
                    sa.Column('lastname', sa.String(), nullable=True),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('number', sa.Integer(), nullable=True),
                    sa.Column('profile', sa.String(), nullable=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('isAdmin', sa.Boolean(),
                              nullable=False, default=False),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('books',
                    sa.Column('BookID', sa.Integer(), nullable=False),
                    sa.Column('Title', sa.String(), nullable=True),
                    sa.Column('Author', sa.String(), nullable=True),
                    sa.Column('Description', sa.String(), nullable=True),
                    sa.Column('CoverImage', sa.String(), nullable=True),
                    sa.Column('Available', sa.Boolean(), nullable=True),
                    sa.Column('RentingPeriod', sa.Integer(), nullable=True),
                    sa.Column('PricePerDay', sa.Integer(), nullable=True),
                    sa.Column('UserID', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['UserID'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('BookID')
                    )

    op.create_table('genres',
                    sa.Column('GenreID', sa.Integer(), nullable=False),
                    sa.Column('GenreName', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('GenreID')
                    )

    op.create_table('book_genres',
                    sa.Column('BookID', sa.Integer(), nullable=False),
                    sa.Column('GenreID', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['BookID'], ['books.BookID'], ),
                    sa.ForeignKeyConstraint(['GenreID'], ['genres.GenreID'], ),
                    sa.PrimaryKeyConstraint('BookID', 'GenreID')
                    )

    op.create_table('reviews',
                    sa.Column('ReviewID', sa.Integer(), nullable=False),
                    sa.Column('UserID', sa.Integer(), nullable=True),
                    sa.Column('BookID', sa.Integer(), nullable=True),
                    sa.Column('Rating', sa.Integer(), nullable=True),
                    sa.Column('ReviewText', sa.String(), nullable=True),
                    sa.Column('ReviewDate', sa.Date(), nullable=True),
                    sa.ForeignKeyConstraint(['BookID'], ['books.BookID'], ),
                    sa.ForeignKeyConstraint(['UserID'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('ReviewID')
                    )

    op.create_table('rentals',
                    sa.Column('RentalID', sa.Integer(), nullable=False),
                    sa.Column('UserID', sa.Integer(), nullable=True),
                    sa.Column('BookID', sa.Integer(), nullable=True),
                    sa.Column('RentalPeriod', sa.Integer(), nullable=True),
                    sa.Column('RentalCost', sa.Integer(), nullable=True),
                    sa.Column('RentalDate', sa.Date(), nullable=True),
                    sa.Column('ReturnDate', sa.Date(), nullable=True),
                    sa.Column('Active', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['BookID'], ['books.BookID'], ),
                    sa.ForeignKeyConstraint(['UserID'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('RentalID')
                    )


def downgrade():
    op.drop_table('rentals')
    op.drop_table('reviews')
    op.drop_table('book_genres')
    op.drop_table('genres')
    op.drop_table('books')
    op.drop_table('users')
