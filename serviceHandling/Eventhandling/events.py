from typing import Callable
from fastapi import Request
import requests
from requests import adapters
from starlette import config
from core.settings import Settings
from fastapi import FastAPI
from core.config import log, settings
from serviceHandling.Eventhandling.database.dbconfig import DataBase
from motor.motor_asyncio import (AsyncIOMotorClient)
from serviceHandling.Eventhandling.loadserver import LoadBalancer 

session = requests.session()
#load_server = LoadBalancer('localhost',8002, 'round robin')

def get_db() -> AsyncIOMotorClient:
    db= DataBase()
    return db

def get_db_client() -> AsyncIOMotorClient:
    db= DataBase()
    return db.client


def get_database(request: Request):
    """Get current database from app state.

    Args:
        request (Request): HTTP Request object through API.

    Returns:
        Database: Apps database.
    """
    return request.app.mongodb


async def connect_to_db(app: FastAPI) -> None:
        """Function to create a database connection for current app.

        Args:
            app (FastAPI App)

        Raises:
            Exception: DB CONNECTION ERROR.

        Returns:
            None (Opens DB Connection)
        """
        try:
            log.info("connecting to a database")
            app.mongodb_client = get_db_client()
            app.mongodb = app.mongodb_client[settings.db_name]
            log.info(app.mongodb)
            log.info("mongo database connected!")    
            
            log.info("connecting to a server")
            session.merge_environment_settings(url=settings.base_url, proxies=session.proxies, stream=session.stream,verify=None, cert=None)
            session.mount(settings.base_url,adapter=adapters.HTTPAdapter(max_retries=20,pool_maxsize=1000,pool_connections=100,pool_block=1))
            log.info("Server connection - successful")
            #log.info("Load server Open")
            #load_server.select_server(,)
        except Exception as e:
            log.warn("--- CORE CONNECTION ERROR ---")
            log.warn(e)
            log.warn("--- CORE CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
        """Function to close a database connection for current app.

        Args:
            app (FastAPI App)

        Raises:
            Exception: DB DISCONNECT ERROR.

        Returns:
            None (Close DB Connection)
        """

        try:
            log.info("Closing connection to Core Server")
            app.mongodb_client.close()
            get_db_client().close()
            session.close()
            #load_server.on_close()
            log.info("Database connection - closed")
        except Exception as e:
            log.warn("--- CORE CONNECTION ERROR  ---")
            log.warn(e)
            log.warn("--- CORE CONNECTION ERROR  ---")


def create_start_app_handler(app: FastAPI) -> Callable:
    """Decorator to handle app startup event along with DB connection.

    Args:
        app (FastAPI App)

    Returns:
        start_app (DB connected App Object)
    """
    
    async def start_app() -> None:
        await connect_to_db(app)
    return start_app

    
def create_stop_app_handler(app: FastAPI) -> Callable:
    """Decorator to handle app shutdown event after closed DB connection.

    Args:
        app (FastAPI App)

    Returns:
        stop_app (DB disconnect App Object)
    """
    
    async def stop_app() -> None:
        await close_db_connection(app)
    return stop_app
 