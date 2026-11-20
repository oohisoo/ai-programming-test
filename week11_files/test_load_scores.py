import csv

import pytest

from load_scores import load_scores


def write_csv(path, rows, encoding="utf-8"):
    with path.open("w", encoding=encoding, newline="") as file:
        csv.writer(file).writerows(rows)
    return path


def test_header_only_returns_empty_lists(tmp_path):
    path = write_csv(tmp_path / "header_only.csv", [["name", "score"]])

    assert load_scores(path) == ([], [])


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_duplicate_name_keeps_first_valid_row(tmp_path):
    path = write_csv(
        tmp_path / "valid.csv",
        [
            ["name", "score"],
            ["김하나", "88"],
            ["김하나", "91"],
            ["  박세찬  ", "72"],
        ],
    )

    assert load_scores(path) == (
        [("김하나", 88), ("박세찬", 72)],
        [(3, "김하나,91", "중복된 이름")],
    )


@pytest.mark.parametrize("score", [0, 100])
def test_score_boundary_values_are_kept(tmp_path, score):
    path = write_csv(
        tmp_path / f"boundary_{score}.csv",
        [["name", "score"], ["경계학생", str(score)]],
    )

    assert load_scores(path) == ([("경계학생", score)], [])


@pytest.mark.parametrize(
    ("row", "reason"),
    [
        (["한셀만"], "열 개수가 2가 아님"),
        (["세", "칸", "추가"], "열 개수가 2가 아님"),
        (["", "90"], "이름이 비어 있음"),
        (["윤보람", ""], "점수가 비어 있음"),
        (["한겨울", "결석"], "점수가 정수가 아님"),
        (["정오름", "-1"], "점수가 0~100 밖"),
        (["이두리", "101"], "점수가 0~100 밖"),
    ],
)
def test_invalid_rows_are_skipped_with_reason(tmp_path, row, reason):
    path = write_csv(tmp_path / "invalid.csv", [["name", "score"], row])

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [(2, ",".join(row), reason)]


def test_blank_line_is_skipped_without_record(tmp_path):
    path = write_csv(
        tmp_path / "blank.csv",
        [["name", "score"], [], ["윤보람", "64"]],
    )

    assert load_scores(path) == ([("윤보람", 64)], [])


def test_mixed_file_records_invalid_lines_and_keeps_valid_lines(tmp_path):
    path = write_csv(
        tmp_path / "mixed.csv",
        [
            ["name", "score"],
            ["김하나", "88"],
            ["이두리", "105"],
            ["박세찬", ""],
            ["장미르", "72", "비고없음"],
            ["한겨울", "결석"],
            ["서한별", "95"],
        ],
    )

    assert load_scores(path) == (
        [("김하나", 88), ("서한별", 95)],
        [
            (3, "이두리,105", "점수가 0~100 밖"),
            (4, "박세찬,", "점수가 비어 있음"),
            (5, "장미르,72,비고없음", "열 개수가 2가 아님"),
            (6, "한겨울,결석", "점수가 정수가 아님"),
        ],
    )


def test_utf8_bom_header_is_read_without_bom(tmp_path):
    path = write_csv(
        tmp_path / "bom.csv",
        [["name", "score"], ["서한별", "95"]],
        encoding="utf-8-sig",
    )

    assert load_scores(path) == ([("서한별", 95)], [])
