Projector Integration for Jupyter
----

The Projector Integration for Jupyter enables you to access [supported](#supported-jetbrains-ides) Jetbrains IDEs in a web browser from your Jupyter environment. 

`jupyter-projector-proxy` is a Python® package based on the following packages.

| Package                                                                    | Description                                                                                                                                                                                                                                                   |
|----------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [projector-installer](https://github.com/JetBrains/projector-installer)    | Provides infrastructure to launch any Jetbrains IDEs and connect to it from a web browser.                                                                                                                                                                    |
| [jupyter-server-proxy](https://github.com/jupyterhub/jupyter-server-proxy) | Extends Jupyter environments to launch any Jetbrains IDEs as an external process alongside the notebook server. For more information see [GUI Launchers](https://jupyter-server-proxy.readthedocs.io/en/latest/launchers.html#jupyterlab-launcher-extension). |

**NOTE:** This package *currently*, does not provide a kernel level integration with Jupyter.

To report any issues or suggestions, see the [Feedback](#feedback) section.

----
## Requirements

This package has the same requirements as its dependencies:
* See [Requirements](https://github.com/jupyterhub/jupyter-server-proxy#requirements) from `jupyter-server-proxy`
* See [Requirements](https://github.com/JetBrains/projector-installer#Installation) from `projector-installer`
* If not already installed, install system packages required for JetBrains-in-a-browser support
  
  **Example (ubuntu):**
  ```bash
    # Install as root or superuser
    apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y \
    libxtst6 \
    libxrender1 \
    libfontconfig1 \
    libxi6 \
    libgtk-3-0
  ```
  
* Install at least one of the [supported](#supported-jetbrains-ides) Jetbrains IDEs. See installation examples below.

After installing the desired intelliJ product, make sure that:
* The `idea.properties` located at `IDE_HOME/bin` is writable by the user that has started `jupyter/jupyterlab/jupyterhub`. `IDE_HOME` is the location where you installed your desired jetbrains IDE
* The installed IDEs can be discovered by this package by using one of the following options:
  * Option 1: (Recommended)
  
    Create a link in the PATH that points to the installed jetbrains IDEs using the appropriate IDE [name](#ides-names)
    ```bash
    # Add a binary to the PATH that points to the IDE startup script.
    ln -s [IDE_HOME]/bin/[IDE].sh /usr/bin/[IDE]
    ```

  * Option 2
  
    Install the IDE in standard locations `/opt/[IDE]`. Use this option if you are not installing multiples editions of the same product. For example, if you are installing Pycharm community edition and Pycharm Professional, use the option 1. Same applies to IntelliJ idea editions.

**Generic installation example:**

```bash
    # Install IDEs as root or superuser
    mkdir -p /opt/[IDE]
    curl -L "https://download.jetbrains.com/product?code=[CODE]&latest&distribution=linux" \
    | tar -C /opt/[IDE] --strip-components 1 -xzvf -
    
    # Make The idea.properties editable by the user that has started jupyter/jupyterlab/jupyterhub
    chown <jupyter_launch_user> [IDE_HOME]/bin/idea.properties
   
    # Add a binary to the PATH that points to the IDE startup script.
    RUN ln -s /opt/[IDE]/bin/[IDE].sh /usr/bin/[IDE]
  ```
   Make sure that you replace [IDE] with the [name](#ides-names) of the IDE in lowercase and provide its [corresponding [CODE]](https://plugins.jetbrains.com/docs/marketplace/product-codes.html).

   **IntelliJ ultimate installation example:**
   ```bash
       # As root or superuser
       # Install IntelliJ IDEA Ultimate
        mkdir -p /opt/idea
        curl -L "https://download.jetbrains.com/product?code=IU&latest&distribution=linux" \
       | tar -C /opt/idea --strip-components 1 -xzvf -
       
       # Make The idea.properties editable
       # If the user you use to start jupyter/jupyter lab/ jupyter hub is named tiaden
        chown tiaden /opt/idea/bin/idea.properties
       
       # Create a symbolic link in PATH that points to the Intellij startup script.
        ln -s /opt/idea/bin/idea.sh /usr/bin/intellij-idea-ultimate
   ```

  **Pycharm community edition example:**
   ```bash
       # As root or superuser
       # Install Pycharm Community
        mkdir -p /opt/pycharm
        curl -L "https://download.jetbrains.com/product?code=PCC&latest&distribution=linux" \
       | tar -C /opt/pycharm --strip-components 1 -xzvf -
       
       # Make The idea.properties editable
       # If the user you use to start jupyter/jupyterlab/jupyter hub is named tiaden
        chown tiaden /opt/pycharm/bin/idea.properties
       
       # Create a symbolic link in PATH that points to the Intellij startup script.
        ln -s /opt/pycharm/bin/pycharm.sh /usr/bin/pycharm
   ```

## IDEs names
* IntelliJ idea &rarr; idea
* Pycharm &rarr; pycharm
* DataGrip &rarr; datagrip
* Goland &rarr; goland
* Clion &rarr; clion
* PhpStorm &rarr; phpstorm
* RubyMine &rarr; rubymine


Only when you are installing multiple editions of the same product (for example IntelliJ idea ultimate and IntelliJ idea educational at the same time), you need to be explicit about the name instead of using the generic name idea or pycharm

* Intellij idea ultimate &rarr; intellij-idea-ultimate
* IntelliJ community &rarr; intellij-idea-community
* IntelliJ educational &rarr; intellij-idea-educational
* Pycharm professional &rarr; pycharm-professional
* Pycharm community &rarr; pycharm-community
* Pycharm educational &rarr; pycharm-educational

## Supported Jetbrains IDEs
* IntelliJ idea (ultimate,community,educational)
* Pycharm (professional,community,educational)
* DataGrip
* WebStorm
* Goland
* Clion
* PhpStorm
* RubyMine

## Installation

### PyPI
This repository can be installed directly from the Python Package Index.
```bash
python -m pip install jupyter-projector-proxy
```

If you want to use this integration with JupyterLab®, ensure that you have JupyterLab installed on your machine by running the following command:
```bash
python -m pip install jupyterlab
```

You should then install `jupyterlab-server-proxy` JupyterLab extension. To install the extension, use the following command:

``` bash
jupyter labextension install @jupyterlab/server-proxy
```

### Building From Sources
```bash
git clone https://github.com/tiaden/jupyter-projector-proxy.git

cd jupyter-projector-proxy

python -m pip install .
```

## Usage

Upon successful installation of `jupyter-projector-proxy`, your Jupyter environment should present options to launch your installed IDE.

* Open your Jupyter environment by starting jupyter notebook or lab
  ```bash
  # For Jupyter Notebook
  jupyter notebook

  # For Jupyter Lab
  jupyter lab 
  ```

* If you are using Jupyter Notebook, on the `New` menu, select one of your installed IDEs . If you are using JupyterLab, select the installed IDE icon on the launcher.

<p align="center">
  <img alt="image" width="600" src="https://github.com/tiaden/jupyter-projector-proxy/raw/master/img/projector_jupyterlab.png">
</p>

## Integration with JupyterHub

To use this integration with JupyterHub®, you must install the `jupyter-projector-proxy` Python package in the Jupyter environment launched by your JupyterHub platform. 

For example, if your JupyterHub platform launches Docker containers, then install this package in the Docker image used to launch them.


## Troubleshooting

In the environment that you have installed the package:

* Verify if the projector executable is discoverable (i.e. if it is in the PATH)
    ```bash
    $ which projector
     ~/.local/bin/projector
    ```

* Verify if the installed Jetbrains executable is discoverable (i.e. if it is in the PATH)

    ```bash
    $ which pycharm
     /usr/bin/pycharm
    ```

* Check if their Python version is 3.8 or higher
    ```bash
    $ python --version
    Python 3.8.10
    ```

* Verify that the user has `Write` permission on `[IDE_HOME]/bin/idea.properties`.
  If you don't see `Permissions Granted` after executing the below command, you need to follow the 
  example above in order to modify the permissions of the user that runs `jupyter/jupyterlab/jupyterhub`
    ```bash
     # If you have installed pycharm like in the above example
    $ [ -w /opt/pycharm/bin/idea.properties ] && echo "Permissions Granted"
    ```

* Ensure that `jupyter-projector-proxy` and the `jupyter` executables are in the same environment as the python executable.
    For example if you are using VENV to manage your python environments:
    ```bash
    $ which python 
    /home/user/my-project/packages/.venv/bin/python

    $ which jupyter-projector-proxy
    /home/user/my-project/packages/.venv/bin/jupyter-projector-proxy

    $ which jupyter
    /home/user/my-project/packages/.venv/bin/jupyter
    ```
    Notice that `jupyter-projector-proxy`, `jupyter` and the `python` executable are in the same parent directory, in this case it is: `/home/user/my-project/packages/.venv/bin`

* Ensure that you are launching `jupyter notebook` using the same executable as listed above.

* Ensure that all two packages are installed in the same python environment
    ```bash
    # Pipe the output of pip freeze and grep for jupyter and jupyter-projector-proxy.
    # All two packages should be highlighted in the output.
    # If you don't see anyone of them, then either the packages missing in the output have been installed
    # in a different python environment or not installed at all.
    $ pip freeze | grep -E "jupyter|jupyter-projector-proxy"
    ```

* Ensure that all required system packages are installed for JetBrains-in-a-browser support 
    
  **Example (ubuntu):**
    ```bash
    # Pipe the output of apt and grep for the required system packages.
    # All required packages should be highlighted in the output.
    # If you don't see anyone of them, then the packages missing in the output have not been installed
    $ apt list --installed | grep -E "libxtst6|libxrender1|libfontconfig1|libxi6|libgtk-3-0"
    ```

* If the integration is not showing up as an option to the dropdown box in the Jupyter notebook:
    ```bash
    #Run the following commands and verify that you are able to see similar output:
    
    $ jupyter serverextension list
    config dir: /home/user/anaconda3/etc/jupyter
        jupyter_server_proxy  enabled
        - Validating...
        jupyter_server_proxy  OK
        jupyterlab  enabled
        - Validating...
        jupyterlab 2.2.6 OK
    
    $ jupyter nbextension list
    Known nbextensions:
    config dir: /home/user/anaconda3/etc/jupyter/nbconfig
        notebook section
        jupyter-js-widgets/extension  enabled
        - Validating: OK
        tree section
        jupyter_server_proxy/tree  enabled
        - Validating: OK  $ pip freeze | grep -E "jupyter|jupyter-projector-proxy"
    
    # IF the server does not show up in the commands above, install:
    $ pip install jupyter_contrib_nbextensions
    ```

## Feedback

We encourage you to try this repository with your environment and provide feedback.
If you encounter a technical issue or have an enhancement request, create an issue [here](https://github.com/tiaden/jupyter-projector-proxy/issues)