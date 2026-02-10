import nox


@nox.session(python=["3.12", "3.13"])
def tests(session):
    session.install(".[dev]")
    session.run("pytest", "--cov=django_object_detail", *session.posargs)
