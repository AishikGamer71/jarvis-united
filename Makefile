.PHONY: install dev build test clean

install:
	pnpm install
	cd engine && pip install -r requirements.txt

dev:
	pnpm turbo run dev

build:
	pnpm turbo run build

test:
	cd engine && pytest tests/

clean:
	rm -rf node_modules
	rm -rf apps/**/node_modules
	rm -rf packages/**/node_modules
	rm -rf out dist .next
