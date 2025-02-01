from typing import Callable
import dagger
from dagger import dag, function, object_type

PYTHON_IMAGE = "python:3.13-slim"


def uv(version: str = "latest") -> Callable[[dagger.Container], dagger.Container]:
    uv = dag.container().from_(f"ghcr.io/astral-sh/uv:{version}")

    def with_container_func(ctr: dagger.Container) -> dagger.Container:
        return ctr.with_files("/usr/bin/", [uv.file("/uv"), uv.file("/uvx")])

    return with_container_func


@object_type
class Resume:
    """Dagger pipeline to build, test, and publish the LaTeX resume"""

    workdir = "/workspace"
    output_dir = "/workspace/output"

    @function
    def build_env(self, source: dagger.Directory) -> dagger.Container:
        """Use a prebuilt LaTeX environment"""
        latex_cache = dag.cache_volume("latex-build-cache")
        return (
            dag.container()
            .from_("ghcr.io/xu-cheng/texlive-full:latest")
            .with_directory(self.workdir, source)
            .with_mounted_cache("/workspace/.latex-cache", latex_cache)
            .with_workdir(self.workdir)
        )

    @function
    def generate_tex(self, source: dagger.Directory) -> dagger.Directory:
        """Runs the Python script to generate .tex files and update cv.yaml."""

        uv_cache = dag.cache_volume("uv-venv-cache")

        return (
            dag.container()
            .from_(PYTHON_IMAGE)
            .with_(uv("latest"))
            .with_mounted_directory("/app", source)
            .with_workdir("/app")
            .with_mounted_cache("/root/.venv", uv_cache)
            .with_exec(["uv", "venv"])
            .with_exec(["uv", "pip", "install", "-r", "pyproject.toml"])
            .with_exec(["uv", "run", "generate_resume.py"])
            .directory("/app")
        )

    @function
    def build(self, source: dagger.Directory) -> dagger.File:
        """Build the LaTeX resume PDF and return the compiled file"""

        container = (
            self.build_env(source)
            .with_workdir(self.workdir)
            .with_exec(["mkdir", "-p", self.output_dir])
            .with_exec(
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "--output-directory=output",
                    "latex/resume.tex",
                ]
            )
        )

        return container.file(f"{self.output_dir}/resume.pdf")

    @function
    def get_artifacts(self, source: dagger.Directory) -> dagger.Directory:
        tex_and_yaml_container: dagger.Directory = self.generate_tex(source=source)
        resume_pdf: dagger.File = self.build(tex_and_yaml_container)

        tex_dir = "tex_dir"
        output = "output"
        container = (
            dag.container()
            .from_("cgr.dev/chainguard/wolfi-base")
            .with_workdir("artifacts")
            .with_file(path=f"{output}/resume.pdf", source=resume_pdf)
            .with_directory(path=tex_dir, directory=tex_and_yaml_container)
            .with_exec(["cp", f"{tex_dir}/resume.yaml", output])
            .with_exec(["cp", f"{tex_dir}/cv.yaml", output])
            .with_exec(["cp", f"{tex_dir}/latex/resume.tex", output])
        )
        return container.directory(output)
