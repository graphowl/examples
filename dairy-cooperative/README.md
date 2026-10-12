# Dairy cooperative: synthetic sample data

[`dairy-coop.sql`](dairy-coop.sql) creates a `dairy` schema in PostgreSQL for a **fictional** dairy cooperative. It is the data behind the GraphOWL live demo, generated deterministically, with no real people or businesses in it.

| Area | Tables |
|---|---|
| Producers | `farm`, `herd`, `breed` |
| Collection | `tanker_run`, `milk_lot` |
| Quality | `quality_test`, `test_parameter`, `milk_grade` |
| Production | `production_batch`, `batch_lot`, `product`, `product_category` |
| Sales | `sale`, `retailer` |
| Safety | `cold_chain_reading`, `storage_condition`, `recall_class` |

The thresholds in the data (somatic cell count limit, chilled maximum temperature and so on) are example parameters, not regulatory values.

## Load it

```bash
createdb dairy_demo
psql dairy_demo -f dairy-coop.sql
```

## Use it with GraphOWL

1. Connect the database as a source, using a **read-only** role.
2. Let GraphOWL scan its tables, columns and keys and propose an ontology; review and approve it.
3. Load a bounded sample of rows as instances of the approved classes.
4. Ask questions of the graph, for example with [`../sparql-python/query.py`](../sparql-python/query.py).

Questions worth asking of this data: which milk lots failed a quality test, which production batches contain those lots, and which retailers received those batches.
