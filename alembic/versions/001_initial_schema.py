"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-05-01

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "drawers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(10), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("label"),
    )

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.ForeignKeyConstraint(["parent_id"], ["categories.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )

    op.create_table(
        "compartments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("drawer_id", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(10), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["drawer_id"], ["drawers.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("label"),
        sa.UniqueConstraint("drawer_id", "label", name="uq_compartment_drawer_label"),
    )

    op.create_table(
        "components",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("manufacturer", sa.String(100), nullable=True),
        sa.Column("part_number", sa.String(100), nullable=True),
        sa.Column("tags", postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column("specs", postgresql.JSONB(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("search_vector", postgresql.TSVECTOR(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_components_search_vector",
        "components",
        ["search_vector"],
        postgresql_using="gin",
    )
    op.create_index(
        "ix_components_tags",
        "components",
        ["tags"],
        postgresql_using="gin",
    )
    op.create_index(
        "ix_components_specs",
        "components",
        ["specs"],
        postgresql_using="gin",
    )

    op.create_table(
        "stock",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("component_id", sa.Integer(), nullable=False),
        sa.Column("compartment_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("minimum_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("unit", sa.String(20), nullable=False, server_default="st"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["component_id"], ["components.id"]),
        sa.ForeignKeyConstraint(["compartment_id"], ["compartments.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("component_id", "compartment_id", name="uq_stock_component_compartment"),
    )

    op.create_table(
        "files",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("component_id", sa.Integer(), nullable=False),
        sa.Column("file_type", sa.String(20), nullable=True),
        sa.Column("source", sa.String(20), nullable=False, server_default="upload"),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("filepath", sa.Text(), nullable=False),
        sa.Column("mime_type", sa.String(100), nullable=True),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["component_id"], ["components.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Trigger för att uppdatera search_vector
    op.execute("""
        CREATE OR REPLACE FUNCTION update_component_search_vector()
        RETURNS trigger AS $$
        BEGIN
            NEW.search_vector :=
                setweight(to_tsvector('swedish', coalesce(NEW.name, '')), 'A') ||
                setweight(to_tsvector('swedish', coalesce(NEW.part_number, '')), 'A') ||
                setweight(to_tsvector('swedish', coalesce(NEW.description, '')), 'B') ||
                setweight(to_tsvector('swedish', coalesce(NEW.manufacturer, '')), 'C');
            NEW.updated_at := now();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER components_search_vector_update
        BEFORE INSERT OR UPDATE ON components
        FOR EACH ROW EXECUTE FUNCTION update_component_search_vector();
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS components_search_vector_update ON components")
    op.execute("DROP FUNCTION IF EXISTS update_component_search_vector")
    op.drop_table("files")
    op.drop_table("stock")
    op.drop_index("ix_components_specs", table_name="components")
    op.drop_index("ix_components_tags", table_name="components")
    op.drop_index("ix_components_search_vector", table_name="components")
    op.drop_table("components")
    op.drop_table("compartments")
    op.drop_table("categories")
    op.drop_table("drawers")
