"""empty message

Revision ID: f86b4e5701fb
Revises: ce125f9cbfe1
Create Date: 2023-08-19 20:50:28.459100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic_utils.pg_function import PGFunction
from sqlalchemy import text as sql_text
from alembic_utils.pg_trigger import PGTrigger
from sqlalchemy import text as sql_text
from alembic_utils.pg_view import PGView
from sqlalchemy import text as sql_text

# revision identifiers, used by Alembic.
revision: str = 'f86b4e5701fb'
down_revision: Union[str, None] = 'ce125f9cbfe1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    payments_f_currency = PGFunction(
        schema="payments",
        signature="f_currency()",
        definition="RETURNS trigger language plpgsql as\n  $$\n    declare\n        current_currency payments.currency%rowtype;\n        version timestamp := coalesce(lower(new.period), current_timestamp at time zone 'utc');\n        new_id integer = new.id;\n    begin\n        select * into current_currency from payments.currency where code = new.code and period @> version;\n\n        current_currency.id = null;\n        current_currency.period = null;\n        new.id = null;\n        new.period = null;\n\n        if current_currency = new then\n            return null;\n        end if;\n\n        update payments.currency set period = tsrange(lower(period), version) where code = new.code and period @> version;\n\n        new.id = new_id;\n        new.period = tsrange(version, null);\n\n        return new;\n    end;\n  $$"
    )
    op.create_entity(payments_f_currency)

    payments_v_currency = PGView(
        schema="payments",
        signature="v_currency",
        definition="select to_char(lower(period),'dd.mm.yyyy hh24:mi:ss') datetime_utc, code, name, value\n    from payments.currency c \n    where period @> now() at time zone 'utc'\n    order by code, lower(period)"
    )
    op.create_entity(payments_v_currency)

    payments_currency_t_currency = PGTrigger(
        schema="payments",
        signature="t_currency",
        on_entity="payments.currency",
        is_constraint=False,
        definition='before insert\n\ton payments.currency\n\tfor each row\n    execute procedure payments.f_currency()'
    )
    op.create_entity(payments_currency_t_currency)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    payments_currency_t_currency = PGTrigger(
        schema="payments",
        signature="t_currency",
        on_entity="payments.currency",
        is_constraint=False,
        definition='before insert\n\ton payments.currency\n\tfor each row\n    execute procedure payments.f_currency()'
    )
    op.drop_entity(payments_currency_t_currency)

    payments_v_currency = PGView(
        schema="payments",
        signature="v_currency",
        definition="select to_char(lower(period),'dd.mm.yyyy hh24:mi:ss') datetime_utc, code, name, value\n    from payments.currency c \n    where period @> now() at time zone 'utc'\n    order by code, lower(period)"
    )
    op.drop_entity(payments_v_currency)

    payments_f_currency = PGFunction(
        schema="payments",
        signature="f_currency()",
        definition="RETURNS trigger language plpgsql as\n  $$\n    declare\n        current_currency payments.currency%rowtype;\n        version timestamp := coalesce(lower(new.period), current_timestamp at time zone 'utc');\n        new_id integer = new.id;\n    begin\n        select * into current_currency from payments.currency where code = new.code and period @> version;\n\n        current_currency.id = null;\n        current_currency.period = null;\n        new.id = null;\n        new.period = null;\n\n        if current_currency = new then\n            return null;\n        end if;\n\n        update payments.currency set period = tsrange(lower(period), version) where code = new.code and period @> version;\n\n        new.id = new_id;\n        new.period = tsrange(version, null);\n\n        return new;\n    end;\n  $$"
    )
    op.drop_entity(payments_f_currency)

    # ### end Alembic commands ###
