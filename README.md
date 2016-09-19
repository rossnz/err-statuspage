# err-statuspage

A plugin for [Err](http://github.com/gbin/err) which lets you interact with a [Cachet](https://cachethq.io) server. Currently this plugin lets you :

* list components
* list incidents
* create new incidents

## Config

The plugin needs to know:

* the location of your Cachet installation (`SERVER`)
* your API credentials (`API_TOKEN`)

You can configure your Errbot for this plugin like this:
`!config statuspage { 'URL': 'https://status.mydomain.com', 'API_TOKEN': 'abc123'}`

## Licence

Released into public domain. 
