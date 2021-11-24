#!/venv/bin/python

import os
import subprocess
import sys

github_event_path = os.getenv("GITHUB_EVENT_PATH")
github_repository = os.getenv("GITHUB_REPOSITORY")
github_workspace = os.getenv("GITHUB_WORKSPACE")

entropy = os.getenv("INPUT_ENTROPY")
regex = os.getenv("INPUT_REGEX")
scan_filenames = os.getenv('INPUT_SCAN-FILENAMES')
output_format = os.getenv('INPUT_OUTPUT-FORMAT')
b64_entropy_score = os.getenv('INPUT_B64-ENTROPY-SCORE')
hex_entropy_score = os.getenv('INPUT_HEX-ENTROPY-SCORE')
include_submodules = os.getenv('INPUT_INCLUDE-SUBMODULE')
current_branch = os.getenv('INPUT_CURRENT-BRANCH')


def push_arguments(github_event):
    if "ref" in github_event.keys() and "before" in github_event.keys():
        return [
            "--branch",
            github_event["ref"],
            "--since-commit",
            github_event["before"],
        ]
    return []


def pr_arguments(github_event):
    if "pull_request" in github_event.keys():
        return [
            "--branch",
            github_event["pull_request"]["head"]["ref"],
            "--max-depth",
            str(github_event["pull_request"]["commits"]),
        ]
    return []


os.chdir(github_workspace)

run_arguments = ["/venv/bin/tartufo", "scan-local-repo"]


def process_global_args(entropy, regex, scan_filenames, output_format, b64_entropy_score, hex_entropy_score):
    options = []
    if entropy.lower() == "false":
        options.append('--no-entropy')
    if regex.lower() == "false":
        options.append('--no-regex')
    if scan_filenames.lower() == "false":
        options.append('--no-scan-filenames')
    options.append(
        f'--output-format {output_format} --b64-entropy-score {b64_entropy_score} --hex-entropy-score {hex_entropy_score}')

    return options


run_arguments[1:1] = process_global_args(entropy, regex, scan_filenames, output_format, b64_entropy_score,
                                         hex_entropy_score)

process = subprocess.run(run_arguments)

print(f"Tartufo secret scan completed with exit code {process.returncode}")

sys.exit(process.returncode)
