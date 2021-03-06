TYPE = 'type'

# controller types
CONTROLLER_TYPE_GAME = 'game'
CONTROLLER_TYPE_INVITE = 'invite'

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
GAME_START_TURN = 'game_start_turn'
GAME_LOAD_MESSAGES = 'game_load_messages'
GAME_LOAD_GAME = 'game_load_game'
GAME_LOAD_MOVES = 'game_load_moves'

# channel message types
GROUP_MESSAGE = 'group.message'
SINGLE_MESSAGE = 'single.message'
ADD_GAME = 'add.game'
REMOVE_GAME = 'remove.game'
CLIENT_SEND = 'send.message'

# client message types
CLIENT_TYPE_ERROR = 'client_error' 
CLIENT_TYPE_LOAD_BOARD = 'load_board'
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
CLIENT_TYPE_UPDATE_TIME = 'update_time'
CLIENT_TYPE_MOVE_RESPONSE = 'move_response'
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
VALID_MOVES = 'valid_moves'
MOVE = 'move'
MOVE_FROM = 'from'
MOVE_TO = 'to'
CHAT_MESSAGE = 'message'
MESSAGE_SENDER = 'sender'
NOTATION = 'notation'
MY_TIME = 'my_time'
OPPONENT_TIME = 'opponent_time'
SPECIAL_MOVES = 'special_moves'
MOVE_TYPE = 'type'
RESULTS = 'results'
WINS = 'wins'
GAMES_PLAYED = 'games_played'
WINNER = 'winner'
USER_ID = 'user_id'
BOARD = 'board'