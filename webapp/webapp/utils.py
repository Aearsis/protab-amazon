import random
from django.contrib.auth.decorators import user_passes_test, permission_required


def player_required(view_func):
    """
    Decorator that ensures logged user have a team
    """
    player_decorator = user_passes_test(
        lambda u: hasattr(u, 'player') and u.player is not None
    )
    return player_decorator(view_func)


def miner_required(view_func):
    return permission_required('goods.can_mine')(player_required(view_func))


def seller_required(view_func):
    return permission_required('goods.can_sell')(player_required(view_func))


def random_token(len):
    return "".join(random.choice("QWERTYUIPASDFGHJKLZXCVBNM123456789") for _ in range(len))
