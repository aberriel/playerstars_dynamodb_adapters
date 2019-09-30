"""Top-level package for PlayerStars Adapters."""

__author__ = """Storm Development Ltda"""
__email__ = 'playerstars@stormsec.com.br'
__version__ = '0.1.1'

from .basic_adapter import BasicDynamodbAdapter
from .console_adapter import ConsoleAdapter
from .duel_adapter import DuelAdapter
from .player_adapter import PlayerAdapter
from .region_country_adapter import CountryRegionAdapter
from .region_state_adapter import StateRegionAdapter
from .team_adapter import TeamAdapter
from .user_admin_adapter import UserAdminAdapter
from .product_adapter import ProductAdapter

__all__ = [
    'BasicDynamodbAdapter',
    'ConsoleAdapter',
    'PlayerAdapter',
    'CountryRegionAdapter',
    'StateRegionAdapter',
    'TeamAdapter',
    'UserAdminAdapter',
    'DuelAdapter',
    'ProductAdapter'
]
