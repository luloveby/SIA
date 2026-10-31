"""Supplemental full-height browser captures of the two demo duplicate states."""
import os
import threading
from pathlib import Path
from selenium import webdriver
from demo.server import build_server
from pages.login_page import LoginPage
from pages.queue_page import QueuePage

out=Path('../evidence/supplemental');out.mkdir(parents=True,exist_ok=True)
for run,bug in [(1,True),(2,False)]:
 server=build_server(duplicate_bug=bug)
 worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
 options=webdriver.ChromeOptions();options.add_argument('--headless=new');options.add_argument('--disable-gpu');options.add_argument('--window-size=1365,1400')
 import shlex
 for flag in shlex.split(os.environ.get('BROWSER_EXTRA_ARGS','')):options.add_argument(flag)
 driver=webdriver.Chrome(options=options)
 try:
  driver.set_window_size(1365,1400)
  LoginPage(driver,f'http://127.0.0.1:{server.server_port}').open().submit('staff.demo','DemoQueue123!')
  queue=QueuePage(driver);queue.identity();queue.issue('CUST-001','Registrar');queue.issue('CUST-001','Registrar')
  assert len(queue.rows())==(2 if bug else 1)
  target=out/f'run-0{run}-AUTO-Q04-full.png';driver.save_screenshot(str(target));print(target)
 finally:
  driver.quit();server.shutdown();server.server_close();worker.join(timeout=5)
(out/'README.txt').write_text('Supplemental captures recreated the baseline/fixed AUTO-Q04 states with a taller browser window so both ticket rows are visible. These were captured after the two full test runs, not at the original test timestamps. Original unmodified screenshots and logs remain in run-01 and run-02. Reproduce from source/: python -m scripts.capture_demo.\n',encoding='utf8')
