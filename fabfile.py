from fabric.api import task, local
from fabric.contrib.console import confirm


pylint_disable = ",".join(["R0903", "C0103", "R0903", "F0401", "C0301"])
pep8_disable = ",".join(["E501"])


@task(default=True)
def pyflakes():
    local("pyflakes .")


@task
def pep8():
    local("python tools/pep8.py --ignore={pep8_disable} --repeat *.py tvnamer/*.py tests/*.py".format(pep8_disable = pep8_disable))


@task
def pylint():
  local("pylint --reports=n --disable-msg={pylint_disable} *.py tvnamer/*.py tests/*.py".format(pylint_disable = pylint_disable))


@task(default=True)
def test():
    local("nosetests")


@task
def topypi():
    import sys
    sys.path.insert(0, ".")
    import tvnamer
    version = tvnamer.__version__

    msg = "Upload tvnamer {0} to PyPi?".format(".".join(str(x) for x in version))
    if not confirm(msg, default = False):
        print "Cancelled"
        return

    local("python setup.py sdist register upload")
