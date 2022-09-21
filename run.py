import requests


def run():
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'token <TOKEN>',
    }

    data = '{"event_type": "class_1_2"}'

    response = requests.post(f'https://api.github.com/repos/inannan423/get_class_push/dispatches', headers=headers,
                             data=data)


# 云函数入口
def main_handler(event, context):
    return run()