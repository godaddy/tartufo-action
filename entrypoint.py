#!/venv/bin/python
"""
Tartufo action executor
"""
import os
import subprocess
import sys
from typing import Optional

github_workspace = os.getenv("GITHUB_WORKSPACE")

input_mode: str = os.getenv("INPUT_MODE", "scan-local-repo")
input_entropy: str = os.getenv("INPUT_ENTROPY", "true")
input_regex: str = os.getenv("INPUT_REGEX", "true")
input_scan_filenames: str = os.getenv("INPUT_SCAN-FILENAMES", "true")
input_output_format: str = os.getenv("INPUT_OUTPUT-FORMAT", "text")
input_entropy_sensitivity: Optional[str] = os.getenv("INPUT_ENTROPY-SENSITIVITY")
input_branch: Optional[str] = os.getenv("INPUT_BRANCH")
input_include_submodules: str = os.getenv("INPUT_INCLUDE-SUBMODULE", "false")


os.chdir(github_workspace)  # type: ignore

run_arguments = ["/venv/bin/tartufo", input_mode, "."]


def process_global_args(
    entropy: str,
    regex: str,
    scan_filenames: str,
    output_format: str,
    entropy_sensitivity: Optional[str],
):
    """
    Process global tartufo arguments
    """
    options = []
    if entropy.lower() == "false":
        options.append("--no-entropy")
    if regex.lower() == "false":
        options.append("--no-regex")
    if scan_filenames.lower() == "false":
        options.append("--no-scan-filenames")
    if output_format.lower() != "text":
        options.append("--output-format")
        options.append(output_format)
    if entropy_sensitivity:
        options.append("--entropy-sensitivity")
        options.append(entropy_sensitivity)

    return options


def process_command_args(branch: Optional[str], include_submodules: str):
    """
    Process arguments specific to the scan-local-repo command
    """
    options = []
    if branch:
        options.append("--branch")
        options.append(branch)

    if include_submodules.lower() != "false":
        options.append("--include-submodules")

    return options


run_arguments[1:1] = process_global_args(
    input_entropy,
    input_regex,
    input_scan_filenames,
    input_output_format,
    input_entropy_sensitivity,
)

run_arguments[len(run_arguments) :] = process_command_args(
    input_branch, input_include_submodules
)

process = subprocess.run(run_arguments, check=False)

print(f"Tartufo secret scan completed with exit code {process.returncode}")

sys.exit(process.returncode)
