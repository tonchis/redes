function timeout() {
  pgrep sleep && pkill -9 sleep
  ${*:2} &
  echo "$2 will be killed in $1 seconds if still running"
  sleep $1
  pgrep $2 && pkill -9 $2
}