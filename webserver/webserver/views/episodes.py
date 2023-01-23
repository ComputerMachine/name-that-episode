from pyramid.view import view_config


@view_config(route_name='episodes', renderer='webserver:templates/episodes.mako')
def my_view(request):
    return {
        "project": "name-that-episode",
        "data": request.registry.settings["episode_data"]
    }
