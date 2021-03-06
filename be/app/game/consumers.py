import uuid, random, time, threading
import game.constants as constants
from chess.game import InvalidMoveError
from chess.game import Game as ChessEngine
from chess.piece import Position
from chess.constants import WHITE, BLACK, IN_PROGRESS
from channels.layers import get_channel_layer
import game.serializers as serializers
import user.serializers as user_serializers
from core.models import User, GameInvite, Game, Player, Move, ChatMessage
from channels.db import database_sync_to_async
from channels.auth import login
from channels.consumer import get_handler_name
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


def parse_move(move_json):
    """Parse JSON move and return as Position objects"""
    from_position = Position(move_json[constants.MOVE_FROM][0], move_json[constants.MOVE_FROM][1])
    to_position = Position(move_json[constants.MOVE_TO][0], move_json[constants.MOVE_TO][1])
    return (from_position, to_position)

def game_timeout_callback(game_id, player_id):
    """
    Callback to change game status when a players time
    runs out
    """
    game = Game.objects.get(id=game_id)
    player = Player.objects.get(game=game, id=player_id)
    player.timeout = True
    player.save()
    game.status = Game.GameStatus.TIMEOUT
    game.save()

def cancel_timeout(game_id, player_id):
    """
    Helper func to get timer thread for a player and cancel it
    """
    
    for th in threading.enumerate():
        if (getattr(th, 'game_id', None) == game_id and getattr(th, 'player_id', None) == player_id):
            
            th.cancel()

class ChessConsumer(JsonWebsocketConsumer):

    def connect(self):
        self.accept()
        self.game_controllers = [] 
        self.invite_controller = InviteController(self.scope['user'])
        self.channel_layer = get_channel_layer()
        self.scope['user'].online = True 
        self.scope['user'].channel_name = self.channel_name 
        self.scope['user'].save()
        self.load_active_games()
    
    def load_active_games(self):
        """
        Create game controllers for all active games and 
        load game history into chess engines
        """
        games = Game.objects.filter(
            game_to_user__user=self.scope['user'],
            _status=Game.GameStatus.IN_PROGRESS
        )
        for game in games: 
            game_controller = GameController(game, self.scope['user'], new_game=False)
            game_controller.load_game()
            self.game_controllers.append(game_controller)

    def disconnect(self, code):
        """
        Set user offline to False when disconnecting
        """
        if self.scope['user'].id != None:
            self.scope['user'].online = False
            self.scope['user'].save()

    def get_controller(self, game_id):
        """
        Helper to get correct game controller
        """
        if isinstance(game_id, str):
            game_id = uuid.UUID(game_id)
        for gc in self.game_controllers:
            if gc.game.id == game_id:
                return gc

    def chess_dispatch(self, message):
        """
        Dispatches the message to the controller to handle it 
        """
        type_str = message[constants.TYPE]
        if type_str == constants.WS_LOGIN:
            self.login_user(message[constants.USER_ID])
            return
        if self.scope['user'].id is None: #TODO TEST
            self.send_message({
                constants.CLIENT_TYPE: constants.CLIENT_AUTH_ERROR
            })

        controller_type = type_str.split("_")[0]
        subtype_str = type_str[len(controller_type) + 1:]
        func = None
        if controller_type == constants.CONTROLLER_TYPE_GAME:
            game_controller = self.get_controller(message[constants.GAME_ID])
            if not game_controller:
                self.send_message({
                    constants.CONTENT: {
                        constants.CLIENT_TYPE: constants.CLIENT_TYPE_ERROR,
                        constants.CLIENT_ERROR_MESSAGE: f"Error retrieving game.",
                        constants.GAME_ID: str(message[constants.GAME_ID])
                    }
                })
                return
            func = getattr(game_controller, subtype_str)

        if controller_type == constants.CONTROLLER_TYPE_INVITE:
            func = getattr(self.invite_controller, subtype_str)

        func(**message)

    def receive_json(self, message):
        """
        Dispatch message to correct handling function
        """
        self.chess_dispatch(message)

    def group_message(self, message):
        """
        Dispatch message to correct handling function
        """
        self.chess_dispatch(message[constants.CONTENT])

    def single_message(self, message):
        """
        Dispatch message to correct handling function
        """
        self.chess_dispatch(message[constants.CONTENT])

    def send_message(self, message):
        """
        Send down json message to the client
        """
        self.send_json(message[constants.CONTENT])

    def add_game(self, message):
        """
        Instantiate new Game controller with the game passed
        """
        game_id = message[constants.GAME_ID]
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            print("Error game does not exist.")
        self.game_controllers.append(GameController(game, self.scope['user']))

    def remove_game(self, message):
        """
        Remove game from active game controllers when it has ended
        """
        game_id = message[constants.GAME_ID]
        for gc in self.game_controllers:
            if str(gc.game.id) == game_id:
                self.game_controllers.remove(gc)

class GameController:

    def __init__(self, game, user, new_game=True):
        """
        Initialize game controller
        """
        self.game = game
        self.user = user
        self.chess_engine = ChessEngine()
        self.my_player = Player.objects.get(game=self.game, user=self.user)
        self.opponent = Player.objects.filter(game=self.game).exclude(user=self.user)[0]
        if new_game:
            self.start_game()

    def send_game(self, message_type):
        """
        Send down a start game message to client
        """
        serializer = serializers.GameSerializer(self.game)
        my_player_serializer = serializers.PlayerSerializer(self.my_player)
        opponent_serializer = serializers.PlayerSerializer(self.opponent)
        async_to_sync(get_channel_layer().send)(self.user.channel_name, {
            constants.TYPE: constants.CLIENT_SEND,
            constants.CONTENT: {
                constants.TYPE: message_type,
                constants.GAME: serializer.data,
                constants.ME: my_player_serializer.data,
                constants.OPPONENT: opponent_serializer.data
            }
        })

    def start_game(self, **kwargs):
        """
        Handle start of the game, send down start game message 
        to the client
        """    
        self.send_game(constants.CLIENT_TYPE_START_GAME)
        if self.my_player.colour is WHITE:
            self.my_player.turn = True
            self.my_player.save()

    def load_game(self, **kwargs):
        """
        Send game details down to client
        """
        async_to_sync(get_channel_layer().group_add)(
            self.game.group_channel_name,
            self.user.channel_name
        )
        self.send_game(constants.CLIENT_TYPE_LOAD_GAME)
        self.load_moves()
        self.load_board()
        self.load_messages()
        if self.my_player.turn:
            cancel_timeout(self.game.id, self.my_player.id)
            self.start_turn()

    def load_board(self, **kwargs):
        """
        Send down the positions of pieces on board to client
        """
        async_to_sync(get_channel_layer().send)(self.user.channel_name, {
            constants.TYPE: constants.CLIENT_SEND,
            constants.CONTENT: {
                constants.TYPE: constants.CLIENT_TYPE_LOAD_BOARD,
                constants.BOARD: self.chess_engine.board.format_board(),
                constants.GAME_ID: str(self.game.id)
            }
        })

    def load_moves(self, **kwargs):
        """
        Load moves from db into chess_engine and send each 
        move down to client
        """
        moves = Move.objects.filter(game=self.game).order_by('move_number')
        move_list = []
        for m in moves:
            self.chess_engine.load_move(m) 
            move_from, move_to = m.get_move()
            move_list.append({
                constants.NOTATION: m.notation
            })
        async_to_sync(get_channel_layer().send)(self.user.channel_name, {
            constants.TYPE: constants.CLIENT_SEND,
            constants.CONTENT: {
                constants.TYPE: constants.CLIENT_TYPE_LOAD_MOVES,
                constants.MOVE_LIST: move_list,
                constants.GAME_ID: str(self.game.id)
            } 
        })

    def load_messages(self, **kwargs):
        """
        Load all chat messages from the db, 
        and send down to client
        """
        messages = ChatMessage.objects.filter(game=self.game)
        if not messages:
            return
        serializer = serializers.ChatMessageSerializer(messages, many=True)
        async_to_sync(get_channel_layer().send)(self.user.channel_name, {
            constants.TYPE: constants.CLIENT_SEND,
            constants.CONTENT: {
                constants.TYPE: constants.CLIENT_TYPE_LOAD_MESSAGES,
                constants.CHAT_MESSAGE: serializer.data
            }
        })

    def start_turn(self, **kwargs):
        """
        Send down valid moves from chess engine to the client
        """
        self.my_player.update_time()
        self.my_player.save()
        self.my_player.refresh_from_db()
        self.opponent.refresh_from_db()
        
        self.turn_timer = threading.Timer(
           int(self.my_player.time),
           game_timeout_callback,
           args=[self.game.id, self.my_player.id]
        )
        self.turn_timer.game_id = self.game.id
        self.turn_timer.player_id = self.my_player.id
        
        self.turn_timer.start()
        async_to_sync(get_channel_layer().send)(self.user.channel_name, {
            constants.TYPE: constants.CLIENT_SEND,
            constants.CONTENT: {
                constants.TYPE: constants.CLIENT_TYPE_START_TURN,
                constants.VALID_MOVES: self.chess_engine.format_moves(),
                constants.GAME_ID: str(self.game.id),
                constants.MY_TIME: int(self.my_player.time),
                constants.OPPONENT_TIME: int(self.opponent.time)
            }
        })

    def my_message(self, **kwargs):
        """
        Add message to the db.
        """
        new_message = ChatMessage(
            user=self.user,
            game=self.game,
            message=kwargs[constants.CHAT_MESSAGE]
        )
        new_message.save()
        
    def my_move(self, **kwargs):
        """
        Update the chess engine with the clients move,
        Update the DB with the move
        """
        move_values = kwargs.get(constants.MOVE, None)
        move_from, move_to = parse_move(move_values)
        try: 
            self.chess_engine.player_move(move_from, move_to, colour=self.my_player.colour)
        except InvalidMoveError as ex:
            async_to_sync(get_channel_layer().send)(self.user.channel_name, {
                constants.TYPE: constants.CLIENT_SEND,
                constants.CONTENT: {
                    constants.TYPE: constants.CLIENT_TYPE_ERROR,
                    constants.CONTENT: f"Error: {ex.message}"
                }
            })
        else:
            
            self.turn_timer.cancel()
            self.my_player.refresh_from_db()
            self.my_player.turn = False
            self.my_player.save()
            my_move = Move.objects.save_move(self.chess_engine.history[-1], self.game)
            async_to_sync(get_channel_layer().send)(self.user.channel_name, {
                constants.TYPE: constants.CLIENT_SEND,
                constants.CONTENT: {
                    constants.TYPE: constants.CLIENT_TYPE_MOVE_RESPONSE,
                    constants.NOTATION: my_move.notation,
                    constants.GAME_ID: str(self.game.id)
                }
            })
            if self.chess_engine.status != IN_PROGRESS:
                self.game.refresh_from_db()
                self.game.status = self.chess_engine.status
                self.game.save()
            

    def opponent_message(self, **kwargs):
        """
        Retrieve last message from DB and send down to client
        """
        message_id = kwargs.get(constants.ID, None)
        try:
            new_message = ChatMessage.objects.get(id=message_id)
        except ChatMessage.DoesNotExist:
            print(f'Error: message with id: {message_id} not found')
            return 
        serializer = serializers.ChatMessageSerializer(new_message)
        async_to_sync(get_channel_layer().send)(self.user.channel_name, {
            constants.TYPE: constants.CLIENT_SEND,
            constants.CONTENT: {
                constants.TYPE: constants.CLIENT_TYPE_NEW_CHAT_MESSAGE,
                constants.CHAT_MESSAGE: serializer.data
            }
        })

    def opponent_move(self, **kwargs):
        """
        Update chess_engine with the opponents move
        Send valid moves over the channel
        """
        move_id = kwargs.get(constants.ID, None)
        try:
            last_move = Move.objects.get(id=move_id)
        except Move.DoesNotExist:
            print(f"Error: move with id: {move_id} not found.")
            return

        move_from, move_to = last_move.get_move()
        async_to_sync(get_channel_layer().send)(self.user.channel_name, {
            constants.TYPE: constants.CLIENT_SEND,
            constants.CONTENT: {
                constants.TYPE: constants.CLIENT_TYPE_OPPONENT_MOVE,
                constants.MOVE: {
                    constants.MOVE_FROM: move_from,
                    constants.MOVE_TO: move_to,
                    constants.NOTATION: last_move.notation,
                    constants.MOVE_TYPE: last_move.move_type
                },
                constants.GAME_ID: str(self.game.id)
            }
        })
        
        self.chess_engine.load_move(last_move)
        if self.chess_engine.status == IN_PROGRESS:
            self.my_player.turn = True
            self.my_player.save()
        
    def update_time(self, **kwargs):
        """
        Send down updated time to client
        """
        self.my_player.refresh_from_db()
        self.my_player.update_time()
        self.my_player.save()
        self.opponent.refresh_from_db()
        self.opponent.update_time()
        self.opponent.save()
        async_to_sync(get_channel_layer().send)(self.user.channel_name, {
            constants.TYPE: constants.CLIENT_SEND,
            constants.CONTENT: {
                constants.CLIENT_TYPE: constants.CLIENT_TYPE_UPDATE_TIME,
                constants.MY_TIME: int(self.my_player.time),
                constants.OPPONENT_TIME: int(self.opponent.time),
                constants.GAME_ID: str(self.game.id)   
            }
        })

    def resign(self, **kwargs):
        """
        Handle client sending a resign message
        """
        self.my_player.resigned = True
        self.my_player.save()
        self.game.status = Game.GameStatus.RESIGN
        self.game.save()

    def status_update(self, **kwargs):
        """
        Fetch game results from DB and send over channel for 
        client
        """
        self.game.refresh_from_db()
        
        self.my_player.refresh_from_db()
        
        cancel_timeout(self.game.id, self.my_player.id)
        async_to_sync(get_channel_layer().send)(self.user.channel_name, {
            constants.TYPE: constants.CLIENT_SEND,
            constants.CONTENT: {
                constants.CLIENT_TYPE: constants.CLIENT_TYPE_STATUS_UPDATE,
                constants.CLIENT_STATUS: self.game.status,
                constants.CLIENT_WINNER: self.my_player.winner,
                constants.GAME_ID: str(self.game.id)     
            }
        })

        async_to_sync(get_channel_layer().send)(self.user.channel_name, {
            constants.TYPE: constants.REMOVE_GAME,
            constants.GAME_ID: str(self.game.id) 
        })


class InviteController:

    def __init__(self, user):
        self.me = user

    def received(self, **kwargs):
        """
        Load the received invite from DB and send down to the client
        """
        invite_id = kwargs.get(constants.ID, None)
        try:
            invite = GameInvite.objects.get(id=invite_id)
        except GameInvite.DoesNotExist:
            print(f"Error: invite with id: {invite_id} not found")
            return 
        serializer = user_serializers.GameInviteReadSerializer(invite)
        async_to_sync(get_channel_layer().send)(self.me.channel_name, {
            constants.TYPE: constants.CLIENT_SEND,
            constants.CONTENT: {
                constants.CLIENT_TYPE: constants.CLIENT_TYPE_INVITE_RECEIVED,
                constants.INVITE: serializer.data
            }
        })
    def response(self, **kwargs):
        """
        Handle client response to invite
        """
        invite_id = kwargs.get(constants.ID)
        try:
            invite = GameInvite.objects.get(id=invite_id)
        except:
            print(f"Error: invite with id: {invite_id} not found")
            async_to_sync(get_channel_layer().send)(self.me.channel_name, {
                constants.TYPE: constants.CLIENT_SEND,
                constants.CONTENT: {
                    constants.CLIENT_TYPE: constants.CLIENT_TYPE_ERROR,
                    constants.CLIENT_ERROR_MESSAGE: 'Error responding to invite.'
                }
            })
            return 
        response = kwargs.get(constants.ACCEPTED)
        if response:
            invite.accepted = True
        else:
            invite.declined = True
        invite.save()

    def update(self, **kwargs):
        """
        Send invite update over channel layer for client
        """
        invite_id = kwargs.get(constants.ID)
        try:
            invite = GameInvite.objects.get(id=invite_id)
        except:
            print(f"Error: invite with id: {invite_id} not found")
            return 
        serializer = user_serializers.GameInviteReadSerializer(invite)
        async_to_sync(get_channel_layer().send)(self.me.channel_name, {
            constants.TYPE: constants.CLIENT_SEND,
            constants.CONTENT: {
                constants.TYPE: constants.CLIENT_TYPE_INVITE_UPDATE,
                constants.INVITE: serializer.data
            }
        })
        
        if invite.accepted:
            game = Game.objects.create(
                group_channel_name=f"group_{invite.game_id}"
            )
            async_to_sync(get_channel_layer().group_add)(
                game.group_channel_name,
                invite.from_user.channel_name
            )
            async_to_sync(get_channel_layer().group_add)(
                game.group_channel_name,
                invite.to_user.channel_name
            )
            self.create_players(
                invite.from_user,
                invite.to_user,
                game
            )
            game.started = True
            game.save()

    def create_players(self, user1, user2, game):
        """
        Creates player objects for the given game
        """
        random_colour = bool(random.randint(0, 1))
        Player.objects.create(
            user=user1,
            game=game,
            winner=False,
            colour=random_colour
        )
        Player.objects.create(
            user=user2,
            game=game,
            winner=False,
            colour=not random_colour
        )