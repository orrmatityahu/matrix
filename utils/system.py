import os


def get_file_path(file_name):
    """
    function to get file path for cross platform support
    :param file_name: file name
    :return: return file name from files directory
    """
    return os.path.join('files', file_name)