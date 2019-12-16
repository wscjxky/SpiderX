from fabric import Connection, task
from invoke import Context

local_con = Context()

def commit(message):
    local_con.run('git add -A && git commit -m ' + message, warn=True)

def pull():
    local_con.run('git pull', warn=True)


def push():
    local_con.run('git push', warn=True)
@task
def deploy(ctx, message=''):
    commit(message)
    pull()
    push()