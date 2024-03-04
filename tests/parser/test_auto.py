from .fixtures import *

# Next five tests are the first ones from:
#   https://github.com/ArchiveBox/ArchiveBox/issues/1363#issuecomment-1966177173
# (The defaults are --parser=auto and --depth=0.)
#
# The rest of the tests that test specifying the parser are in ./test_specific.py
#
def test_add_urls(db):
    # archivebox add 'https://example.com' 'https://example.org'
    expected = [
        'https://example.com',
        'https://example.org',
    ]
    results = add_files_or_urls(expected)

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"

def test_add_stdin_urls(db):
    # echo -e"https://example.com\nhttps://example.org" | archivebox add --depth=0
    expected = [
        'https://example.com',
        'https://example.org',
    ]
    results = add_stdin("\n".join(expected))

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"

def test_add_stdin_json(db, base_path):
    # cat example.json | archivebox add --depth=0
    results = add_stdin(open(base_path + 'example.json','r').read())

    expected = [
        'http://127.0.0.1:8080/static/title_og_with_html',
        'http://127.0.0.1:8080/static/shift_jis.html',
        'http://127.0.0.1:8080/static/iana.org.html',
        'http://127.0.0.1:8080/static/example.com.html',
    ]
    unexpected = [
        'http://www.example.com/should-not-exist',
    ]

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"
    for url in unexpected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 0, f"{url} was not expected to be found"
    assert db.execute("SELECT COUNT(*) FROM core_tag").fetchone()[0] == 6

def test_add_file_json(db, base_path):
    # archivebox add --depth=0 example.json
    results = add_files_or_urls(base_path + 'example.json')

    expected = [
        'http://127.0.0.1:8080/static/title_og_with_html',
        'http://127.0.0.1:8080/static/shift_jis.html',
        'http://127.0.0.1:8080/static/iana.org.html',
        'http://127.0.0.1:8080/static/example.com.html',
    ]
    unexpected = [
        'http://www.example.com/should-not-exist',
    ]

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"
    for url in unexpected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 0, f"{url} was not expected to be found"
    assert db.execute("SELECT COUNT(*) FROM core_tag").fetchone()[0] == 6

def test_add_stdin_file_json(db, base_path):
    # echo 'example.json' | archivebox add --depth=0

    data= base_path + 'example.json'

    results = add_stdin(data)

    expected = [
        'http://127.0.0.1:8080/static/title_og_with_html',
        'http://127.0.0.1:8080/static/shift_jis.html',
        'http://127.0.0.1:8080/static/iana.org.html',
        'http://127.0.0.1:8080/static/example.com.html',
    ]
    unexpected = [
        'http://www.example.com/should-not-exist',
    ]

    assert db.execute("SELECT COUNT(*) FROM core_snapshot").fetchone()[0] == len(expected)
    for url in expected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 1, f"{url} not found, even though it was expected"
    for url in unexpected:
        assert db.execute("SELECT COUNT(*) FROM core_snapshot WHERE url = ?", (url,)).fetchone()[0] == 0, f"{url} was not expected to be found"
    assert db.execute("SELECT COUNT(*) FROM core_tag").fetchone()[0] == 6
