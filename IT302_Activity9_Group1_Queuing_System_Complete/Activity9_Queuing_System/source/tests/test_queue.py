import json
import os
from pathlib import Path
import pytest
from pages.login_page import LoginPage
from pages.queue_page import QueuePage

CASES = json.loads((Path(__file__).parents[1] / 'data/login_cases.json').read_text())

def credentials():
    # Public synthetic defaults are for the bundled demo only. Use env vars for other test environments.
    return os.environ.get('DEMO_USER', 'staff.demo'), os.environ.get('DEMO_PASSWORD', 'DemoQueue123!')

def sign_in(driver, app_url):
    user, password = credentials()
    LoginPage(driver, app_url).open().submit(user, password)
    page = QueuePage(driver)
    assert user in page.identity()
    return page

@pytest.mark.smoke
@pytest.mark.parametrize('case', CASES, ids=[c['id'] for c in CASES])
def test_login(driver, app_url, case, evidence):
    """AUTO-Q01 -> QTC-01 (TC-01 adaptation); AUTO-Q02 -> QTC-03 (TC-03 adaptation)."""
    user, password = credentials()
    login = LoginPage(driver, app_url).open()
    login.submit(user, password if case['kind'] == 'valid' else case['password'])
    if case['kind'] == 'valid':
        assert user in QueuePage(driver).identity()
        assert driver.current_url.endswith('#queue')
    else:
        assert case['expected'] in login.error_containing(case['expected'])
        evidence('AUTO-Q02-validation')
        driver.get(app_url + '/queue#queue')
        login.wait.until(lambda d: not d.current_url.endswith('#queue'))
        # Protected content requires a valid server-side session, even at the queue URL.
        assert login.wait.until(lambda d: d.find_element(*login.USERNAME).is_displayed())
        assert not driver.find_element(*QueuePage.IDENTITY).is_displayed()
    evidence(case['id'])

@pytest.mark.regression
def test_lockout_after_five_invalid_attempts(driver, app_url, evidence):
    """AUTO-Q03 -> QTC-02, adapted from Activity 5 TC-02/R2."""
    user, valid_password = credentials()
    login = LoginPage(driver, app_url).open()
    wrong_password = valid_password + '-wrong'
    for attempt in range(1, 6):
        login.submit(user, wrong_password)
        expected = 'Account locked' if attempt == 5 else f'attempt {attempt} of 5'
        assert expected in login.error_containing(expected)
    login.submit(user, valid_password)
    assert 'Account locked' in login.error_containing('Account locked')
    assert driver.find_element(*login.USERNAME).is_displayed()
    evidence('AUTO-Q03')

@pytest.mark.regression
def test_duplicate_ticket_is_prevented(driver, app_url, evidence):
    """AUTO-Q04 -> QTC-04, adapted from Activity 5 TC-06/R6, DEF-004 principle."""
    queue = sign_in(driver, app_url)
    assert 'created' in queue.issue('CUST-001', 'Registrar')
    first = queue.rows()
    assert first == [['Q-001', 'CUST-001', 'Registrar', 'Waiting']]
    message = queue.issue('CUST-001', 'Registrar')
    evidence('AUTO-Q04-after-repeat')
    assert 'already has an active ticket' in message, f'Duplicate not rejected: {message}'
    assert queue.rows() == first, 'Repeat submission changed the active ticket records'
    # Check persistent server state through a browser refresh, not only the message.
    driver.refresh()
    assert credentials()[0] in queue.identity()
    queue.wait.until(lambda d: len(queue.rows()) > 0)
    assert queue.rows() == first

@pytest.mark.regression
def test_valid_ticket_is_saved(driver, app_url, evidence):
    """AUTO-Q05 -> QTC-05, adapted from Activity 5 TC-08/R7."""
    queue = sign_in(driver, app_url)
    assert 'Ticket Q-001 created' in queue.issue('CUST-002', 'Cashier')
    assert queue.rows() == [['Q-001', 'CUST-002', 'Cashier', 'Waiting']]
    driver.refresh()
    queue.identity()
    queue.wait.until(lambda d: len(queue.rows()) > 0)
    assert queue.rows() == [['Q-001', 'CUST-002', 'Cashier', 'Waiting']]
    evidence('AUTO-Q05')
