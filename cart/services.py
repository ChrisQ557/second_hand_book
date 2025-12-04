from typing import Dict, Tuple

CART_KEY = "cart"


def _get_cart(session) -> Dict[str, Dict[str, int]]:
    return session.get(CART_KEY, {})


def _save_cart(session, cart: Dict[str, Dict[str, int]]):
    session[CART_KEY] = cart
    session.modified = True


def add_item(session, book_id: int, qty: int = 1) -> None:
    cart = _get_cart(session)
    key = str(book_id)
    entry = cart.get(key, {"qty": 0})
    entry["qty"] = int(entry.get("qty", 0)) + int(qty)
    cart[key] = entry
    _save_cart(session, cart)


def update_item(session, book_id: int, qty: int) -> None:
    cart = _get_cart(session)
    key = str(book_id)
    if qty <= 0:
        cart.pop(key, None)
    else:
        cart[key] = {"qty": int(qty)}
    _save_cart(session, cart)


def remove_item(session, book_id: int) -> None:
    cart = _get_cart(session)
    cart.pop(str(book_id), None)
    _save_cart(session, cart)


def total_qty(session) -> int:
    cart = _get_cart(session)
    return sum(int(v.get("qty", 0)) for v in cart.values())
