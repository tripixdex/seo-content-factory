"""Tests for batch ordering guarantees."""

from __future__ import annotations

import csv
from pathlib import Path

from seo_factory.pipeline.batch_runner import run_batch_from_csv


def test_batch_summary_preserves_csv_order(tmp_path: Path) -> None:
    csv_path = tmp_path / "batch.csv"
    csv_path.write_text(
        "\n".join(
            [
                "job_id,source_path,target_keyword",
                "item_001,fixtures/pages/demo_b_1.html,automated seo reporting",
                "item_002,fixtures/pages/demo_b_2.html,technical seo audits",
                "item_003,fixtures/pages/demo_b_3.html,content workflow automation",
            ]
        ),
        encoding="utf-8",
    )

    summary_path = run_batch_from_csv(csv_path, "test-run", Path("outputs/test_batch_order/out"))
    with summary_path.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert [row["row_id"] for row in rows] == ["1", "2", "3"]
    assert [row["job_id"] for row in rows] == ["item_001", "item_002", "item_003"]
