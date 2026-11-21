"""Run against a dedicated Machbase 8.9 Standard lab database."""
import os

from machbaseAPI import connect


def main():
    connection = connect(
        host=os.getenv("M89_HOST", "127.0.0.1"),
        port=int(os.getenv("M89_PORT", "5656")),
        user=os.getenv("M89_USER", "SYS"),
        password=os.environ["M89_PASSWORD"],
    )
    ddl = connection.cursor()
    created = False
    try:
        ddl.execute("CREATE LOG TABLE M89_ARRAY_PY(ID INTEGER, A DOUBLE[65536])")
        created = True
        writer = connection.cursor(prepared=True)
        try:
            for length in (0, 1, 1024, 1025, 65536):
                values = [None if i % 3 == 1 else float(i) for i in range(length)]
                writer.execute("INSERT INTO M89_ARRAY_PY VALUES (?, ?)", (length, values))
            writer.execute("INSERT INTO M89_ARRAY_PY VALUES (?, ?)", (-1, None))
        finally:
            writer.close()
        ddl.execute("EXEC TABLE_FLUSH(M89_ARRAY_PY)")
        reader = connection.cursor(stream=True)
        try:
            reader.execute("SELECT ID,A FROM M89_ARRAY_PY ORDER BY ID")
            assert reader.fetchone_typed()["A"] is None
            for length in (0, 1, 1024, 1025, 65536):
                row = reader.fetchone_typed()
                value = row["A"]
                assert row["ID"] == value.actual_length == length
                assert value.declared_max_elements == 65536
                assert value.values == tuple(
                    None if i % 3 == 1 else float(i) for i in range(length)
                )
                assert tuple(value.null_mask) == tuple(i % 3 == 1 for i in range(length))
            assert reader.fetchone_typed() is None
        finally:
            reader.close()
        assert value.values[-1] == 65535.0
        print("PASS: NULL and all five ARRAY lengths")
    finally:
        try:
            if created:
                ddl.execute("DROP TABLE M89_ARRAY_PY")
        finally:
            ddl.close()
            connection.close()


if __name__ == "__main__":
    main()
