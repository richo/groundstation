import git_store

STORAGE_BACKENDS = {
        "git": git_store.GitStore,
        }


class NoSuchObject(Exception):
    pass
