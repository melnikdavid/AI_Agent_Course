from schemas import SearchArgs

raw = '{"query": "solar"}'
args = SearchArgs.model_validate_json(raw)
print(args.query)
print(SearchArgs.model_json_schema())
