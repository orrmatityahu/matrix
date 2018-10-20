import os
import platform


def get_file_path(file_name):
    """
    function to get file path for cross platform support
    :param file_name: file name
    :return: return file name from files directory
    """
    return os.path.join('files', file_name)


def get_file_name_by_os():
    """
    function to get file name by os
    :return: return file name
    """
    if platform.mac_ver()[0]:
        return 'chromedriver-mac'
    elif platform.win32_ver()[0]:
        return 'chromedriver.exe'
    else:
        return 'chromedriver-linux'
