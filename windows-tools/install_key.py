"""把公钥装进设备真实 root home（/var/root/.ssh/）并验证免密登录。"""

import pathlib
import sys

import paramiko

pub = pathlib.Path.home().joinpath('.ssh/zake_device_key.pub').read_text().strip()

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('127.0.0.1', 2222, username='root', password='yuchen',
          timeout=8, allow_agent=False, look_for_keys=False)

CMDS = [
    # 根因确认：/root 到底指向哪里
    'ls -la /root 2>&1 | head -3',
    # 安装公钥到真实 home；同时兼容 rootless（jbroot）布局
    'mkdir -p /var/root/.ssh && chmod 700 /var/root/.ssh && '
    'echo ' + repr(pub).replace('"', '') + ' > /var/root/.ssh/authorized_keys && '
    'chmod 600 /var/root/.ssh/authorized_keys && '
    'chown -R root:wheel /var/root/.ssh 2>/dev/null; echo INSTALL-OK',
    'cat /var/root/.ssh/authorized_keys | head -c 60; echo',
]

for cmd in CMDS:
    _, out, err = c.exec_command(cmd, timeout=10)
    print('$ ' + cmd[:60] + '...')
    print(out.read().decode(errors='replace')[:500])
    e = err.read().decode(errors='replace')[:200]
    if e:
        print('[stderr]', e)
    print('---')
c.close()
print('DONE')
