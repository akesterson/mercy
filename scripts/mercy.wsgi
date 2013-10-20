from mercy.MercyApplication import MercyApplication

class ScriptNameStripper(object):
    def __init__(self, app):
        self.app = app

    def __call_(self, environ, start_response):
        environ['SCRIPT_NAME'] = ''
        return self.app(environ, start_response)

app = ScriptNameStripper(MercyApplication())

if __name__ == "__main__":
    app.run()
