import os
from enum import Enum
from pathlib import Path
from typing import Optional

from prefect import flow, task
from prefect.blocks.system import Secret
from prefect_dbt.cli.commands import trigger_dbt_cli_command
from prefect_github import GitHubCredentials, GitHubRepository
from prefect_shell import shell_run_command


@task(name="Clone Prefect DBT Repo")
def clone_dbt_repo(destination_path: str, reference: str = "main"):
    dbt_repo_url = "https://github.com/PrefectHQ/prefect_dbt.git"
    github_credentials = GitHubCredentials.load("prefect-dbt-contents-ro-pat")
    repository = GitHubRepository(
        repository_url=dbt_repo_url, credentials=github_credentials, reference=reference
    )
    repository.get_directory(local_path=destination_path)


def get_dbt_paths(profiles_dir: str = "./dbt/.github", project_dir: str = "./dbt"):
    profiles_dir = str(Path(profiles_dir).resolve())
    project_dir = str(Path(project_dir).resolve())
    assert os.path.exists(f"{profiles_dir}/profiles.yml")
    return profiles_dir, project_dir


@task(name="Run Monte Carlo CLI Command")
def run_montecarlo_cli_cmd(
    name: str,
    command: str,
    cmd_env: dict,
):
    shell_run_command(
        command=command,
        env=cmd_env,
    )


def dbt_deps():
    """
    install dependencies
    """
    trigger_dbt_cli_command(
        command="dbt deps", project_dir="./dbt", profiles_dir="./dbt/.github"
    )


@task(name="dbt build")
def dbt_build(
    profiles_dir: str,
    project_dir: str,
    target: str = "dev",
    select: Optional[str] = None,
):
    """
    define dbt build task
    """
    extra_command_args = ["-t", target]
    if select:
        extra_command_args.extend(["-s", select])
    is_prd = target == "prod"
    trigger_dbt_cli_command(
        command="dbt build",
        profiles_dir=profiles_dir,
        project_dir=project_dir,
        return_state=True,
        create_summary_artifact=is_prd,
        summary_artifact_key=f"dbt-build-{target}-summary" if is_prd else None,
        extra_command_args=extra_command_args,
    )


def dbt_test(
    profiles_dir, project_dir, target: str = "dev", select: Optional[str] = None
):
    """
    define dbt test task
    """
    extra_command_args = ["-t", target]
    if select:
        extra_command_args.extend(["-s", select])
    is_prd = target == "prod"
    trigger_dbt_cli_command(
        command="dbt test",
        profiles_dir=profiles_dir,
        project_dir=project_dir,
        return_state=True,
        create_summary_artifact=is_prd,
        summary_artifact_key=f"dbt-test-{target}-summary" if is_prd else None,
        extra_command_args=extra_command_args,
    )


class DbtJob(Enum):
    BUILD = "build"
    TEST = "test"
    CI = "ci"
    RUN = "run"


class DbtTarget(Enum):
    DEV = "dev"
    PRD = "prod"
    CI = "ci"


def run_dbt_task(
    profiles_dir: str,
    project_dir: str,
    dbt_job: DbtJob = DbtJob.BUILD,
    target: DbtTarget = DbtTarget.DEV,
    select: Optional[str] = None,
):
    """
    select which task to run
    """
    if target == DbtTarget.DEV and "DBT_DEV_SCHEMA" not in os.environ:
        raise EnvironmentError(
            "DBT_DEV_SCHEMA environment variable not set for dbt target 'dev'"
        )
    if dbt_job == DbtJob.BUILD:
        dbt_build(
            target=target.value,
            select=select,
            profiles_dir=profiles_dir,
            project_dir=project_dir,
        )
    elif dbt_job == DbtJob.TEST:
        dbt_test(
            target=target.value,
            select=select,
            profiles_dir=profiles_dir,
            project_dir=project_dir,
        )
    elif dbt_job == DbtJob.CI:
        pass  # todo
    elif dbt_job == DbtJob.RUN:
        pass  # do we ever want to run a deployment without building?


@flow(name="dbt-runner")
def dbt_runner(
    dbt_job: DbtJob = DbtJob.BUILD,
    target: DbtTarget = DbtTarget.DEV,
    run_montecarlo: bool = False,
    select: Optional[str] = None,
    dbt_repo_branch: str = "main",
):
    """
    clone dbt repo and
    run dbt task with optional overrides
    """
    clone_dbt_repo(destination_path="./dbt", reference=dbt_repo_branch)
    profiles_dir, project_dir = get_dbt_paths()
    dbt_deps()
    run_dbt_task(
        dbt_job=dbt_job,
        profiles_dir=profiles_dir,
        project_dir=project_dir,
        target=target,
        select=select,
    )
    if run_montecarlo and target == DbtTarget.PRD:
        cmd_env = {
            "MCD_DEFAULT_API_ID": Secret.load("montecarlo-default-api-id").get(),
            "MCD_DEFAULT_API_TOKEN": Secret.load("montecarlo-default-api-token").get(),
        }
        # https://docs.getmontecarlo.com/docs/dbt-core#modify-your-production-dbt-cicd-workflow-%EF%B8%8F-updated
        # NOTE: the `--connection-id` is the BigQuery connection ID in Monte Carlo
        # as the `import dbt-run` command now requires that we specify which connection
        # to associate this metadata with, if we have >1 connections (which we do).
        # To obtain the connection UUID, locally run:
        # $ montecarlo integrations list
        run_montecarlo_cli_cmd(
            name="Monte Carlo: Upload DBT Metadata",
            command="""
            montecarlo import dbt-run \
                --manifest ./dbt/target/manifest.json \
                --run-results ./dbt/target/run_results.json \
                --project-name prefect-data-warehouse \
                --connection-id 704c5d70-900e-418f-92dd-a6243c661cac
""",
            cmd_env=cmd_env,
        )


if __name__ == "__main__":
    dbt_runner(
        dbt_job=DbtJob.TEST,
        target=DbtTarget.PRD,
        run_montecarlo=False,
        select="arr_running",
    )