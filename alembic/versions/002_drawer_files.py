"""Add drawer_id to files, make component_id nullable

Revision ID: 002
Revises: 001
"""
from alembic import op
import sqlalchemy as sa

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("files", "component_id", nullable=True)
    op.add_column("files", sa.Column("drawer_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_files_drawer_id", "files", "drawers", ["drawer_id"], ["id"]
    )


def downgrade() -> None:
    op.drop_constraint("fk_files_drawer_id", "files", type_="foreignkey")
    op.drop_column("files", "drawer_id")
    op.alter_column("files", "component_id", nullable=False)
