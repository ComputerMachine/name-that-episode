from pyramid.view import view_config


@view_config(route_name='home', renderer='webserver:templates/home.mako')
def my_view(request):
    data = request.registry.settings["episode_data"]
    return {
        "project": "name-that-episode"
    }
