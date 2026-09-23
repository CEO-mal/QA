import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    # Десктопный размер окна: при узком окне сайт показывает мобильное меню
    return {**browser_context_args, "viewport": {"width": 1440, "height": 900}}