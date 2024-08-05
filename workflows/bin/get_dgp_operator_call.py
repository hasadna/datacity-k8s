#!/usr/bin/env python3
import sys
import json
import subprocess

from ruamel.yaml import YAML


yaml = YAML(typ='safe')


ROOTPATHS_CONFIG = {
    # python3 workflows/bin/get_dgp_operator_call.py genericFetcherInstanceOrganizationWorkflows.haifa-automated-devices
    'genericFetcherInstanceOrganizationWorkflows': {
        'get_name': lambda values: f'generic-fetcher-{values[1]}',
        'config_instance_key': 'target_instance_name'
    },
    # python3 workflows/bin/get_dgp_operator_call.py continuousProcessingTasksInstanceWorkflows.haifa.xlsx
    'continuousProcessingTasksInstanceWorkflows': {
        'get_name': lambda values: f'cntprct-{values[1]}-{values[2]}',
        'config_instance_key': 'instance_name'
    },
    # python3 workflows/bin/get_dgp_operator_call.py gisFetcherInstanceOrganizationWorkflows.haifa-yeudei-karka
    'gisFetcherInstanceOrganizationWorkflows': {
        'get_name': lambda values: f'gis-fetcher-{values[1]}',
        'config_instance_key': 'target_instance_name'
    },
}


def main(values_path, *args):
    kwargs = {}
    for arg in args:
        if arg.startswith('--') and '=' in arg:
            arg = arg.replace('--', '')
            key, value = arg.split('=')
            kwargs[key] = value
    exec_ = '--exec' in args
    values = values_path.split('.')
    rootpath_config = ROOTPATHS_CONFIG.get(values[0])
    if rootpath_config:
        if 'get_extra_config' in rootpath_config:
            extra_config = rootpath_config['get_extra_config'](kwargs, values)
        else:
            extra_config = {}
        extra_config[rootpath_config['config_instance_key']] = kwargs.get('target_instance_name') or 'LOCAL_DEVELOPMENT'
        templates = subprocess.check_output(['helm', 'template', 'workflows'], text=True)
        templates = yaml.load_all(templates)
        num_matches = 0
        cmd = None
        for template in templates:
            if template.get('kind') == 'WorkflowTemplate' and template.get('metadata', {}).get('name') == rootpath_config['get_name'](values):
                num_matches += 1
                params = {p['name']: p['value'] for p in template['spec']['templates'][0]['steps'][0][0]['arguments']['parameters']}
                config = json.loads(params['config_json'])
                config.update(extra_config)
                config_json = json.dumps(config, ensure_ascii=False)
                cmd = ['-m', f'datacity_ckan_dgp.operators.{params["operator"]}', config_json]
                print('python3 ' + ' '.join(cmd))
        if num_matches == 0:
            print('ERROR! No matching generic fetcher workflow found.')
            exit(1)
        elif num_matches > 1:
            print('ERROR! Multiple matching generic fetcher workflows found.')
            exit(2)
        elif exec_:
            subprocess.check_call(['venv/bin/python3'] + cmd, cwd=f'../datacity-ckan-dgp')
        else:
            exit(0)


if __name__ == '__main__':
    main(*sys.argv[1:])
