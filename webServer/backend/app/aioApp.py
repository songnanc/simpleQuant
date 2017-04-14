import os
import argparse
import aiopg.sa
import asyncio
import sys
import trafaret as T
import zmq

from aiohttp import web
from trafaret_config import commandline

from .routes import setup_routes
from common.simpleQuantZmqProcess import SimpleQuantZmqRequestReplyProcess
from common.simpleQuantLogger import SimpleQuantLoggerServer

primitive_ip_regexp = r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$'

TRAFARET = T.Dict({
    T.Key('postgres'):
        T.Dict({
            'database': T.String(),
            'user': T.String(),
            'password': T.String(),
            'host': T.String(),
            'port': T.Int(),
            'minsize': T.Int(),
            'maxsize': T.Int(),
        }),
    T.Key('regressionServer'):
        T.Dict({
            'addr': T.String(),
            'port': T.Int(),
        }),
    T.Key('host'): T.String(regex=primitive_ip_regexp),
    T.Key('port'): T.Int(),
})

async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        loop=app.loop)
    app['db'] = engine

async def init_regression(app):
    msg = ['connectionReq', {'name':'zechfox'}]

    regressionClient = app['regressionClient']
    await regressionClient.send(msg)
    msgName, data = await regressionClient.recv()

async def logHandler(message):
    print(message)

async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()

def init(argv):

    ap = argparse.ArgumentParser()
    dirPath = os.path.dirname(os.path.realpath(__file__)) 
    configFile = os.path.abspath(os.path.join(dirPath, '../config/config.yaml'))
    commandline.standard_argparse_options(ap,
                                          default_config=configFile)
    #
    # define your command-line arguments here
    #
    options = ap.parse_args(argv)

    config = commandline.config_from_options(options, TRAFARET)

    #
    # log server
    #
    logServer = SimpleQuantLoggerServer('127.0.0.1:4321', logHandler)
    logServer.run()

    #
    # regression server
    #
    regressionServerConfig = config['regressionServer']
    regressionServerAddr = regressionServerConfig['addr']
    regressionServerPort = regressionServerConfig['port']
    serverAddr = regressionServerAddr + ':' + str(regressionServerPort)
    regressionClient = SimpleQuantZmqRequestReplyProcess(False, serverAddr)
    regressionClient.run()
    # setup application and extensions
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)

    # load config from yaml file in current dir
    app['config'] = config

    #regression client
    app['regressionClient'] = regressionClient

    #log server
    app['logServer'] = logServer 

    # create connection to the database
    app.on_startup.append(init_pg)
    # shutdown db connection on exit
    app.on_cleanup.append(close_pg)

    # create connection to regression server
    app.on_startup.append(init_regression)
    # setup views and routes
    setup_routes(app)

    return app 

def run(argv):
    # init logging


    app = init(argv)
    web.run_app(app,
                host=app['config']['host'],
                port=app['config']['port'])
if __name__ == '__main__':
    run(sys.argv[1:])
