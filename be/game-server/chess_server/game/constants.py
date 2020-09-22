TYPE = 'type'
"""
ERROR = 'error'
GAME_ID_PARAM = 'game_id'
ERROR_MSG = 'error_msg'
MOVE = 'move'
MOVE_FROM = 'from'
MOVE_TO = 'to'
CONTENT = 'message'
SENDER = 'sender'
DID_RESIGN = 'did_resign'
GAME_STATUS = 'status'
VALID_MOVES = 'valid_moves'
BOARD = 'board'
MY_COLOUR = 'my_colour'
DID_SUCCEED = 'success'
COLOUR = 'colour'
CHANNEL_NAME = 'channel_name'
MOVE_ERROR = 'move_error'
CLIENT_ERROR = 'client_errors'
USER = 'user'
PLAYER_MOVE = 'move'
RESIGNED = 'resigned'
MY_TURN = 'my_turn'
# constants for group messages

GROUP_MESSAGE_TYPE = 'type'
GROUP_MESSAGE_START_GAME = 'group.start.game'
GROUP_MESSAGE_END_GAME = 'group.end.game'
GROUP_MESSAGE_CHAT_MESSAGE = 'group.chat.message'
GROUP_MESSAGE_RESIGN = 'group.resign'

# constants for regular channel message

MESSAGE_TYPE = 'type'
MESSAGE_ERROR = 'messsage.error'
MESSAGE_SET_UP = 'message.set.up'
MESSAGE_OPPONENT_MOVE_SEND = 'message.opponent.move'
MESSAGE_PLAYER_RESIGN = 'resign'
MESSAGE_START_TURN = 'start_turn'
MESSAGE_END_TURN = 'end_turn'

# constants for sending data to client

CLIENT_MESSAGE_TYPE = 'type'
CLIENT_MESSAGE_START_GAME = 'start_game'
CLIENT_MESSAGE_START_TURN = 'start_turn'
CLIENT_MESSAGE_END_TURN = 'end_turn'
CLIENT_MESSAGE_OPPONENT_MOVE = 'opponent_move'
CLIENT_MESSAGE_MOVE = 'move'
CLIENT_MESSAGE_END_GAME = 'end_game'
CLIENT_MESSAGE_PLAYER_MOVE = 'player_move'
CLIENT_MESSAGE_MY_TURN = 'my_turn'
CLIENT_MESSAGE_RESIGN = 'player_resign'
CLIENT_ERROR = 'client_error'
CLIENT_MESSAGE_CHAT = 'chat_message'
"""
# NEW CONSTANTS BELOW 

# controller types

CONTROLLER_TYPE_GAME = 'game'
CONTROLLER_TYPE_INVITE = 'invite'


WINNER = 'winner'
USER_ID = 'user_id'
WS_LOGIN = 'ws_login'
#controller function names
INVITE_RECEIVED = 'invite_received'
INVITE_UPDATE = 'invite_update'
INVITE_RESPONSE = 'invite_response'

GAME_PLAYERS_UPDATE = 'game_players_update'
GAME_STATUS_UPDATE = 'game_status_update'
GAME_OPPONENT_MOVE = 'game_opponent_move'
GAME_OPPONENT_MESSAGE = 'game_opponent_message'
GAME_MY_MOVE = 'game_my_move'
GAME_MY_MESSAGE = 'game_my_message'
GAME_START_TURN = 'game_start_move'
GAME_LOAD_MESSAGES = 'game_load_messages'
GAME_LOAD_GAME = 'game_load_game'
GAME_LOAD_MOVES = 'game_load_moves'
# channel message types
GROUP_MESSAGE = 'group.message'
SINGLE_MESSAGE = 'single.message'
ADD_GAME = 'add.game'
CLIENT_SEND = 'send.message'
# client message types
CLIENT_TYPE_ERROR = 'client_error' 
CLIENT_TYPE_INVITE_UPDATE = 'invite_update'
CLIENT_TYPE_INVITE_RECEIVED = 'invite_received'
CLIENT_TYPE_INVITE_ACCEPTED = 'invite_accepted'
CLIENT_TYPE_START_TURN = 'start_turn'
CLIENT_TYPE_AUTH_ERROR = 'auth_error'
CLIENT_TYPE_STATUS_UPDATE = 'status_update'
CLIENT_TYPE_LOAD_GAME = 'load_game'
CLIENT_TYPE_LOAD_MOVES = 'load_moves'
CLIENT_TYPE_LOAD_MESSAGES = 'load_messages'
CLIENT_TYPE_NEW_CHAT_MESSAGE = 'opponent_message'
CLIENT_TYPE_OPPONENT_MOVE = 'opponent_move'
CLIENT_TYPE_START_GAME = 'start_game'
CLIENT_TYPE = 'type'


# Fields for data being sent to client
CLIENT_ERROR_MESSAGE = 'message'
CLIENT_STATUS = 'status'
CLIENT_WINNER = 'winner'
CLIENT_LOSER = 'loser'
GAME_ID = 'game_id'
ID = 'id'
CONTENT = 'content'
GAME = 'game'
MOVE_LIST = 'move_list'
INVITE = 'invite'
ACCEPTED = 'accepted'
ME = 'me'
OPPONENT = 'opponent'