#!/usr/bin/env python

import sys, os
from fabric.api import env, run, execute, settings
from fabric.contrib.files import upload_template
from fabric.context_managers import shell_env, cd
import logging
import datetime

logging.basicConfig(level=logging.INFO)

#env.hosts = ['uieos.itep.ru']
#env.hosts = ['eostest.pnpi.nw.ru']
#env.hosts = ['alice02.spbu.ru', 'eostest.pnpi.nw.ru']
#env.hosts = ['ui2.grid.kiae.ru', 'alice06.spbu.ru', 'eostest.pnpi.nw.ru', 'gridmsu1.sinp.msu.ru', 'vm173.jinr.ru', 'uieos.itep.ru']
env.hosts = ['ui2.grid.kiae.ru', 'alice06.spbu.ru', 'eostest.pnpi.nw.ru', 'vm221-124.jinr.ru', 'uieos.itep.ru']
env.user = 'zar'
env.key_filename = ['/home/virthead/.ssh/jinr_cloud_rsa']

def run_xrdstress(storname='eos', fedname='spb', mb=1):
    mbs = ',1,10,100,'
    if mbs.find(',' + str(mb) + ',') == -1:
        mb = 1
    
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    
    with open('results/xrdstress_%s_%s_%s_%s.log' % (storname, fedname, mb, today), 'a') as f:
        f.write('Host: ')
        f.write(env.host)
        f.write('. Date: ')
        f.write(today)
        f.write('\n')
    
    upload_template('/tmp/x509up_u500', 'x509up_virthead')
    user_home = run('echo $HOME')
    user_proxy = user_home + '/x509up_virthead'
    
    with settings(
        warn_only = True
    ):
        with shell_env(X509_USER_PROXY=user_proxy, TEST_MB=mb):
            if storname == 'eos':
                if fedname == 'msk':
                    output = run('/usr/sbin/xrdstress -d root://muon.grid.kiae.ru//eos/fedcloud/zar/rep1 -o rdwr -j 2 -f 100 -b ${TEST_MB}MB -s ${TEST_MB}MB -n $TEST_MB.$HOSTNAME')
                if fedname == 'spb':
                    output = run('/usr/sbin/xrdstress -d root://alice01.spbu.ru//eos/spbcloud/test/zar/rep0 -o rdwr -j 2 -f 100 -b ${TEST_MB}MB -s ${TEST_MB}MB -n $TEST_MB.$HOSTNAME')
            if storname == 'dcache':
                if fedname == 'msk':
                    output = run('/usr/sbin/xrdstress -d root://muon.grid.kiae.ru//dcache/fedcloud/zar/rep0 -o rdwr -j 2 -f 100 -b ${TEST_MB}MB -s ${TEST_MB}MB -n $TEST_MB.$HOSTNAME')
                if fedname == 'spb':
                    output = run('/usr/sbin/xrdstress -d root://alice01.spbu.ru://dcache/spbcloud/test/zar/rep0/ -o rdwr -j 2 -f 100 -b ${TEST_MB}MB -s ${TEST_MB}MB -n $TEST_MB.$HOSTNAME')
            
            with open('results/xrdstress_%s_%s_%s_%s.log' % (storname, fedname, mb, today), 'a') as f:
                f.write(output + '\n\n')
    

# eos
def run_xrdstress_eos_msk_1():
    run_xrdstress('eos','msk', 1)
def run_xrdstress_eos_spb_1():
    run_xrdstress('eos','spb', 1)

# dcache
def run_xrdstress_dcache_msk_1():
    run_xrdstress('dcache','msk', 1)
def run_xrdstress_dcache_spb_1():
    run_xrdstress('dcache','spb', 1)


def run_alice():
    with open('alice.log', 'a') as f:
        f.write('Host: ')
        f.write(env.host)
        f.write('. Date: ')
        f.write(str(datetime.now()))
        f.write('\n')
    
    upload_template('/tmp/x509up_u500', 'x509up_virthead')
    user_home = run('echo $HOME')
    user_proxy = user_home + '/x509up_virthead'

    with settings(
        warn_only = True
    ):
        with shell_env(X509_USER_PROXY=user_proxy):
            with cd('~/scripts'):
                output = run('source ./ALEIN.env;./alicetest.sh ~/muon_alice_data')
            
            with open('alice.log', 'a') as f: 
                f.write(output + '\n\n')

def run_atlas():
    with open('atlas.log', 'a') as f:
        f.write('Host: ')
        f.write(env.host)
        f.write('. Date: ')
        f.write(str(datetime.now()))
        f.write('\n')
    
    upload_template('/tmp/x509up_u500', 'x509up_virthead')
    upload_template('muon_atlas_data', 'muon_atlas_data')
    user_home = run('echo $HOME')
    user_proxy = user_home + '/x509up_virthead'

    with settings(
        warn_only = True
    ):
        with shell_env(X509_USER_PROXY=user_proxy):
            with cd('~/fed-storage-tests/scripts/'):
                output = run('source atlas.init;../atlastesfull_0.sh  ~/muon_atlas_data')
            
            with open('atlas.log', 'a') as f: 
                f.write(output + '\n\n')
