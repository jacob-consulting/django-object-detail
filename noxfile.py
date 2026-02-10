import nox

DJANGO_VERSIONS = ["4.2", "5.2", "6.0"]


@nox.session(python=["3.12", "3.13"])
@nox.parametrize("django", DJANGO_VERSIONS)
def tests(session, django):
    session.install(f"django~={django}.0")
    session.install(".[dev]")
    session.run("pytest", "--cov=django_object_detail", *session.posargs)
