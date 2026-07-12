#!/usr/bin/env/bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
cd "$HERE"

NO_LOAD=0
while [[ $# -gt 0]]; do
    case "$1" in
        --no-load) NO_LOAD=1; shift ;;
        -h|--help) 
            cat << EOF
Usage: $0 [--no-load]

Options:
    --no-load    Skip loading the Docker image (useful if you have already built it)
    -h, --help   Show this help message and exit
EOF
    exit 0 ;;
        *) echo "Unknown arg: $1" ; exit 2 ;;
    esac
done

IMAGE_TGZ="$HERE/door_inspec.tar.gz"
COMPOSE_FILE="$HERE/docker-compose.yml"

if [[$NO_LOAD -eq 0]]; then
    if [[ -f "$IMAGE_TGZ"]]; then
        echo "Loading Docker image from $IMAGE_TGZ...."
        if command -v docker-compose >/dev/null 2>&1; then
            docker load -i "$IMAGE_TGZ"
        else
        docker load -i "$IMAGE_TGZ"
        fi
    else
        echo "Docker image tarball not found at $IMAGE_TGZ. Skipping load." >&2
    fi
else
    echo "Skipping Docker image load as per --no-load flag."
fi

export SPOT_IP="${SPOT_IP:-192.168.80.3}"

if [[! -f "$COMPOSE_FILE"]]; then
    echo "Docker Compose file not found at $COMPOSE_FILE. Exiting." >&2
    exit 1
fi

if command -v docker-compose >/dev/null 2>&1; then
    DC_CMD=(docker-compose -f "$COMPOSE_FILE")
else
    DC_CMD=(docker compose -f "$COMPOSE_FILE")
fi

echo "Starting Docker Compose services..."
"${DC_CMD[@]}" up -d --remove-orphans

echo "Docker Compose services started successfully. To view logs, run: ${DC_CMD[*]} logs -f" 