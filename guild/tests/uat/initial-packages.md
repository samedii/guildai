# Initial packages

By default the `packages` command lists packages in the `gpkg`
namespace). We don't have any installed yet so this is an empty list.

    >>> run("guild packages")
    <BLANKLINE>
    <exit 0>

If we use the `-a` option, we get all packages, which at this point
consists of all of the pip packages that are installed in the env.

Note, the following list is abbreviated to avoid spurious failures.

    >>> run("guild packages -a")
    Jinja2             ...
    Keras-Applications ...
    Markdown           ...
    PyYAML             ...
    Werkzeug           ...
    Whoosh             ...
    tensorboard        ...
    tensorflow...      ...
    wheel              ...
    <exit 0>
