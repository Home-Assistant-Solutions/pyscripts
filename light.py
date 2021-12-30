import io
import yaml

def get_light_state(light_id, scenes_entities):
  for entities in scenes_entities:
    input_selects = [entity for entity in entities if entity.startswith('input_select.')]
    for input_select in input_selects:
      if state.get(input_select) == entities[input_select]['state']:
        state = {
          'state': entities[light_id]['state'],
          'supported_color_modes': entities[light_id]['supported_color_modes']
        }

        if 'brightness' in entities[light_id]:
          state['brightness'] = entities[light_id]['brightness']
        if 'hs_color' in entities[light_id] and not 'color_temp' in entities[light_id]:
          state['hs_color'] = entities[light_id]['hs_color']
        if 'color_temp' in entities[light_id]:
          state['color_temp'] = entities[light_id]['color_temp']
        if 'effect' in entities[light_id]:
          state['effect'] = entities[light_id]['effect']

        return state

  return {}

@service
def turn_on_light(light_id, scenes=None, default_brightness=None):
  if scenes == None:
    with io.open('scenes.yaml', 'r') as scenes_file:
      scenes = yaml.safe_load(scenes_file)

  scenes_entities = [scene['entities'] for scene in scenes if light_id in scene['entities']]
  attr = state.getattr(light_id)
  light_state = get_light_state(light_id, scenes_entities)

  if 'entity_id' in attr and light_state == {}:
    for light in attr['entity_id']:
      turn_on_light(light, scenes, 0)
  else:
    if default_brightness != None:
      if light_state == {}:
        light_state['brightness'] = default_brightness
      if not 'brightness' in light_state and not 'onoff' in light_state['supported_color_modes']:
        light_state['brightness'] = default_brightness
      if 'state' in light_state and light_state['state'] == 'off':
        light_state['brightness'] = 0

    if 'state' in light_state:
      del light_state['state']
    if 'supported_color_modes' in light_state:
      del light_state['supported_color_modes']

    light.turn_on(entity_id=light_id, **light_state)

@service
def turn_off_light(light_id):
  light.turn_off(entity_id=light_id)

@service
def toggle_light(light_id):
  if state.get(light_id) == 'on':
    turn_off_light(light_id)
  else:
    turn_on_light(light_id)