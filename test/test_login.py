

def test_login(app):
    app.session.login("administrator", "root")