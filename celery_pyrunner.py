#!/usr/bin/env python

import functools
import sys
import os

from celery_app.app import app


def get_path_component(a_path):
  res = []
  while a_path != '':
    a_path, tail = os.path.split(a_path)
    res.insert(0, tail)
  return res

def split_task_config(argvs):
  task_config = {}
  config_names = ['priority', 'queue', 'routing_key']
  for config in config_names:
    config_flag = '--%s' % config
    if config_flag in argvs:
      idx = argvs.index(config_flag)
      argvs.pop(idx)
      config_value = argvs.pop(idx)
      if config == 'priority':
        config_value = int(config_value)
      task_config.update({config: config_value})
  return task_config, argvs

def gen_env():
  env = {}
  env.update(os.environ)
  if 'TZ' not in env:
    env['TZ'] = 'Asia/Shanghai'
  python_path = [
      os.path.normpath(
          os.getcwd())
  ]
  python_path = ':'.join(python_path)
  if 'PYTHONPATH' in env:
    env['PYTHONPATH'] += ':' + python_path
  else:
    env['PYTHONPATH'] = python_path
  return env

@app.task(name='celery_demo')
def run_job(argv):
  py_path = argv[1]
  assert os.path.isfile(py_path), py_path

  a_path, ext = os.path.splitext(py_path)
  comp = get_path_component(a_path)
  assert ext == '.py'
  assert len(comp) >= 1, len(comp)
  module_path = '.'.join(comp)

  args = ['python3', '-B', '-m', module_path] + argv[2:]
  os.execvpe('python3', args, gen_env())

def main(argvs):
  task_config, argv = split_task_config(argvs)
  run_job.apply_async(args=[argv,], **task_config)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
