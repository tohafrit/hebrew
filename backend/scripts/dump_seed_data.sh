#!/usr/bin/env bash
# Dump content tables from the running DB into data/seed/*.sql
# Usage: ./scripts/dump_seed_data.sh
# Run from the project root (where docker-compose.yml is)

set -euo pipefail

TABLES=(
  levels binyanim skills topics alphabet_letters nikkud
  words word_forms root_families root_family_members example_sentences
  grammar_topics grammar_rules verb_conjugations prepositions collocations
  lessons exercises reading_texts dialogues culture_articles achievement_definitions
  learning_paths
)

SEED_DIR="backend/data/seed"
mkdir -p "$SEED_DIR"

for table in "${TABLES[@]}"; do
  echo "Dumping $table..."
  docker compose exec -T db pg_dump -U ulpan -d ulpan \
    --data-only --column-inserts --table="$table" --no-owner --no-privileges \
    | sed '/^SET /d; /^SELECT pg_catalog.set_config/d; /^--/d; /^$/d; /^\\[a-z]/d' \
    > "$SEED_DIR/${table}.sql"
done

echo ""
echo "Done. Files:"
ls -lh "$SEED_DIR"/*.sql | awk '{print $5, $9}'
