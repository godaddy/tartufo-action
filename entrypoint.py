#!/venv/bin/python

import os
import subprocess
import sys

github_event_path = os.getenv("GITHUB_EVENT_PATH")
github_repository = os.getenv("GITHUB_REPOSITORY")
github_workspace = os.getenv("GITHUB_WORKSPACE", None)

entropy = os.getenv("INPUT_ENTROPY")
regex = os.getenv("INPUT_REGEX")
scan_filenames = os.getenv("INPUT_SCAN-FILENAMES")
output_format = os.getenv("INPUT_OUTPUT-FORMAT")
include_submodules = os.getenv("INPUT_INCLUDE-SUBMODULE")
current_branch = os.getenv("INPUT_CURRENT-BRANCH")


def branch_name(github_event):
    if "ref" in github_event.keys():
        return [
            "--branch",
            github_event["ref"],
        ]
    elif "pull_request" in github_event.keys():
        return [
            "--branch",
            github_event["pull_request"]["head"]["ref"],
        ]
    return []


os.chdir(github_workspace)  # type: ignore

run_arguments = ["/venv/bin/tartufo", "scan-local-repo", "."]


def process_global_args(entropy, regex, scan_filenames, output_format):
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

    return options


def process_command_args(current_branch, include_submodules):
    options = []
    if current_branch.lower() == "false":
        options.append("--branch")
        event_name = os.getenv("GITHUB_EVENT_NAME")
        if event_name == "pull_request":
            branch = os.getenv("GITHUB_HEAD_REF")
        else:
            branch = os.getenv("GITHUB_REF_NAME")
        options.append(branch)
    if include_submodules:
        options.append("--include-submodules")

    return options


run_arguments[1:1] = process_global_args(entropy, regex, scan_filenames, output_format)

run_arguments[len(run_arguments) :] = process_command_args(
    current_branch, include_submodules
)

process = subprocess.run(run_arguments)

print(f"Tartufo secret scan completed with exit code {process.returncode}")

sys.exit(process.returncode)
