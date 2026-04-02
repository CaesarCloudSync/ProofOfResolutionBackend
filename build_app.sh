#!/usr/bin/env bash

set -e

MODE="$1"

if [[ -z "$MODE" ]]; then
  echo "Usage: ./build_app.sh --local | --prod | --test | --migrate"
  exit 1
fi

artifact_repo="palondomus"
image="proofofresolution"

newv=$(head -c 32 /dev/urandom | sha256sum | cut -d' ' -f1)
export FULL_IMAGE="$artifact_repo/$image:$newv"
export IMAGE=$image
export NEWV=$newv

case "$MODE" in
  --migrate)
    echo "🔧 Running database migrations..."
    docker compose -f docker-compose.local.yml build migrate && docker compose -f docker-compose.local.yml run --rm migrate
    ;;

  --local)
    echo "🔧 Building LOCAL environment..."
    docker compose -f docker-compose.local.yml build web
    docker compose -f docker-compose.local.yml up web
    ;;

  --test)
    echo "🔧 Running Tests..."

    # Clean start
    docker compose -f docker-compose.local.yml down -v --remove-orphans

    # Build both images
    docker compose -f docker-compose.local.yml build web test

    # Start web in background — healthcheck must pass before test container starts
    docker compose -f docker-compose.local.yml up -d web

    echo ""
    echo "========================================="
    echo "           TEST RESULTS"
    echo "========================================="

    # Run tests — depends_on waits for web to be healthy before starting
    docker compose -f docker-compose.local.yml run --rm -T test
    TEST_EXIT_CODE=$?

    echo "========================================="
    if [ $TEST_EXIT_CODE -eq 0 ]; then
      echo "✅ All tests passed."
    else
      echo "❌ Tests FAILED (exit code: $TEST_EXIT_CODE)."
    fi
    echo "========================================="

    # Cleanup
    docker compose -f docker-compose.local.yml down -v --remove-orphans

    exit $TEST_EXIT_CODE
    ;;

  --prod)
    echo "🚀 Building PRODUCTION environment..."

    gcloud auth application-default login

    docker compose build
    docker push $artifact_repo/$image:$newv

    export TF_VAR_image="$artifact_repo/$image:$newv"
    cd infra
    terraform init
    terraform plan
    terraform apply -auto-approve
    cd ..

    if [[ "$2" == "--commit" && -n "$3" ]]; then
      msg="$3"
      git add .
      git commit -m "$msg"
      git push origin -u main:main
    fi

    docker compose -f docker-compose.yml build --build-arg DOCKERFILE=Dockerfile
    docker compose -f docker-compose.yml up
    ;;

  *)
    echo "❌ Unknown option: $MODE"
    echo "Use --local, --test, or --prod"
    exit 1
    ;;
esac