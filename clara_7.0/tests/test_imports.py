def test_imports():
    import clara
    from clara.api.main import app
    assert app.title == "Clara 7.0"
