#!/usr/bin/env bash
# Run the test suite for every service.
#
# Each service exposes its tests as a compose service named "<service>-tests"
# (built from that service's "dev" image stage, behind the "test" profile).
# This script discovers those services by naming convention and runs each one,
# so new services are picked up automatically once they add a "-tests" service.

set -u

# Run from the repository root regardless of where the script is invoked.
cd "$(dirname "$0")/.." || exit 1

mapfile -t services < <(
  docker compose --profile test config --services | grep -E -- '-tests$' | sort
)

if [ "${#services[@]}" -eq 0 ]; then
  echo "No '*-tests' services found."
  exit 0
fi

failed=()
for svc in "${services[@]}"; do
  echo "==================== ${svc} ===================="
  if ! docker compose run --rm --build "${svc}"; then
    failed+=("${svc}")
  fi
  echo
done

if [ "${#failed[@]}" -ne 0 ]; then
  echo "FAILED: ${failed[*]}"
  exit 1
fi

echo "All test suites passed."
