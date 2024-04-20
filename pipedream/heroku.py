import heroku3

heroku_conn = heroku3.from_key('xxx')
app = heroku_conn.apps()['bitcoin-tff']
# stop
app.process_formation()['web'].scale(0)
# start
app.process_formation()['web'].scale(1)
