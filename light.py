import io
import yaml

def get_light_state(light_id):
  with io.open('scenes.yaml', 'r') as scenes_file:
    scenes = yaml.safe_load(scenes_file)
    scenes_entities = [scene['entities'] for scene in scenes if light_id in scene['entities']]

    for entities in scenes_entities:
      input_selects = [entity for entity in entities if entity.startswith('input_select.')]
      for input_select in input_selects:
        if state.get(input_select) == entities[input_select]['state']:
          return {key: entities[light_id][key] for key in [
            'brightness',
            'hs_color',
            'color_temp',
            'effect'
          ] if key in entities[light_id]}

  return {}

@service
def turn_on_light(light_id):
  attr = state.getattr(light_id)
  light_state = get_light_state(light_id)

  if 'entity_id' in attr and light_state != {}:
    log.info(attr['entity_id'])
    for light in attr['entity_id']:
      turn_on_light(light)
  else:
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