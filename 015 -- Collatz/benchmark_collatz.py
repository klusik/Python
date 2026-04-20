import gc
import io
import json
import math
import os
import statistics
import tempfile
import time
import tracemalloc
from pathlib import Path

import klusik_collatz
import legacy_collatz


PROJECT_DIR = Path(__file__).resolve().parent
RESULTS_JSON = PROJECT_DIR / "benchmark_results.json"
REPORT_PDF = PROJECT_DIR / "benchmark_report.pdf"

SIZES = [100, 1_000, 5_000, 10_000]
REPEATS = 5


def legacy_generate(max_number):
    stdout = io.StringIO()
    original_stdout = os.sys.stdout
    os.sys.stdout = stdout
    try:
        return legacy_collatz.collatz(max_number)
    finally:
        os.sys.stdout = original_stdout


def optimized_generate(max_number):
    return [list(sequence) for _, sequence in klusik_collatz.collatz_sequences(max_number)]


def legacy_end_to_end(max_number):
    results = legacy_generate(max_number)
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as handle:
        output_path = Path(handle.name)
        for index, sequence in enumerate(results, start=1):
            handle.write(f"{index} (length = {len(sequence)}): {sequence}\n")
    output_path.unlink()


def optimized_end_to_end(max_number):
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as handle:
        output_path = Path(handle.name)
    try:
        klusik_collatz.write_output(max_number, output_path)
    finally:
        output_path.unlink(missing_ok=True)


def benchmark_callable(func, max_number, repeats):
    timings = []
    peak_memories = []

    for _ in range(repeats):
        gc.collect()
        tracemalloc.start()
        started = time.perf_counter()
        func(max_number)
        elapsed = time.perf_counter() - started
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        timings.append(elapsed)
        peak_memories.append(peak)

    return {
        "times": timings,
        "peak_memory_bytes": peak_memories,
        "mean_time_s": statistics.fmean(timings),
        "median_time_s": statistics.median(timings),
        "min_time_s": min(timings),
        "max_time_s": max(timings),
        "stdev_time_s": statistics.stdev(timings) if len(timings) > 1 else 0.0,
        "mean_peak_memory_bytes": statistics.fmean(peak_memories),
        "max_peak_memory_bytes": max(peak_memories),
    }


def validate_equivalence():
    for max_number in (5, 10, 25):
        legacy = legacy_generate(max_number)
        optimized = optimized_generate(max_number)
        if legacy != optimized:
            raise AssertionError(
                f"Mismatch detected for n={max_number}: legacy != optimized"
            )


def build_results():
    validate_equivalence()

    scenarios = {
        "generate_only": {
            "legacy": legacy_generate,
            "optimized": optimized_generate,
        },
        "end_to_end_write": {
            "legacy": legacy_end_to_end,
            "optimized": optimized_end_to_end,
        },
    }

    report = {
        "sizes": SIZES,
        "repeats": REPEATS,
        "scenarios": {},
    }

    for scenario_name, implementations in scenarios.items():
        scenario_results = {}
        for label, func in implementations.items():
            per_size = {}
            for size in SIZES:
                per_size[str(size)] = benchmark_callable(func, size, REPEATS)
            scenario_results[label] = per_size
        report["scenarios"][scenario_name] = scenario_results

    return report


def speedup(a, b):
    return a / b if b else math.inf


class PdfCanvas:
    def __init__(self):
        self.pages = []

    def add_page(self, commands):
        self.pages.append(commands)

    def save(self, path):
        objects = []

        def add_object(data):
            objects.append(data)
            return len(objects)

        font_id = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        page_ids = []

        for commands in self.pages:
            stream = commands.encode("latin-1")
            content_id = add_object(
                f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1")
                + stream
                + b"\nendstream"
            )
            page_id = add_object(
                (
                    "<< /Type /Page /Parent PAGES_ID 0 R /MediaBox [0 0 612 792] "
                    f"/Resources << /Font << /F1 {font_id} 0 R >> >> "
                    f"/Contents {content_id} 0 R >>"
                ).encode("latin-1")
            )
            page_ids.append(page_id)

        kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
        pages_id = add_object(
            f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("latin-1")
        )
        catalog_id = add_object(f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("latin-1"))

        rendered = []
        for obj in objects:
            rendered.append(obj.replace(b"PAGES_ID", str(pages_id).encode("latin-1")))

        buffer = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]

        for index, obj in enumerate(rendered, start=1):
            offsets.append(len(buffer))
            buffer.extend(f"{index} 0 obj\n".encode("latin-1"))
            buffer.extend(obj)
            buffer.extend(b"\nendobj\n")

        xref_offset = len(buffer)
        buffer.extend(f"xref\n0 {len(rendered) + 1}\n".encode("latin-1"))
        buffer.extend(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            buffer.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))

        buffer.extend(
            (
                f"trailer\n<< /Size {len(rendered) + 1} /Root {catalog_id} 0 R >>\n"
                f"startxref\n{xref_offset}\n%%EOF\n"
            ).encode("latin-1")
        )

        path.write_bytes(buffer)


def escape_pdf_text(text):
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def text_line(x, y, text, size=12):
    escaped = escape_pdf_text(text)
    return f"BT /F1 {size} Tf 1 0 0 1 {x:.2f} {y:.2f} Tm ({escaped}) Tj ET\n"


def rect(x, y, width, height, fill=False):
    operator = "B" if fill else "S"
    return f"{x:.2f} {y:.2f} {width:.2f} {height:.2f} re {operator}\n"


def line(x1, y1, x2, y2):
    return f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S\n"


def rgb(r, g, b):
    return f"{r:.3f} {g:.3f} {b:.3f} rg {r:.3f} {g:.3f} {b:.3f} RG\n"


def draw_bar_chart(title, data_pairs, x, y, width, height, left_label, right_label):
    commands = [text_line(x, y + height + 28, title, 14)]
    commands.append(rgb(0.2, 0.2, 0.2))
    commands.append(rect(x, y, width, height))

    all_values = [value for _, pair in data_pairs for value in pair]
    max_value = max(all_values) if all_values else 1.0
    inner_left = x + 50
    inner_bottom = y + 35
    inner_width = width - 70
    inner_height = height - 55
    commands.append(line(inner_left, inner_bottom, inner_left, inner_bottom + inner_height))
    commands.append(line(inner_left, inner_bottom, inner_left + inner_width, inner_bottom))

    group_width = inner_width / max(len(data_pairs), 1)
    bar_width = group_width * 0.28

    for index, (label, pair) in enumerate(data_pairs):
        group_x = inner_left + (index * group_width) + (group_width * 0.18)
        commands.append(text_line(group_x - 4, y + 12, label, 9))
        for pair_index, value in enumerate(pair):
            bar_x = group_x + (pair_index * (bar_width + 8))
            bar_height = 0 if max_value == 0 else (value / max_value) * (inner_height - 10)
            color = (0.77, 0.31, 0.24) if pair_index == 0 else (0.16, 0.47, 0.71)
            commands.append(rgb(*color))
            commands.append(rect(bar_x, inner_bottom, bar_width, bar_height, fill=True))

    commands.append(rgb(0.77, 0.31, 0.24))
    commands.append(rect(x + width - 145, y + height - 18, 10, 10, fill=True))
    commands.append(text_line(x + width - 130, y + height - 20, left_label, 9))
    commands.append(rgb(0.16, 0.47, 0.71))
    commands.append(rect(x + width - 72, y + height - 18, 10, 10, fill=True))
    commands.append(text_line(x + width - 57, y + height - 20, right_label, 9))
    commands.append(rgb(0.2, 0.2, 0.2))

    for tick in range(5):
        tick_value = max_value * tick / 4 if max_value else 0
        tick_y = inner_bottom + (inner_height * tick / 4)
        commands.append(line(inner_left - 4, tick_y, inner_left, tick_y))
        commands.append(text_line(x + 6, tick_y - 3, f"{tick_value:.3f}", 8))

    return "".join(commands)


def draw_speedup_chart(title, data_points, x, y, width, height):
    commands = [text_line(x, y + height + 28, title, 14)]
    commands.append(rgb(0.2, 0.2, 0.2))
    commands.append(rect(x, y, width, height))

    max_value = max((value for _, value in data_points), default=1.0)
    inner_left = x + 50
    inner_bottom = y + 35
    inner_width = width - 70
    inner_height = height - 55
    commands.append(line(inner_left, inner_bottom, inner_left, inner_bottom + inner_height))
    commands.append(line(inner_left, inner_bottom, inner_left + inner_width, inner_bottom))

    step = inner_width / max(len(data_points), 1)
    previous = None

    for index, (label, value) in enumerate(data_points):
        point_x = inner_left + (index + 0.5) * step
        point_y = inner_bottom + ((value / max_value) * (inner_height - 10) if max_value else 0)
        if previous is not None:
            commands.append(rgb(0.16, 0.47, 0.71))
            commands.append(line(previous[0], previous[1], point_x, point_y))
        commands.append(rgb(0.16, 0.47, 0.71))
        commands.append(rect(point_x - 2, point_y - 2, 4, 4, fill=True))
        commands.append(text_line(point_x - 14, y + 12, label, 9))
        commands.append(text_line(point_x - 10, point_y + 8, f"{value:.2f}x", 8))
        previous = (point_x, point_y)

    commands.append(rgb(0.2, 0.2, 0.2))
    for tick in range(5):
        tick_value = max_value * tick / 4 if max_value else 0
        tick_y = inner_bottom + (inner_height * tick / 4)
        commands.append(line(inner_left - 4, tick_y, inner_left, tick_y))
        commands.append(text_line(x + 6, tick_y - 3, f"{tick_value:.2f}x", 8))

    return "".join(commands)


def render_report(results, path):
    canvas = PdfCanvas()

    generate_scenario = results["scenarios"]["generate_only"]
    write_scenario = results["scenarios"]["end_to_end_write"]
    sizes = results["sizes"]

    def scenario_summary(scenario):
        speedups = []
        memory_savings = []
        for size in sizes:
            size_key = str(size)
            legacy_time = scenario["legacy"][size_key]["mean_time_s"]
            optimized_time = scenario["optimized"][size_key]["mean_time_s"]
            legacy_mem = scenario["legacy"][size_key]["mean_peak_memory_bytes"]
            optimized_mem = scenario["optimized"][size_key]["mean_peak_memory_bytes"]
            speedups.append(speedup(legacy_time, optimized_time))
            memory_savings.append(legacy_mem / optimized_mem if optimized_mem else math.inf)
        return statistics.fmean(speedups), statistics.fmean(memory_savings)

    gen_speedup_mean, gen_memory_mean = scenario_summary(generate_scenario)
    write_speedup_mean, write_memory_mean = scenario_summary(write_scenario)

    page1 = []
    page1.append(text_line(50, 748, "Collatz Optimization Benchmark Report", 22))
    page1.append(text_line(50, 722, "Project: 015 -- Collatz", 12))
    page1.append(text_line(50, 706, "Benchmark date: 2026-04-20", 12))
    page1.append(text_line(50, 682, "Methodology", 16))
    methodology = [
        f"Compared original legacy implementation against the optimized implementation.",
        f"Validated identical sequence output for n=5, 10, and 25 before measuring.",
        f"Measured with time.perf_counter and tracemalloc using {results['repeats']} runs per input size.",
        f"Input sizes: {', '.join(str(size) for size in sizes)}.",
        "Scenarios: generation only, and end-to-end generation plus output file writing.",
    ]
    y = 660
    for line_text in methodology:
        page1.append(text_line(60, y, line_text, 11))
        y -= 16
    page1.append(text_line(50, 560, "Top-line Findings", 16))
    findings = [
        f"Generation-only average speedup: {gen_speedup_mean:.2f}x.",
        f"Generation-only average memory reduction factor: {gen_memory_mean:.2f}x.",
        f"End-to-end average speedup: {write_speedup_mean:.2f}x.",
        f"End-to-end average memory reduction factor: {write_memory_mean:.2f}x.",
    ]
    y = 538
    for line_text in findings:
        page1.append(text_line(60, y, line_text, 11))
        y -= 16

    bar_data = []
    for size in sizes:
        size_key = str(size)
        bar_data.append(
            (
                str(size),
                (
                    generate_scenario["legacy"][size_key]["mean_time_s"],
                    generate_scenario["optimized"][size_key]["mean_time_s"],
                ),
            )
        )
    page1.append(
        draw_bar_chart(
            "Generation Runtime by Input Size (seconds)",
            bar_data,
            50,
            250,
            510,
            220,
            "Legacy",
            "Optimized",
        )
    )
    canvas.add_page("".join(page1))

    page2 = []
    write_bar_data = []
    write_speedups = []
    memory_bar_data = []
    for size in sizes:
        size_key = str(size)
        write_bar_data.append(
            (
                str(size),
                (
                    write_scenario["legacy"][size_key]["mean_time_s"],
                    write_scenario["optimized"][size_key]["mean_time_s"],
                ),
            )
        )
        write_speedups.append(
            (
                str(size),
                speedup(
                    write_scenario["legacy"][size_key]["mean_time_s"],
                    write_scenario["optimized"][size_key]["mean_time_s"],
                ),
            )
        )
        memory_bar_data.append(
            (
                str(size),
                (
                    generate_scenario["legacy"][size_key]["mean_peak_memory_bytes"] / (1024 * 1024),
                    generate_scenario["optimized"][size_key]["mean_peak_memory_bytes"] / (1024 * 1024),
                ),
            )
        )
    page2.append(
        draw_bar_chart(
            "End-to-End Runtime by Input Size (seconds)",
            write_bar_data,
            50,
            500,
            510,
            210,
            "Legacy",
            "Optimized",
        )
    )
    page2.append(
        draw_speedup_chart(
            "End-to-End Speedup (legacy / optimized)",
            write_speedups,
            50,
            250,
            510,
            180,
        )
    )
    page2.append(
        draw_bar_chart(
            "Generation Peak Memory by Input Size (MiB)",
            memory_bar_data,
            50,
            20,
            510,
            180,
            "Legacy",
            "Optimized",
        )
    )
    canvas.add_page("".join(page2))

    page3 = []
    page3.append(text_line(50, 748, "Detailed Results", 18))
    y = 722
    headers = [
        "Scenario",
        "n",
        "Legacy mean s",
        "Optimized mean s",
        "Speedup",
        "Legacy peak MiB",
        "Optimized peak MiB",
    ]
    positions = [50, 150, 190, 290, 410, 470, 555]
    for position, header in zip(positions, headers):
        page3.append(text_line(position, y, header, 9))
    y -= 14
    scenarios = [
        ("generate", generate_scenario),
        ("write", write_scenario),
    ]
    for scenario_label, scenario in scenarios:
        for size in sizes:
            size_key = str(size)
            legacy = scenario["legacy"][size_key]
            optimized = scenario["optimized"][size_key]
            row = [
                scenario_label,
                str(size),
                f"{legacy['mean_time_s']:.6f}",
                f"{optimized['mean_time_s']:.6f}",
                f"{speedup(legacy['mean_time_s'], optimized['mean_time_s']):.2f}x",
                f"{legacy['mean_peak_memory_bytes'] / (1024 * 1024):.3f}",
                f"{optimized['mean_peak_memory_bytes'] / (1024 * 1024):.3f}",
            ]
            for position, cell in zip(positions, row):
                page3.append(text_line(position, y, cell, 8))
            y -= 12
    y -= 12
    notes = [
        "Interpretation",
        "The optimized version wins by removing the giant in-memory results list during normal writing,",
        "by caching previously discovered Collatz suffixes, and by using cheaper parity and division operations.",
        "Memory drops most sharply in the end-to-end path because output is streamed directly to disk.",
        "The original parity helper is misnamed, but its control flow still produces the expected operations.",
        "The optimized version preserves the original special-case output for the starting value 1.",
    ]
    for index, line_text in enumerate(notes):
        page3.append(text_line(50, y, line_text, 12 if index == 0 else 10))
        y -= 16
    canvas.add_page("".join(page3))

    canvas.save(path)


def main():
    results = build_results()
    RESULTS_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")
    render_report(results, REPORT_PDF)
    print(f"Wrote benchmark data to {RESULTS_JSON}")
    print(f"Wrote PDF report to {REPORT_PDF}")


if __name__ == "__main__":
    main()
