import * as actions from '../actions/user'

const initialState = {
  authFields: {
    name: '',
    email: '',
    password: ''
  },
  name: null,
  email: null,
  id: null,
  attemptedFetch: false,
  isAuthenticated: false,
  registerResult: null,
  wsInvite: null,
  inviteSender: null,
  search: {
    results: [],
    loading: false,
    value: ''
  },
  selectedUser: null,
  inviteMessage: ''
}

function userReducer(state = initialState, action) {
  switch (action.type) {
    case actions.LOGIN_USER:
      if (!action.id) {
        return { ...state, isAuthenticated: false}
      }
      return { ...state,
        id: action.id,
        email: action.email,
        name: action.name,
        rating: action.rating,
        isAuthenticated: true 
      } 
    case actions.REGISTER_USER:
      return { ...state, registerResult: { success: true }}
    case actions.LOGOUT_USER:
      return { ...state, name: null, email: null, isAuthenticated: false }
    case actions.UPDATE_EMAIL_FIELD:
      return { ...state, authFields: { 
        ...state.authFields,
        email: action.value
      }}
    case actions.UPDATE_PASSWORD_FIELD:
      return { ...state, authFields: { 
        ...state.authFields,
        password: action.value
      }}
    case actions.UPDATE_USERNAME_FIELD:
      return { ...state, authFields: { 
        ...state.authFields,
        name: action.value
      }}
    case actions.CLEAR_AUTH_FIELDS:
      return { ...state, authFields: { name: '', email: '', password: '' } }
    case actions.LOAD_INVITES:
      return { ...state, invites: action.data }
    case actions.SAVE_INVITE:
      return { ...state, wsInvite: action.invite } 
    case actions.SET_INVITE_SENDER:
      return { ...state, inviteSender: action.user}
    case actions.START_SEARCH:
      return { ...state, search: { ...state.search, value: action.value, loading: true } }
    case actions.FINISH_SEARCH:
      return { ...state, search: { ...state.search, results: action.results, loading: false } }
    case actions.SET_INVITE_MESSAGE:
      return { ...state, inviteMessage: action.value}
    case actions.SET_SELECTED_USER:
      return { ...state, selectedUser: action.selectedUser }
    case actions.SET_ATTEMPTED_FETCH:
      return { ...state, attemptedFetch: action.value }
    case actions.SET_HISTORY:
      return state
    default:
      return state
  }
}

export default userReducer