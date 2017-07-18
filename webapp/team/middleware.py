def team_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        if hasattr(request.user, 'player'):
            request.player = request.user.player
            request.team = request.player.team
        else:
            request.player = None
            request.team = None

        response = get_response(request)
        return response

    return middleware
