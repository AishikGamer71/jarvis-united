#!/bin/bash
set -e

echo "Adding Hermes Agent subtree..."
git subtree add --prefix=apps/agent-core/vendor/hermes-agent https://github.com/NousResearch/hermes-agent.git main --squash

echo "Syncing Python dependencies..."
cd apps/agent-core
uv sync
echo "Agent core bootstrap complete!"
