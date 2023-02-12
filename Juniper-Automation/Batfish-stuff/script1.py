from pybatfish.client.commands import bf_session, bf_set_network
from pybatfish.question import bfq
from pybatfish.question.question import load_questions
from rich import print as rprint

BATFISH_ADDRESS = "127.0.0.1"
SNAPSHOT_DIR = "snapshots/test01"
NETWORK_NAME = "test-topology"

bf_session.host = BATFISH_ADDRESS
load_questions()

bf_set_network(NETWORK_NAME)
bf_session.init_snapshot(SNAPSHOT_DIR, name=NETWORK_NAME, overwrite=True)

rprint(bfq.bgpSessionStatus(status="ESTABLISHED").answer().frame())
