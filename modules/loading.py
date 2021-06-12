import logging
import os
import ast
from os.path import join as opj

_logger = logging.getLogger('modules.loading')

ADDONS_PATH = 'addons'
ADDONS_DEFAULT_FILE = '__manifest__.py'

addons_list = {}  # list of addons ADDONS_DEFAULT_FILE content


class AddonsModuleImport():
    def __init__(self):
        self.modules_load()

    def modules_load(self):
        """ Get modules list. """
        _logger.debug(f'os.listdir(ADDONS_PATH): {os.listdir(ADDONS_PATH)}')
        for module in os.listdir(ADDONS_PATH):
            addons_module_path = opj(ADDONS_PATH, module)
            if os.path.isdir(addons_module_path):
                addons_module_default_path = opj(addons_module_path, ADDONS_DEFAULT_FILE)
                if os.path.exists(addons_module_default_path):
                    # _logger.debug(f'addons_module_default_path: {addons_module_default_path}')
                    # module ADDONS_DEFAULT_FILE loading
                    manifest = ast.literal_eval(open(addons_module_default_path).read())
                    manifest.update({
                        'addons_module_path': addons_module_path
                    })
                    addons_list[module] = manifest
                    # _logger.debug(f'ADDONS_DEFAULT_FILE= {manifest}')
                    _logger.info(f'Loading {module}')

def get_load_extension():
    """ If auto_install true ,bot load extension modules. """
    module_list = []
    for module in addons_list:
        if 'auto_install' in addons_list[module] and addons_list[module]['auto_install'] == True:
            module_list.append(module)
        else:
            _logger.info(f'{module} no auto_install, skip.')
    for module in module_list:
        if 'depends' in addons_list[module]:
            depends = addons_list[module]['depends']
            no_depends = [depend for depend in depends if depend not in module_list]
            if no_depends:
                _logger.warn(f'Install fail, {module} depends not find or not install. depends= {no_depends}')
                module_list.remove(module)

    return module_list