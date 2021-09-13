# Troubleshooting

## Zookeeper fails to start: java.io.EOFException

This may be caused after unexpected node problem or something like that, the solution is to start a bash shell on the Zookeeper pod and
delete the last (0 length) log file at /var/lib/zookeeper/log/version-2/
