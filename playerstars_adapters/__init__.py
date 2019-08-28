"""Top-level package for PlayerStars Adapters."""

__author__ = """Storm Development Ltda"""
__email__ = 'playerstars@stormsec.com.br'
__version__ = '0.1.0'

from .basic_adapter import BasicDynamodbAdapter
from .console_adapter import ConsoleAdapter
from .duel_adapter import DuelAdapter
from .player_adapter import PlayerAdapter
from .purchase_history_adapter import PurchaseHistoryAdapter
from .region_country_adapter import CountryRegionAdapter
from .region_state_adapter import StateRegionAdapter
from .team_adapter import TeamAdapter
from .user_adapter import UserAdapter
from .user_admin_adapter import UserAdminAdapter

__all__ = ['BasicDynamodbAdapter', 'ConsoleAdapter', 'UserAdapter',
           'PlayerAdapter', 'CountryRegionAdapter', 'StateRegionAdapter',
           'TeamAdapter', 'UserAdminAdapter', 'DuelAdapter',
           'PurchaseHistoryAdapter']
