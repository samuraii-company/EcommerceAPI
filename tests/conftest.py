import pytest

from ecommerce.user import models
from ecommerce.products import models as mdls


@pytest.fixture(autouse=True)
def create_dummy_user(tmpdir):
    """Fixture to execute asserts before and after a test is run"""

    from ecommerce.conf_test_db import override_get_db

    database = next(override_get_db())
    new_user = models.User(name="test", email="test@gmail.com", password="password")
    database.add(new_user)
    database.commit()

    yield  # this is where the testing happens

    database.query(models.User).delete()
    database.commit()
    database.query(mdls.Product).delete()
    database.commit()
    database.query(mdls.Category).delete()
    database.commit()
