# From trozet via apex, minus some things
import json
import logging
import os
import pprint
import subprocess
import sys

def run_ansible(ansible_vars, playbook, host,
                user, tmp_dir=None, dry_run=False, private_key=None):
    """
    Executes ansible playbook and checks for errors
    :param ansible_vars: dictionary of variables to inject into ansible run
    :param playbook: playbook to execute
    :param tmp_dir: temp directory to store ansible command
    :param dry_run: Do not actually apply changes
    :return: None
    """
    logging.info("Executing ansible playbook: {}".format(playbook))
    playbook = sys.prefix + '/usr/share/clianet/playbooks/' + playbook
    ansible_command = ['ansible-playbook', '-u',user,'-i', host+',',
                       '-c', 'smart', playbook, '-vvv']
    if private_key:
        ansible_command.append('--private-key='+private_key)

    if dry_run:
        ansible_command.append('--check')

    if isinstance(ansible_vars, dict) and ansible_vars:
        logging.debug("Ansible variables to be set:\n{}".format(
            pprint.pformat(ansible_vars)))
        ansible_command.append('--extra-vars')
        ansible_command.append(json.dumps(ansible_vars))
    logging.debug("Ansible command: {}".format(ansible_command))
    try:
        my_env = os.environ.copy()
        my_env['ANSIBLE_HOST_KEY_CHECKING'] = 'False'
        logging.info("Executing playbook...this may take some time")
        logging.debug(subprocess.check_output(ansible_command, env=my_env,
                      stderr=subprocess.STDOUT).decode('utf-8'))
    except subprocess.CalledProcessError as e:
        logging.error("Error executing ansible: {}".format(
            pprint.pformat(e.output.decode('utf-8'))))
        raise
