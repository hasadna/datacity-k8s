#!/usr/bin/env python3
import sys
import json
import subprocess

from ruamel.yaml import YAML


yaml = YAML(typ='safe')


def main(values_path, *args):
    target_instance_name = 'LOCAL_DEVELOPMENT'
    for arg in args:
        if arg.startswith('--target-instance-name='):
            target_instance_name = arg.split('=')[1]
    exec_ = '--exec' in args
    values = values_path.split('.')
    if values[0] == 'genericFetcherInstanceOrganizationWorkflows':
        name_suffix = values[1]
        templates = subprocess.check_output(['helm', 'template', 'workflows'], text=True)
        templates = yaml.load_all(templates)
        num_matches = 0
        cmd = None
        for template in templates:
            if template.get('kind') == 'WorkflowTemplate' and template.get('metadata', {}).get('name') == f'generic-fetcher-{name_suffix}':
                num_matches += 1
                params = {p['name']: p['value'] for p in template['spec']['templates'][0]['steps'][0][0]['arguments']['parameters']}
                config = json.loads(params['config_json'])
                config['target_instance_name'] = target_instance_name
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
