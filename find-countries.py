import StringIO import time import datetime
import pycurl import stem.control
# Static exit for us to make 2-hop circuits through. Picking aurora, a
# particularly beefy one...
#
# https://atlas.torproject.org/#details/379FB450010D17078B3766C2273303C358C3A442
EXIT_FINGERPRINT = 'DB19E709C9EDB903F75F2E6CA95C84D637B62A02'
SOCKS_PORT = 9150
CONNECTION_TIMEOUT = 3 # timeout before we give up on a circuit
def query(url): """
    Uses pycurl to fetch a site using the proxy on the SOCKS_PORT. """
output = StringIO.StringIO() query = pycurl.Curl()
    query.setopt(pycurl.URL, url)
query.setopt(pycurl.PROXY, 'localhost')
query.setopt(pycurl.PROXYPORT, SOCKS_PORT) query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME) query.setopt(pycurl.CONNECTTIMEOUT, CONNECTION_TIMEOUT) query.setopt(pycurl.WRITEFUNCTION, output.write)
try:
query.perform()
return output.getvalue()
except pycurl.error as exc:
raise ValueError("Unable to reach %s (%s)" % (url, exc))
def scan(controller, path): """
    Fetch check.torproject.org through the given path of relays, providing back the time it took.
    """
circuit_id = controller.new_circuit(path, await_build = True)
def attach_stream(stream): if stream.status == 'NEW':
controller.attach_stream(stream.id, circuit_id)
controller.add_event_listener(attach_stream, stem.control.EventType.STREAM)
try:
controller.set_conf('__LeaveStreamsUnattached', '1') # leave stream management to us start_time = time.time()
check_page = query('http://ctf.martincarlisle.com/')
if 'flag' in check_page: print check_page
# raise ValueError("Request didn't have the right content")
return time.time() - start_time finally:
controller.remove_event_listener(attach_stream) controller.reset_conf('__LeaveStreamsUnattached')
with stem.control.Controller.from_port() as controller: controller.authenticate()
relay_fingerprints = [desc.fingerprint for desc in controller.get_network_statuses()]

for fingerprint in relay_fingerprints: try:
time_taken = scan(controller, [EXIT_FINGERPRINT,fingerprint]) print('%s => %0.2f seconds' % (fingerprint, time_taken)) exit_relay = controller.get_network_status(fingerprint)
print(" address: %s:%i" % (exit_relay.address, exit_relay.or_port))
print(" fingerprint: %s" % exit_relay.fingerprint)
print(" nickname: %s" % exit_relay.nickname)
print(" locale: %s" % controller.get_info("ip-to-country/%s" % exit_relay.address, 'unknown')) print(datetime.datetime.now())
except Exception as exc:
print('%s => %s' % (fingerprint, exc))
