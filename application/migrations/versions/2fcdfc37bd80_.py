"""empty message

Revision ID: 2fcdfc37bd80
Revises: 7e530fa0691c
Create Date: 2019-10-09 15:46:44.616471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fcdfc37bd80'
down_revision = '7e530fa0691c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_posts',
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('modified_at', sa.DateTime(), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('author_id', sa.Integer(), nullable=True),
                    sa.Column('title', sa.String(length=100), nullable=False),
                    sa.Column('body', sa.String(length=200), nullable=False),
                    sa.Column('image', sa.Binary(), nullable=False),
                    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('bookmarks_user',
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('modified_at', sa.DateTime(), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('bookmark_user_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['bookmark_user_id'], ['users.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('profiles',
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('modified_at', sa.DateTime(), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('nickname', sa.String(length=80), nullable=True),
                    sa.Column('comment', sa.String(length=200), nullable=True),
                    sa.Column('icon', sa.Binary(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('bookmarks_post',
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('modified_at', sa.DateTime(), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('bookmark_post_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['bookmark_post_id'], ['blog_posts.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookmarks_post')
    op.drop_table('profiles')
    op.drop_table('bookmarks_user')
    op.drop_table('blog_posts')
    # ### end Alembic commands ###
