from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'bd72317e7e24'
down_revision: Union[str, None] = '62f1a8ae9eb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE useraccess ADD VALUE IF NOT EXISTS 'EMPLOYEE'")
    op.execute("ALTER TYPE useraccess ADD VALUE IF NOT EXISTS 'STORE_OWNER'")
    op.execute("ALTER TYPE useraccess ADD VALUE IF NOT EXISTS 'GUEST'")

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("CREATE TYPE useraccess_new AS ENUM ('ADMIN', 'STORE_OWNER')")
    op.execute("""
        ALTER TABLE "user"
        ALTER COLUMN user_access TYPE useraccess_new
        USING user_access::text::useraccess_new
    """)
    op.execute("DROP TYPE useraccess")
    op.execute("ALTER TYPE useraccess_new RENAME TO useraccess")
