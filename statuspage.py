from errbot import BotPlugin, botcmd, arg_botcmd
import requests

CONFIG_TEMPLATE = {'API_TOKEN': '',
                   'SERVER': ''}

class StatusPage(BotPlugin):
    """
    Talks to a Cachet status server
    """

    def get_configuration_template(self):
        return CONFIG_TEMPLATE

    def check_configuration(self, config):
        if type(config) != dict:
            raise Exception("Configuration must be a dict.")
        if "API_TOKEN" not in config:
            raise Exception("API_TOKEN must be specified.")
        if "SERVER" not in config:
            raise Exception("SERVER must be specified.")

    def activate(self):
        self.log.debug("Activating Status...")
        if not self.config:
            self.log.info('Status is not configured. Forbid activation.')
            return
        
        global apiUrl 
        apiUrl = "http://{}/api/v1".format(self.config["SERVER"])
        self.log.debug("Cachet server URL: {}".format(apiUrl))

        global apiToken
        apiToken = self.config['API_TOKEN']
        self.log.debug("API token: {}".format(apiToken))

        super().activate()

    @botcmd(split_args_with=None)
    def list_incidents(self, msg, args):
        """Lists all incidents"""
        self.log.debug("Getting incidents")
        url = apiUrl + '/incidents'
        self.log.debug("Using GET URL: {}".format(url))
        
        t = requests.get(url)
        for d in t.json()['data']:
            yield("{}: {} - {} ({})".format(str(d['id']), str(d['name']), str(d['human_status']), str(d['updated_at'])))

    @botcmd(split_args_with=None)
    def list_components(self, msg, args):
        """Lists all components"""
        self.log.debug("Getting components")
        url = apiUrl + '/components'
        self.log.debug("Using GET URL: {}".format(url))
        
        t = requests.get(url)
        for d in t.json()['data']:
            yield("{}: {} - {} **{}**".format(str(d['id']), str(d['name']), str(d['description']), str(d['status_name'])))

    @arg_botcmd('visible', type=int, default=1)
    @arg_botcmd('status', type=int, default=1)
    @arg_botcmd('message', type=str)
    @arg_botcmd('name', type=str, admin_only=True)
    def create_incident(self, msg, name=None, message=None, status=None, visible=None, admin_only=True):
        """Creates a new incident
        !create incident --name <name> --message <mess> --status [0-4]
        """
        url = apiUrl + '/incidents'
        self.log.debug("Using POST URL: {}".format(url))
        self.log.debug("Creating a new incident")
        self.log.debug("Name   : {}".format(name))
        self.log.debug("Message: {}".format(message))
        self.log.debug("Status : {}".format(status))
        self.log.debug("Visible: {}".format(visible))

        payload = {'name': name, 'message': message, 'status': status, 'visible': visible}
        
        self.log.debug("Data   : {}".format(payload))
        r = requests.post(url, data=payload, headers={'X-Cachet-Token': apiToken})
        yield "Received HTTP response: ```{}```".format(r.status_code)
        self.log.debug(r.text)
        yield "See http://{}/dashboard/incidents for details".format(self.config["SERVER"])
        
