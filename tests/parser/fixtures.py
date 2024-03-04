import pytest

import os
import subprocess
import sqlite3

from typing import Optional, Union
from pathlib import Path

# This seems kind of heavy, running archivebox init before every test :shrug:
@pytest.fixture(autouse=True)
def archivebox_init(tmp_path):
    os.chdir(tmp_path)
    process = subprocess.run(['archivebox', 'init', '--quick'], capture_output=True)

# We poke around in the database to verify what happened, but maybe we should be
# working with the Django Models instead?
@pytest.fixture
def db():
    conn = sqlite3.connect("index.sqlite3")
    conn.row_factory = sqlite3.Row
    return conn.cursor()

@pytest.fixture
def base_url():
    return 'http://127.0.0.1:8080/static/'

@pytest.fixture
def base_path():
    return '../../mock_server/templates/'

def add_files_or_urls(urls: Union[str, list[str]], options: Optional[list] = None):
    if isinstance(urls, str):
        urls = [ urls ]

    # Build the command
    command = [ "archivebox", "add"] + urls + [ "--index-only" ];
    if options:
        command += options

    # Run our command, capturing stdout and stderr
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Return what horrors we have created
    return process.stdout.decode('utf-8')

def add_stdin(data: str, options: Optional[list] = None):
    # Build the command
    command = [ "archivebox", "add", "--index-only" ];
    if options:
        command += options

    # Run our command, feeding it stdin and capturing stdout and stderr
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    process.stdin.write(data.encode())
    outs, errs = process.communicate() # errs should actually be empty
    process.stdin.close()

    # should we check process.retcode here?

    return outs.decode('utf-8')

# useful for debugging test cases
def dump_snapshot(db):
    results = db.execute("SELECT * FROM core_snapshot").fetchall()
    for row in results:
        print(dict(row))
