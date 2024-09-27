def info(version: str) -> None:
    """
    Shows information about version and description.
    :param version:
    :return:
    """
    print("""
┏┓┓         
┃┃┃┏┓╋┏┓┏┓┏┓
┣┛┗┗┻┗┗┛┗┛┛┗
Version: v{version}
    """.format(version=version))
