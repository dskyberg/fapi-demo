#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            players=dict(type='dict', required=True),
            player_name=dict(type='str'),
            service_name=dict(type='str')
        )
    )
    player = {}
    service = {}

    players = module.params['players']
    player_name = module.params['player_name']
    service_name = module.params['service_name']

    if player_name:
        if player_name in players:
            player = players[player_name]
    if service_name and 'services' in player:
        for s in player['services']:
            if s['name'] == service_name:
                service = s
                break

    result = {}
    result['changed'] = False
    result['player'] = player
    result['service'] = service
    module.exit_json(**result)


if __name__ == "__main__":
    main()