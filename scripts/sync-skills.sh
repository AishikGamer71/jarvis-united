#!/bin/bash
set -e

echo "Syncing Hermes skills..."
hermes skill sync hermes --category all

echo "Installing OpenClaw skills..."
hermes skill install openclaw:*

echo "Skills sync complete!"
