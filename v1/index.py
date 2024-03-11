'''
Author: Bramhesh Kumar Srivastava
Version: 0.0.1
Date: 2023-04-19
'''
# Import the 'server' function from the 'index' module of the 'server' package
from .setups.server.index import server

def application():
    return server()