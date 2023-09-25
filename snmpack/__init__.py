try:
    from importlib.metadata import version

    __version__ = version(__package__)
except:  # noqa: E722
    __version__ = "cannot be extracted, upgrade to at least 3.8"
