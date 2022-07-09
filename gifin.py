#!/usr/bin/python3
import configparser, json, os, requests, shlex, shutil, subprocess, sys, urllib, urllib.request
from xdg.BaseDirectory import *

# Configuration
os.makedirs(os.path.join(xdg_config_home, "gifin"), exist_ok=True)
config_defaults_gifin = {
        'giphy_api_key': '',
        'send_type': 'fifo',
        'send_target': '~/.weechat/weechat_fifo',
        'termexec': 'xterm -e'
        }

config = configparser.ConfigParser()

def config_create():
    config.add_section('gifin')

    for i in config_defaults_gifin:
        config['gifin'][i] = config_defaults_gifin[i]

    with open(os.path.join(xdg_config_home, 'gifin/config'), 'w') as configfile:
        config.write(configfile)

if not os.path.exists(os.path.join(xdg_config_home, 'gifin/config')):
    config_create()

config.read(os.path.join(xdg_config_home, 'gifin/config'))

# Check for missing keys
for i in config_defaults_gifin:
    if not config.has_option('gifin', i):
        config['gifin'][i] = config_defaults_gifin[i]
with open(os.path.join(xdg_config_home, 'gifin/config'), 'w') as configfile:
    config.write(configfile)
giphy_api_key = config['gifin']['giphy_api_key']
send_type = config['gifin']['send_type']
send_target = config['gifin']['send_target']
termexec = config['gifin']['termexec']

def send_to_weechat(image):
    if send_type == 'tmux':
        os.system('tmux send-keys -t %s "%s"' % (send_target, image))
    else:
        with open(os.path.expanduser("%s" % send_target),"w") as fp:
            fp.write("*/input insert %s\n" % image)

def main():
    if len(sys.argv) == 1:
        print('gifin <term>.')
    elif sys.argv[1] == '--weechat':
        if len(sys.argv) == 2:
            print('gifin --weechat <image>.')
        else:
            send_to_weechat(sys.argv[2])
    else:
        shutil.rmtree('/tmp/gifin')
        os.makedirs('/tmp/gifin', exist_ok=True)
        data = json.loads(urllib.request.urlopen("http://api.giphy.com/v1/gifs/search?q=%s&api_key=%s" % (sys.argv[1].replace(' ', '%20'), giphy_api_key)).read())

        for i in data['data']:
            if i['type'] == "gif":
                url = "https://i.giphy.com/media/%s/giphy.webp" % i['id']
                response = requests.get(url, stream=True)
                open('/tmp/gifin/%s.webp' % i['id'], 'wb').write(response.content)

        subprocess.Popen(shlex.split('%s term-image /tmp/gifin' % termexec))

if __name__ == "__main__":
    main()

