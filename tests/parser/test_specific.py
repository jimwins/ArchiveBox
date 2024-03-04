from .fixtures import *

# These tests are based on this comment:
#   https://github.com/ArchiveBox/ArchiveBox/issues/1363#issuecomment-1966177173
# The first tests from the comment using --parser=auto are in ./test_auto.py
#
# These tests are with JSON instead of RSS because the RSS tests added in
# PR#1362 hadn't been added at the time these tests were written.
#
# --depth=0 is the default, so our tests don't set it explicitly
#
# Examples from the comment with `curl -s <url>` are not included because
# they're functionally equivalent to just piping in a local file via stdin.
#
# We use two JSON files: 1.json and 2.json available via mock_server or as
# files. 1.json includes the URL for '1.html' on mock_server and 2.json
# includes '2.html'
#
# Variations were added for both single-argument and two-argument versions of
# adding files and URLs (_urls vs. _url and _filenames vs. _filename in the
# test names).
#

def test_json_url(db, base_url):
    # archivebox add --parser=json "${SERVER}1.json"
    results = add_files_or_urls(base_url + '1.json', ['--parser=json'])
    expected = [
        base_url + '1.html',
    ]

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"

def test_json_urls(db, base_url):
    # archivebox add --parser=json "${SERVER}1.json" "${SERVER}2.json"
    results = add_files_or_urls([ base_url + '1.json', base_url + '2.json' ], ['--parser=json'])
    expected = [
        base_url + '1.html',
        base_url + '2.html',
    ]

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"

def test_json_filename(db, base_path, base_url):
    # archivebox add --parser=json "1.json"
    results = add_files_or_urls(base_path + '1.json', ['--parser=json'])
    expected = [
        base_url + '1.html',
    ]

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"

def test_json_filenames(db, base_path, base_url):
    # archivebox add --parser=json "1.json" "2.json"
    results = add_files_or_urls([ base_path + '1.json', base_path + '2.json' ], ['--parser=json'])
    expected = [
        base_url + '1.html',
        base_url + '2.html',
    ]

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"

def test_json_stdin_urls(db, base_url):
    # echo "${SERVER}1.json\n${SERVER}2.json" | archivebox add --depth=0 --parser=json
    urls = [ base_url + '1.json', base_url + '2.json' ]
    results = add_stdin("\n".join(urls), ['--parser=json'])
    expected = [
        base_url + '1.html',
        base_url + '2.html',
    ]

    print(results)
    dump_snapshot(db)

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"

def test_json_stdin_filenames(db, base_path, base_url):
    # echo "1.json\n2.json" | archivebox add --depth=0 --parser=json
    paths = [ base_path + '1.json', base_path + '2.json' ]
    results = add_stdin("\n".join(paths), [ '--parser=json' ])
    expected = [
        base_url + '1.html',
        base_url + '2.html',
    ]

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"

def test_json_stdin_json(db, base_path, base_url):
    # cat 1.json | archivebox add --depth=0 --parser=json
    results = add_stdin(open(base_path + '1.json', 'r').read(), [ '--parser=json' ])
    expected = [
        base_url + '1.html',
    ]

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"

def test_json_depth1_url(db, base_url):
    # archivebox add --depth=1 --parser=json "${SERVER}1.json"
    results = add_files_or_urls(base_url + '1.json', [ '--depth=1', '--parser=json' ])
    expected = [
        base_url + '1.html',
        base_url + '3.html',
    ]

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"

def test_json_depth1_urls(db, base_url):
    # archivebox add --depth=1 --parser=json "${SERVER}1.json" "${SERVER}2.json"
    urls = [ base_url + '1.json', base_url + '2.json' ]
    results = add_files_or_urls(urls, [ '--depth=1', '--parser=json' ])
    expected = [
        base_url + '1.html',
        base_url + '2.html',
        base_url + '3.html',
        base_url + '4.html',
    ]

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"

def test_json_depth1_filename(db, base_path, base_url):
    # archivebox add --depth=1 --parser=json 1.json
    results = add_files_or_urls(base_path + '1.json', ['--depth=1', '--parser=json'])
    expected = [
        base_url + '1.html',
        base_url + '3.html',
    ]

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"

def test_json_depth1_filenames(db, base_path, base_url):
    # archivebox add --depth=1 --parser=json 1.json 2.json
    results = add_files_or_urls(
        [ base_path + '1.json', base_path + '2.json' ],
        [ '--depth=1', '--parser=json' ]
    )
    expected = [
        base_url + '1.html',
        base_url + '2.html',
        base_url + '3.html',
        base_url + '4.html',
    ]

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"

def test_json_depth1_stdin_urls(db, base_url):
    # echo "${SERVER}1.json\n${SERVER}2.json" | archivebox add --depth=1 --parser=json
    urls = [ base_url + '1.json', base_url + '2.json' ]
    results = add_stdin("\n".join(urls), ['--depth=1', '--parser=json'])
    expected = [
        base_url + '1.html',
        base_url + '2.html',
        base_url + '3.html',
        base_url + '4.html',
    ]

    print(results)
    dump_snapshot(db)

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"

def test_json_depth1_stdin_filenames(db, base_path, base_url):
    # echo "1.json\n2.json" | archivebox add --depth=1 --parser=json
    paths = [ base_path + '1.json', base_path + '2.json' ]
    results = add_stdin("\n".join(paths), [ '--depth=1', '--parser=json' ])
    expected = [
        base_url + '1.html',
        base_url + '2.html',
        base_url + '3.html',
        base_url + '4.html',
    ]

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"

def test_json_depth1_stdin_contents(db, base_path, base_url):
    # cat 1.json | archivebox add --depth=1 --parser=json
    results = add_stdin(open(base_path + '1.json', 'r').read(), [ '--depth=1', '--parser=json' ])
    expected = [
        base_url + '1.html',
        base_url + '3.html',
    ]

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"
