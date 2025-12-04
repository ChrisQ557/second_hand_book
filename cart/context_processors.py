from .services import total_qty

def cart_context(request):
    return {
        "cart_count": total_qty(request.session)
    }
