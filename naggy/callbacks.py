import dill
import logging

from naggy import config, slack_client


class Result:
    def __init__(self, data, channel=None):
        if not channel:
            self.channel = config['SLACK_DEFAULT_CHANNEL']
        self.data = data


def process_get_rfr_issues(event):
    logging.info("processing event: get_rfr_issues")
    if not event['type'] == 'message':
        return

    data = dill.loads(event['data'])

    result_format = '({user}) {title} ({url})'
    results = []
    for issue in data:
        result = result_format.format(
            user=issue.user.login,
            title=issue.title,
            url=issue.html_url
        )
        results.append(result)

    results = '\n'.join(results)

    slack_client.send_message(
        config['SLACK_DEFAULT_CHANNEL'], results
    )

    # return Result('\n'.join(results))
