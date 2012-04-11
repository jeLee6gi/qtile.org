import flask
import os
from jinja2 import TemplateNotFound
from pygments_extension import PygmentsExtension

app = flask.Flask(__name__)
app.jinja_env.add_extension(PygmentsExtension)

debug = not os.environ.get('ON_HEROKU')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>/')
def qtile_dot_org(path):
    ## Redirect the favicon to the proper file
    if path == 'favicon.ico':
        return flask.redirect('/static/img/favicon.ico')

    ## Render the appropriate template based on the URL path
    try:
        template = 'pages/{0}.html'.format(path or 'index')
        response = flask.render_template(template, debug=debug)
    except TemplateNotFound:
        ## No template == 404
        response = flask.render_template('404.html', debug=debug)
    return response

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=debug
    )
