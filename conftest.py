import pytest
import json
import os.path
import importlib
import jsonpickle
from fixture.application import Application

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        path_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(path_file) as config_file:
            target = json.load(config_file)
    return target


@pytest.fixture(scope="session")
def app(request):
    global fixture
    web_config = load_config(request.config.getoption('--target'))["web"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=web_config["browser"], base_url=web_config["baseUrl"])
    fixture.session.login(username=web_config["username"], password=web_config["password"])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

@pytest.fixture(scope="session")
def db(request):
    db_config = load_config(request.config.getoption('--target'))["db"]
    dbfixture = Dbfixture(host=db_config["host"], database=db_config["database"], user=db_config["user"], password=db_config["password"])
    def final():
        dbfixture.destroy()
    request.addfinalizer(final)
    return dbfixture


@pytest.fixture
def check_ui(request):
    return request.config.getoption('--check_ui')



def pytest_addoption(parser):
    parser.addoption('--target', action='store', default='target.json')
    parser.addoption('--check_ui', action='store_true')


def pytest_generate_tests(metafunc):  # фикстура для связки данных для групп с тестами
    for fixture in metafunc.fixturenames:  # цикл для поиска фикстур
        if fixture.startswith("group_data"):  # если начинается с "group_data"
            testdata = load_from_module(fixture)  # загружаем в переменную тестовые данные
            metafunc.parametrize(fixture, testdata, ids=[repr(x) for x in testdata])  # параметризуем
        elif fixture.startswith("groups"):  # аналогично предыдущему, только для json файла
            data = load_from_json(fixture)
            metafunc.parametrize(fixture, data, ids=[repr(x) for x in data])


def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata


def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())

