import json
import logging
import os
import platform
import re
import shlex
import threading
from pathlib import Path
from urllib.request import Request, urlopen
import pytest
import selenium
from selenium import webdriver
from demo.server import build_server

LOG = logging.getLogger('queue-tests')

def pytest_addoption(parser):
    parser.addoption('--demo-bug', action='store_true', help='Reproduce the sample duplicate-ticket defect')
    parser.addoption('--evidence-dir', default='reports/actual-run')

def pytest_configure(config):
    out = Path(config.getoption('--evidence-dir'))
    out.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(out / 'run.log', mode='w', encoding='utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    LOG.handlers.clear()
    LOG.addHandler(handler)
    LOG.setLevel(logging.INFO)
    LOG.info('ACTUAL SAMPLE DEMO RUN; Python=%s Selenium=%s pytest=%s bug=%s',
             platform.python_version(), selenium.__version__, pytest.__version__, config.getoption('--demo-bug'))

@pytest.fixture(scope='session')
def app_url(pytestconfig):
    external = os.environ.get('BASE_URL')
    if external:
        # A compatible NON-PRODUCTION test deployment only; see README adaptation notes.
        yield external.rstrip('/')
        return
    server = build_server(duplicate_bug=pytestconfig.getoption('--demo-bug'))
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    yield f'http://127.0.0.1:{server.server_port}'
    server.shutdown()
    server.server_close()
    worker.join(timeout=5)

@pytest.fixture(autouse=True)
def isolated_data(app_url):
    def reset():
        req = Request(app_url + '/__test__/reset', data=b'{}', method='POST',
                      headers={'Content-Type': 'application/json', 'X-Test-Token': os.environ.get('TEST_RESET_TOKEN', 'local-demo-reset')})
        with urlopen(req, timeout=10) as response:
            assert response.status == 200
    reset()
    yield
    reset()

@pytest.fixture
def driver():
    browser = os.environ.get('BROWSER', 'chrome').lower()
    headless = os.environ.get('HEADLESS', 'true').lower() == 'true'
    if browser == 'firefox':
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('-headless')
        instance = webdriver.Firefox(options=options)
    elif browser in ('chrome', 'edge'):
        options = webdriver.ChromeOptions() if browser == 'chrome' else webdriver.EdgeOptions()
        if headless:
            options.add_argument('--headless=new')
        options.add_argument('--window-size=1365,1000')
        options.add_argument('--disable-gpu')
        for flag in shlex.split(os.environ.get('BROWSER_EXTRA_ARGS', '')):
            options.add_argument(flag)
        instance = webdriver.Chrome(options=options) if browser == 'chrome' else webdriver.Edge(options=options)
    else:
        raise ValueError('BROWSER must be edge, chrome or firefox')
    try:
        instance.set_window_size(1365, 1000)
        LOG.info('browser=%s version=%s', browser, instance.capabilities.get('browserVersion'))
        yield instance
    finally:
        instance.quit()

def safe_name(nodeid):
    return re.sub(r'[^a-zA-Z0-9_-]+', '_', nodeid)

@pytest.fixture
def evidence(request, driver, pytestconfig):
    def capture(label):
        folder = Path(pytestconfig.getoption('--evidence-dir')) / 'screenshots'
        folder.mkdir(parents=True, exist_ok=True)
        driver.save_screenshot(str(folder / (safe_name(request.node.nodeid) + '_' + label + '.png')))
    return capture

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    if report.when == 'call' or report.failed:
        LOG.info('%s [%s] %s %.3fs', item.nodeid, report.when, report.outcome.upper(), report.duration)
        if report.failed:
            LOG.error('%s', report.longreprtext)
            browser = item.funcargs.get('driver')
            if browser:
                folder = Path(item.config.getoption('--evidence-dir')) / 'screenshots'
                folder.mkdir(parents=True, exist_ok=True)
                browser.save_screenshot(str(folder / (safe_name(item.nodeid) + '_FAIL.png')))
