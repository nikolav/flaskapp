
cors_resources = {
  r'/auth'                    : {'origins': '*'},
  r'/graphql'                 : {'origins': '*'},
  r'/webhook_viber_channel.*' : {'origins': '*'},
  r'/webhook.*'               : {'origins': '*'},
}

