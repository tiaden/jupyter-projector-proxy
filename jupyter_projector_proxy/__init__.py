import os
import shutil
import subprocess
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

_to_generic_name = {
    "pycharm-professional": "pycharm",
    "pycharm-community": "pycharm",
    "pycharm-educational": "pycharm",
    "intellij-idea-ultimate": "idea",
    "intellij-idea-educational": "idea",
    "intellij-idea-community": "idea"
}


def get_executable(program_name, other_paths=None):
    """
   Try to find the program on the path.
   If it's not found, use the supplied locations to find it
   :param program_name: the program to look for
   :param other_paths: additional list of path to use in case, the program was not found in the path
   :return: the program executable, otherwise throws an exception.
   """
    executable = shutil.which(program_name)
    if executable:
        return executable

    if other_paths is not None:
        for op in other_paths:
            if os.path.exists(op):
                return op

    raise FileNotFoundError(f'Could not find {program_name} in PATH')


def get_jetbrains_ide_executable(ide_name):
    """
    Find the ide in standard locations
    Try to find the executable on Path first.
    Doing so give the opportunity for the ide home directory to have any name.
    Otherwise, the ide home directory must be named pycharm if the start executable in
    IDE_HOME/bin/ is name pycharm.sh. ide name is derived from the ide executable name (IDE_HOME/bin/<ide_name>.sh)
    :param ide_name: the ide name like in IDE_HOME/bin/<ide_name>.sh
    :return: the ide executable
    """
    other_paths = [
        os.path.join("/usr/bin", f"{ide_name}.sh"),
        os.path.join("/usr/local/bin", f"{ide_name}.sh"),
        os.path.join(str(Path.home()), ".local/bin", f"{ide_name}.sh"),
        os.path.join(f"/opt/{ide_name}/bin", f"{ide_name}.sh"),
    ]
    return get_executable(ide_name, other_paths)


def get_projector_executable():
    """
    Find the projector executable.
    Otherwise, throws an exception
    :return: the projector executable
    """
    other_paths = [
        os.path.join(str(Path.home()), ".local/bin", "projector"),
    ]
    return get_executable("projector", other_paths)


def get_icon_path(ide_name):
    """
    Try to use the icon from the installed ide.
    This gives the opportunity to not add the ide icon to this code or to modify this code in case the icon changes
    :param ide_name: the ide name like in IDE_HOME/bin/<ide_name>.sh
    :return: the icon location
    """
    # try to find the installed ide icon first
    exec_bin_dir = Path(get_jetbrains_ide_executable(ide_name)).resolve().parent.absolute()
    icon_name = _to_generic_name.get(ide_name, ide_name)
    icon_path = os.path.join(str(exec_bin_dir), f"{icon_name}.svg")
    if os.path.exists(icon_path):
        return icon_path
    # try packaged icon
    package_icon = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'icons', f"{ide_name}.svg"
    )
    if os.path.exists(package_icon):
        return package_icon

    raise FileNotFoundError(f'Could not find ide icon')


def get_ide_home(ide_name):
    return Path(get_jetbrains_ide_executable(ide_name)).resolve().parent.parent.absolute()


def setup_projector_for(ide_name, ide_title):
    if not isinstance(ide_name, str):
        raise ValueError("ide_name must be of a String type")

    if not isinstance(ide_title, str):
        raise ValueError("ide_title_name must be of a String type")

    def _get_cmd(port):
        """
         Create the ide config needed by projector and the start command.
         For this to work IDE_HOME/bin/idea.properties must be editable by the effective user of this package.
         Otherwise, the projector config creation will throw a permission denied error
        :param port: the port to use. This should be injected by the jupyter-server-proxy package
        :return: the command to use to start the ide
        """

        cmd = [get_projector_executable(), '--accept-license', 'config', 'add',
               '--use-separate-config', '--force', '--port', str(port), '--hostname=localhost', ide_name,
               get_ide_home(ide_name)]
        ret = subprocess.check_output(cmd)
        logger.info(f"Configuration for {ide_name} successful")
        logger.info(ret.decode())
        start_cmd = os.path.join(str(Path.home()), '.projector/configs', ide_name, 'run.sh')
        return [start_cmd]

    server_process = {
        'command': _get_cmd,
        'timeout': 500,
        'new_browser_tab': True,
        'absolute_url': False,
        'launcher_entry': {
            'title': ide_title,
            'icon_path': get_icon_path(ide_name)
        }
    }
    return server_process


def setup_pycharm():
    return setup_projector_for("pycharm", "PyCharm")


def setup_pycharm_professional():
    return setup_projector_for("pycharm-professional", "PyCharm Professional")


def setup_pycharm_community():
    return setup_projector_for("pycharm-community", "PyCharm Community")


def setup_pycharm_educational():
    return setup_projector_for("pycharm-educational", "PyCharm Educational")


def setup_intellij():
    return setup_projector_for("idea", "Intellij")


def setup_intellij_idea_ultimate():
    return setup_projector_for("intellij-idea-ultimate", "Intellij Idea Ultimate")


def setup_intellij_idea_community():
    return setup_projector_for("intellij-idea-community", "Intellij Idea Community")


def setup_intellij_idea_educational():
    return setup_projector_for("intellij-idea-educational", "Intellij Idea Edu")


def setup_datagrip():
    return setup_projector_for("datagrip", "DataGrip")


def setup_webstorm():
    return setup_projector_for("webstorm", "WebStorm")


def setup_goland():
    return setup_projector_for("goland", "Goland")


def setup_clion():
    return setup_projector_for("clion", "Clion")


def setup_phpstorm():
    return setup_projector_for("phpstorm", "PhpStorm")


def setup_rubymine():
    return setup_projector_for("rubymine", "RubyMine")


def _try_add_ide(entry_point_array, ide_name, entry_point_item):
    # Since this package support multiples jetbrains IDEs, we need to fail silently
    # for non installed IDEs in order to give a chance to those installed
    try:
        get_ide_home(ide_name)
        entry_point_array.append(entry_point_item)
        logger.info(f"Found installed ide {ide_name}")
    except FileNotFoundError:
        logger.warning(f"Warning:{ide_name} could not be found !")


def get_projector_servers():
    entry_points = []
    # Pycharm editions
    _try_add_ide(entry_points, "pycharm", "pycharm = jupyter_projector_proxy:setup_pycharm")
    _try_add_ide(entry_points, "pycharm-professional", "pycharm-professional = "
                                                       "jupyter_projector_proxy:setup_pycharm_professional")
    _try_add_ide(entry_points, "pycharm-community", "pycharm-community = "
                                                    "jupyter_projector_proxy:setup_pycharm_community")
    _try_add_ide(entry_points, "pycharm-educational", "pycharm-educational = "
                                                      "jupyter_projector_proxy:setup_pycharm_educational")
    # IntelliJ editions
    _try_add_ide(entry_points, "idea", "idea = jupyter_projector_proxy:setup_intellij")
    _try_add_ide(entry_points, "intellij-idea-ultimate", "intellij-idea-ultimate = "
                                                         "jupyter_projector_proxy:setup_intellij_idea_ultimate")
    _try_add_ide(entry_points, "intellij-idea-community", "intellij-idea-community = "
                                                          "jupyter_projector_proxy:setup_intellij_idea_community")
    _try_add_ide(entry_points, "intellij-idea-educational", "intellij-idea-educational = "
                                                            "jupyter_projector_proxy:setup_intellij_idea_educational")

    _try_add_ide(entry_points, "datagrip", "datagrip = jupyter_projector_proxy:setup_datagrip")
    _try_add_ide(entry_points, "webstorm", "webstorm = jupyter_projector_proxy:setup_webstorm")
    _try_add_ide(entry_points, "goland", "goland = jupyter_projector_proxy:setup_goland")
    _try_add_ide(entry_points, "clion", "clion = jupyter_projector_proxy:setup_clion")
    _try_add_ide(entry_points, "phpstorm", "phpstorm = jupyter_projector_proxy:setup_phpstorm")
    _try_add_ide(entry_points, "rubymine", "rubymine = jupyter_projector_proxy:setup_rubymine")

    # There should be at least one supported IDEs installed or found. Otherwise, an exception is thrown
    # Meaning, this extension should not be installed without at least one supported IDEs
    if 0 == len(entry_points):
        raise ValueError("No supported IDEs can be found. At least one of the supported IDEs should me installed."
                         " Consult the documentation for more information")

    return entry_points
