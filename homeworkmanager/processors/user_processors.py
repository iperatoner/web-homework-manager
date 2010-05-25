def user(request):
    """Yeah, this is an unessecary context processor ;)"""
    
    if hasattr(request, 'user'):
        return { 'user': request.user }
    else:
        return {}
