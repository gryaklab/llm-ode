#!/bin/bash

PROBLEM="all"
PORT=8000
export CUDA_VISIBLE_DEVICES=0,1,2,3
MODELS=(
    "Qwen/Qwen3-30B-A3B-Instruct-2507"
    "allenai/Olmo-3.1-32B-Instruct"
    "mistralai/Ministral-3-14B-Instruct-2512"
)

export NCCL_P2P_DISABLE=1

set -euo pipefail

cleanup() {
    echo "Shutting down server..."
    if kill -0 "$SERVER_PID" 2>/dev/null; then
        kill "$SERVER_PID"
        wait "$SERVER_PID" || true
    fi
}

trap cleanup EXIT INT TERM

NUM_GPUS=$(awk -F, '{print NF}' <<< "$CUDA_VISIBLE_DEVICES")

for model in "${MODELS[@]}"; do
    echo "Running experiment using model $model"
    uv run vllm serve $model --seed 42 --tensor_parallel_size=$NUM_GPUS --dtype=bfloat16 --max_num_seqs=64 &
    SERVER_PID=$!

    # Wait until server is ready
    until curl -s http://localhost:$PORT/health >/dev/null; do
        sleep 1
    done

    uv run python main.py \
        --iters 200 \
        --n_islands 4 \
        --island_size 2 \
        --k 8 \
        --b 3 \
        --iters_per_refine 5 \
        --save_iterations 5 50 100 150 200 \
        --results_dir results/llm-ode-${model} \
        --problem "$PROBLEM" \
        --openai_api_base http://localhost:$PORT/v1

    kill $SERVER_PID
    wait $SERVER_PID
done
