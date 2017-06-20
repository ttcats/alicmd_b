#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible import constants as C
from ansible.utils.ssh_functions import check_for_controlpersist
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase



class ResultCallback(CallbackBase):
    
    '''
    重新定义CallbackBase类,用于自定义日志输出(这是以json方式输出)
    '''

    def v2_runner_on_ok(self, result):
        host = result._host.get_name()
        global info
        info = json.dumps({host: result._result}, indent=4)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        print(json.dumps({host: result._result}, indent=4))

    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        return(json.dumps({host: result._result}, indent=4))

    def v2_playbook_on_stats(self, stats):
        return(json.dumps({host: stats.summarize(host) for host in stats.processed.keys()}, indent=4))

    def v2_playbook_on_play_start(self, play):
        pass


class CallBack_PlaybookExecutor(PlaybookExecutor):

    '''
    重新定义PlaybookExecutor类,增加了stdout_callback参数,可用于自定义日志格式输出
    '''

    def __init__(self, playbooks, inventory, variable_manager, loader, options, passwords, stdout_callback=None):
        self._playbooks = playbooks
        self._inventory = inventory
        self._variable_manager = variable_manager
        self._loader = loader
        self._options = options
        self.passwords = passwords
        self._unreachable_hosts = dict()

        if options.listhosts or options.listtasks or options.listtags or options.syntax:
            self._tqm = None
        else:
            self._tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=self.passwords,
                stdout_callback=stdout_callback)

        check_for_controlpersist(C.ANSIBLE_SSH_EXECUTABLE)



class Runner(object):
    def __init__(self, *args, **kwargs):
        self.inventory = None
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.results_callback = None
        self.passwords = None
        self.__initializeData()
        self.results_callback = ResultCallback()

    def __initializeData(self):
        # 初始化ansible
        Options = namedtuple('Options',
                             ['connection',
                              'module_path',
                              'forks',
                              'become',
                              'become_method',
                              'become_user',
                              'listhosts',
                              'listtasks',
                              'listtags',
                              'syntax',
                              'check'])
        self.loader = DataLoader()
        self.variable_manager = VariableManager()

        self.options = Options(
            connection='ssh',
            module_path='/usr/share/ansible',
            forks=3,
            become=None,
            become_method=None,
            become_user=None,
            listhosts=None,
            listtasks=None,
            listtags=None,
            syntax=None,
            check=False)

        self.inventory = Inventory(
            loader=self.loader,
            variable_manager=self.variable_manager,
            host_list='/etc/ansible/hosts')

        self.variable_manager.set_inventory(self.inventory)

    def run(self, hosts, module, args):
        play_source = dict(
            name="ansible run",
            hosts=hosts,
            gather_facts='no',
            tasks=[
                dict(
                    action=dict(
                        module=module,
                        args=args),
                    register='shell_out'),
                dict(
                    action=dict(
                        module='debug',
                        args=dict(
                            msg='{{shell_out.stdout}}')))
            ]
        )
        play = Play().load(
            play_source,
            variable_manager=self.variable_manager,
            loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=self.results_callback,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
        try:
            return(info)
        except:
            pass



    def run_playbook(self, files, host_list, commend):
        extra_vars = {} #额外的参数,yml模板中的参数,--extra-vars
        extra_vars['host_list'] = host_list
        extra_vars['commend'] = commend
        self.variable_manager.extra_vars = extra_vars

        playbook = CallBack_PlaybookExecutor(
            playbooks=files,
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            passwords=self.passwords,
            stdout_callback=self.results_callback
        )
        playbook.run()


if __name__ == '__main__':
    t = Runner()
    print(t.run('10.7.253.14', 'setup', ''))
