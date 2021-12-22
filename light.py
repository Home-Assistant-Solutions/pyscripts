import subprocess
import yaml

@service
def turn_on_light(light_id):
  scenes = yaml.safe_load(subprocess.check_output(["cat", "scenes.yaml"]))
  scenes_with_light = [scene for scene in scenes if light_id in scene['entities']]

  for scene in scenes_with_light:
    input_selects = [entity for entity in scene['entities'] if entity.startswith('input_select.')]
    for input_select in input_selects:
      if state.get(input_select) == scene['entities'][input_select]['state']:
        light_state = scene['entities'][light_id]
        params = {}
        if 'brightness' in light_state:
          params['brightness'] = light_state['brightness']
        if 'hs_color' in light_state:
          params['hs_color'] = light_state['hs_color']
        if 'color_temp' in light_state:
          params['color_temp'] = light_state['color_temp']
        if 'effect' in light_state:
          params['effect'] = light_state['effect']
        light.turn_on(entity_id=light_id, **params)
        return

  light.turn_on(entity_id=light_id)

@service
def turn_off_light(light_id):
  light.turn_off(entity_id=light_id)

@service
def toggle_light(light_id):
  if state.get(light_id) == 'on':
    turn_off_light(light_id)
  else:
    turn_on_light(light_id)