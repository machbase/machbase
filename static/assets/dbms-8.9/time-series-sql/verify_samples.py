"""전용 실습 DB에서 setup → 모든 SQL → prepared 재실행 → cleanup을 검증합니다."""
import argparse
import json
import math
import os
import re
import time
from pathlib import Path


def split_sql(text):
    statements, current = [], []
    quoted = False
    index = 0
    while index < len(text):
        char = text[index]
        if not quoted and text[index:index + 2] == '--':
            end = text.find('\n', index)
            index = len(text) if end < 0 else end
            continue
        current.append(char)
        if char == "'":
            if quoted and index + 1 < len(text) and text[index + 1] == "'":
                current.append("'")
                index += 1
            else:
                quoted = not quoted
        elif char == ';' and not quoted:
            statements.append(''.join(current).strip())
            current = []
        index += 1
    if ''.join(current).strip():
        statements.append(''.join(current).strip())
    if quoted:
        raise ValueError('SQL 문자열의 따옴표가 닫히지 않았습니다')
    return statements


def equivalent(actual, expected):
    if expected is None:
        return actual is None
    if isinstance(expected, list):
        return isinstance(actual, (tuple, list)) and len(actual) == len(expected) and all(
            equivalent(a, b) for a, b in zip(actual, expected))
    if isinstance(expected, (int, float)) and not isinstance(expected, bool):
        try:
            return math.isclose(float(actual), float(expected), rel_tol=1e-10, abs_tol=1e-9)
        except (ValueError, TypeError):
            return False
    return actual == expected


def check_result(case, rows):
    if case['expected'] is not None:
        assert equivalent(rows, case['expected']), (rows, case['expected'])
    checks = case.get('checks', {})
    if 'row_count' in checks:
        assert len(rows) == checks['row_count'], len(rows)
    if 'last_values' in checks:
        assert equivalent([r[-1] for r in rows], checks['last_values']), rows
    if 'ids' in checks:
        assert [r[0] for r in rows] == checks['ids'], rows
        assert equivalent([r[checks['value_column']] for r in rows], checks['values']), rows
    if 'time_ns' in checks:
        assert [r[3] for r in rows] == checks['time_ns'], rows
    if 'data_prefix' in checks:
        assert equivalent([list(r[:-1]) for r in rows], checks['data_prefix']), rows
    if 'provenance' in checks:
        for row in rows:
            data = json.loads(row[-1])
            assert data['version'] == 1 and len(data['sources']) == 2, data
            source, wanted = data['sources'][1], checks['provenance']
            if wanted.get('unmatched'):
                assert source['selected'] is None, source
            if 'selected_time' in wanted:
                endpoint = source['selected']
                assert endpoint['timestamp_ns'] == str(wanted['selected_time']), endpoint
                assert endpoint['delta_ns'] == wanted['delta'], endpoint
                if 'selected_id' in wanted:
                    assert str(endpoint['id'][0]['value']) == str(wanted['selected_id']), endpoint
                if 'clock_domain' in wanted:
                    assert endpoint['clock_domain'] == wanted['clock_domain'], endpoint
            if 'left_time' in wanted:
                assert source['left']['timestamp_ns'] == str(wanted['left_time']), source
                assert source['right']['timestamp_ns'] == str(wanted['right_time']), source


def query(connection, sql, params=None, cursor=None):
    own = cursor is None
    cur = cursor or connection.cursor(dictionary=False)
    try:
        cur.execute(sql, params) if params is not None else cur.execute(sql)
        rows = cur.fetchall()
        columns = [c[0] for c in cur.description] if cur.description else []
        return rows, columns
    finally:
        if own:
            cur.close()


def prepared_checks(connection, base_ns):
    checks = []
    sql = '''SELECT e.ID,m.ID FROM TS13_EVENT e ASOF JOIN TS13_MOTOR m
             ON e.NAME=m.NAME TOLERANCE (?) ORDER BY e.ID'''
    cur = connection.cursor(prepared=True, dictionary=False)
    try:
        for ns, expected in [(0, [104, None, 111, None, None, None]),
                             (5000000000, [104, 107, 111, 114, 116, None]),
                             (0, [104, None, 111, None, None, None])]:
            rows, _ = query(connection, sql, [ns], cur)
            assert [r[1] for r in rows] == expected, rows
            checks.append({'kind': 'tolerance', 'ns': ns, 'rows': rows})
    finally:
        cur.close()
    sql = '''SELECT TIME,AVG(VALUE) AS V FROM TS13_FILL WHERE NAME='A'
             SAMPLE BY 1s FROM FROM_TIMESTAMP(?) TO FROM_TIMESTAMP(?) FILL(NULL)'''
    cur = connection.cursor(prepared=True, dictionary=False)
    try:
        for start, end, count in [(0, 6, 6), (2, 2, 0), (0, 6, 6)]:
            rows, _ = query(connection, sql, [base_ns + start * 10**9, base_ns + end * 10**9], cur)
            assert len(rows) == count, rows
            if count:
                assert equivalent([r[1] for r in rows], [20, None, 24, None, None, 30]), rows
            checks.append({'kind': 'sample_bounds', 'count': count})
    finally:
        cur.close()
    sql = '''SELECT ID,SUM(VALUE) OVER(ORDER BY TIME,ID
             ROWS BETWEEN ? PRECEDING AND CURRENT ROW) AS V
             FROM TS13_MOTOR WHERE NAME='edu27_main' ORDER BY ID'''
    cur = connection.cursor(prepared=True, dictionary=False)
    try:
        for width, first_three in [(0, [0, 16, 64]), (1, [0, 16, 80]), (0, [0, 16, 64])]:
            rows, _ = query(connection, sql, [width], cur)
            assert [r[1] for r in rows[:3]] == first_three and len(rows) == 18, rows
            checks.append({'kind': 'rows_frame', 'width': width, 'count': len(rows)})
    finally:
        cur.close()
    checks.extend(dynamic_pivot_checks(connection))
    return checks


def dynamic_pivot_checks(connection):
    created = False
    prepared = None
    results = []
    try:
        query(connection, 'CREATE LOG TABLE TS13_DYNAMIC(K INTEGER,V INTEGER)')
        created = True
        query(connection, 'INSERT INTO TS13_DYNAMIC VALUES(1,10)')
        query(connection, 'INSERT INTO TS13_DYNAMIC VALUES(2,20)')
        query(connection, 'EXEC TABLE_FLUSH(TS13_DYNAMIC)')
        sql = ('SELECT * FROM (SELECT K,V FROM TS13_DYNAMIC) '
               'PIVOT(SUM(V) FOR K IN(SELECT DISTINCT K FROM TS13_DYNAMIC ORDER BY K))')
        prepared = connection.cursor(prepared=True, dictionary=False)
        rows, cols = query(connection, sql, cursor=prepared)
        assert equivalent(rows, [[10, 20]]) and len(cols) == 2, (rows, cols)
        results.append({'kind': 'pivot_initial', 'columns': cols, 'rows': rows})
        query(connection, 'INSERT INTO TS13_DYNAMIC VALUES(3,30)')
        query(connection, 'EXEC TABLE_FLUSH(TS13_DYNAMIC)')
        rows, cols = query(connection, sql, cursor=prepared)
        assert equivalent(rows, [[10, 20]]) and len(cols) == 2, (rows, cols)
        results.append({'kind': 'pivot_same_prepare', 'columns': cols, 'rows': rows})
        prepared.close()
        prepared = connection.cursor(prepared=True, dictionary=False)
        rows, cols = query(connection, sql, cursor=prepared)
        assert equivalent(rows, [[10, 20, 30]]) and len(cols) == 3, (rows, cols)
        results.append({'kind': 'pivot_reprepare', 'columns': cols, 'rows': rows})
    finally:
        if prepared is not None:
            prepared.close()
        if created:
            query(connection, 'DROP TABLE TS13_DYNAMIC')
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5656)
    parser.add_argument('--user', default='SYS')
    parser.add_argument('--password-env', default='TS_SQL_PASSWORD')
    parser.add_argument('--output', default='verification-results.json')
    args = parser.parse_args()
    from machbaseAPI import connect
    password = os.environ[args.password_env]
    folder = Path(__file__).resolve().parent
    cases = json.loads((folder / 'examples.json').read_text())
    fixtures = json.loads((folder / 'fixtures.json').read_text())
    connection = connect(host=args.host, port=args.port, user=args.user, password=password)
    created, results, prepared, setup_error = [], [], [], None
    try:
        for sql in split_sql((folder / 'setup.sql').read_text()):
            query(connection, sql)
            match = re.match(r'CREATE (?:TAG|LOG|TRANSACTION) TABLE (\w+)', sql, re.I)
            if match:
                created.append(match[1])
        deadline = time.monotonic() + 20
        for table, expected in fixtures['expected_counts'].items():
            while True:
                actual = query(connection, 'SELECT COUNT(*) FROM ' + table)[0][0][0]
                if actual == expected:
                    break
                if actual > expected or time.monotonic() > deadline:
                    raise AssertionError((table, actual, expected))
                time.sleep(0.1)
        for index, case in enumerate(cases, 1):
            path = folder / case['file']
            sql = path.read_text().strip()
            assert sql == case['sql'].strip(), str(path)
            result = {'index': index, 'topic': case['topic'], 'title': case['title'],
                      'file': case['file']}
            try:
                rows, columns = query(connection, sql)
                if case['error']:
                    raise AssertionError('오류가 예상되는 SQL이 정상 종료했습니다')
                check_result(case, rows)
                result.update(status='PASS', rows=rows, columns=columns)
            except Exception as exc:
                if case['error'] and not isinstance(exc, AssertionError) and re.search(case['error'], str(exc), re.I):
                    result.update(status='EXPECTED_ERROR', error=str(exc))
                    assert query(connection, 'SELECT 1 AS N')[0][0][0] == 1
                else:
                    result.update(status='FAIL', error=str(exc))
            results.append(result)
            print(f'{index:03d} {result["status"]}: {case["topic"]} / {case["title"]}', flush=True)
        if all(r['status'] != 'FAIL' for r in results):
            prepared = prepared_checks(connection, fixtures['base_ns'])
    except Exception as exc:
        setup_error = str(exc)
    finally:
        for table in reversed(created):
            try:
                query(connection, 'DROP TABLE ' + table)
            except Exception as exc:
                results.append({'status': 'CLEANUP_FAIL', 'table': table, 'error': str(exc)})
        connection.close()
    report = {'setup_error': setup_error, 'results': results, 'prepared_checks': prepared,
              'expected_cases': len(cases), 'cleanup_tables': created}
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    failures = [r for r in results if r['status'] not in ('PASS', 'EXPECTED_ERROR')]
    if setup_error or failures or len(results) != len(cases):
        raise SystemExit(f'검증 실패: setup={setup_error}, failures={len(failures)}')
    print(f'PASS: {len(results)} SQL examples, {len(prepared)} prepared executions; cleanup complete')


if __name__ == '__main__':
    main()
