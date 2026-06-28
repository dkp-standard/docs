<!-- AUTO-GENERATED — edit docs/schemas/v1/*.json, then run build_spec.py -->
## Appendix B — JSON Schemas (Normative)

The schemas in this appendix are normative. Conformant DKP bundles MUST produce assets that validate against these schemas. Conformant processors MUST reject assets that fail validation.

Schemas use [JSON Schema Draft 2020-12](https://json-schema.org/specification).

### B.1 `ontology.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/ontology.json",
  "title": "DKP Ontology",
  "type": "object",
  "required": [
    "entity_types"
  ],
  "properties": {
    "entity_types": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "id",
          "name",
          "description",
          "attributes"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "name": {
            "type": "string",
            "minLength": 1
          },
          "description": {
            "type": "string",
            "minLength": 1
          },
          "attributes": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "relationships": {
            "type": "array",
            "items": {
              "type": "object",
              "required": [
                "name",
                "target_type"
              ],
              "properties": {
                "name": {
                  "type": "string"
                },
                "target_type": {
                  "type": "string"
                },
                "cardinality": {
                  "type": "string",
                  "enum": [
                    "one-to-one",
                    "one-to-many",
                    "many-to-many"
                  ]
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### B.2 `glossary.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/glossary.json",
  "title": "DKP Glossary",
  "type": "object",
  "required": [
    "terms"
  ],
  "properties": {
    "terms": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "id",
          "term",
          "definition"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "term": {
            "type": "string",
            "minLength": 1
          },
          "definition": {
            "type": "string",
            "minLength": 1
          },
          "aliases": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "related_terms": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "source_ref": {
            "type": "string"
          },
          "ttl_days": {
            "type": "integer",
            "minimum": 1
          },
          "review_date": {
            "type": "string",
            "format": "date"
          },
          "stability": {
            "type": "string",
            "enum": [
              "stable",
              "volatile",
              "experimental"
            ]
          },
          "audience": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        }
      }
    }
  }
}
```

### B.3 `constraints.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/constraints.json",
  "title": "DKP Constraints",
  "type": "object",
  "required": [
    "edge_cases",
    "anti_patterns",
    "hard_limits"
  ],
  "properties": {
    "edge_cases": {
      "$ref": "#/$defs/constraintArray"
    },
    "anti_patterns": {
      "$ref": "#/$defs/constraintArray"
    },
    "hard_limits": {
      "$ref": "#/$defs/constraintArray"
    }
  },
  "$defs": {
    "constraintArray": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "id",
          "title",
          "description"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "title": {
            "type": "string",
            "minLength": 1
          },
          "description": {
            "type": "string",
            "minLength": 1
          },
          "source_ref": {
            "type": "string"
          },
          "ttl_days": {
            "type": "integer",
            "minimum": 1
          },
          "review_date": {
            "type": "string",
            "format": "date"
          },
          "stability": {
            "type": "string",
            "enum": [
              "stable",
              "volatile",
              "experimental"
            ]
          },
          "audience": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        }
      }
    }
  }
}
```

### B.4 `rules.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/rules.json",
  "title": "DKP Rules",
  "type": "object",
  "required": [
    "rules"
  ],
  "properties": {
    "rules": {
      "type": "array",
      "minItems": 2,
      "items": {
        "type": "object",
        "required": [
          "id",
          "title",
          "description",
          "polarity"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "title": {
            "type": "string",
            "minLength": 1
          },
          "description": {
            "type": "string",
            "minLength": 1
          },
          "polarity": {
            "type": "string",
            "enum": [
              "affirmative",
              "prohibitive"
            ]
          },
          "source_ref": {
            "type": "string"
          },
          "ttl_days": {
            "type": "integer",
            "minimum": 1
          },
          "review_date": {
            "type": "string",
            "format": "date"
          },
          "stability": {
            "type": "string",
            "enum": [
              "stable",
              "volatile",
              "experimental"
            ]
          },
          "audience": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        }
      }
    }
  },
  "allOf": [
    {
      "properties": {
        "rules": {
          "contains": {
            "properties": {
              "polarity": {
                "const": "affirmative"
              }
            }
          }
        }
      }
    },
    {
      "properties": {
        "rules": {
          "contains": {
            "properties": {
              "polarity": {
                "const": "prohibitive"
              }
            }
          }
        }
      }
    }
  ]
}
```

### B.5 `decision_trees.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/decision_trees.json",
  "title": "DKP Decision Trees",
  "type": "object",
  "required": [
    "trees"
  ],
  "properties": {
    "trees": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "id",
          "title",
          "description",
          "root"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "title": {
            "type": "string",
            "minLength": 1
          },
          "description": {
            "type": "string",
            "minLength": 1
          },
          "root": {
            "$ref": "#/$defs/node"
          }
        }
      }
    }
  },
  "$defs": {
    "node": {
      "type": "object",
      "required": [
        "question"
      ],
      "properties": {
        "question": {
          "type": "string",
          "minLength": 1
        }
      },
      "oneOf": [
        {
          "required": [
            "answer"
          ],
          "properties": {
            "answer": {
              "type": "string",
              "minLength": 1
            }
          },
          "not": {
            "required": [
              "branches"
            ]
          }
        },
        {
          "required": [
            "branches"
          ],
          "properties": {
            "branches": {
              "type": "array",
              "minItems": 1,
              "items": {
                "type": "object",
                "required": [
                  "condition",
                  "next"
                ],
                "properties": {
                  "condition": {
                    "type": "string"
                  },
                  "next": {
                    "$ref": "#/$defs/node"
                  }
                }
              }
            }
          },
          "not": {
            "required": [
              "answer"
            ]
          }
        }
      ]
    }
  }
}
```

### B.6 `retrieval_chunks.jsonl` Line Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/retrieval_chunk.json",
  "title": "DKP Retrieval Chunk",
  "type": "object",
  "required": [
    "id",
    "title",
    "chunk_text",
    "tags",
    "source_ref"
  ],
  "properties": {
    "id": {
      "type": "string",
      "minLength": 1
    },
    "title": {
      "type": "string",
      "minLength": 1
    },
    "chunk_text": {
      "type": "string",
      "minLength": 1
    },
    "tags": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "source_ref": {
      "type": "string",
      "minLength": 1
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "summary": {
      "type": "string",
      "minLength": 1
    },
    "embedding_model": {
      "type": "string",
      "minLength": 1
    },
    "token_count": {
      "type": "integer",
      "minimum": 1
    },
    "retrieval_priority": {
      "type": "string",
      "enum": [
        "critical",
        "high",
        "normal",
        "low"
      ]
    },
    "asset_refs": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "ttl_days": {
      "type": "integer",
      "minimum": 1
    },
    "review_date": {
      "type": "string",
      "format": "date"
    },
    "stability": {
      "type": "string",
      "enum": [
        "stable",
        "volatile",
        "experimental"
      ]
    },
    "audience": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  }
}
```

### B.7 `eval_set.jsonl` Line Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/eval_entry.json",
  "title": "DKP Eval Entry",
  "type": "object",
  "required": [
    "query",
    "expected_dimensions",
    "critical_must_include",
    "scoring_rubric",
    "version_meta"
  ],
  "properties": {
    "query": {
      "type": "string",
      "minLength": 1
    },
    "expected_dimensions": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "critical_must_include": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "scoring_rubric": {
      "type": "string",
      "minLength": 1
    },
    "version_meta": {
      "type": "object",
      "required": [
        "prompt_hash",
        "model_version",
        "dataset_version"
      ],
      "properties": {
        "prompt_hash": {
          "type": "string",
          "minLength": 1
        },
        "model_version": {
          "type": "string",
          "minLength": 1
        },
        "dataset_version": {
          "type": "string",
          "minLength": 1
        }
      }
    }
  }
}
```

### B.8 OKF Concept File Frontmatter Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/concept_frontmatter.json",
  "title": "DKP OKF Concept Frontmatter",
  "type": "object",
  "required": [
    "type",
    "title",
    "description",
    "tags",
    "timestamp"
  ],
  "properties": {
    "type": {
      "type": "string",
      "enum": [
        "DomainTerm",
        "DomainRule",
        "Constraint",
        "DecisionProcedure",
        "KnowledgeChunk",
        "EntityType",
        "EvalCase"
      ]
    },
    "title": {
      "type": "string",
      "minLength": 1
    },
    "description": {
      "type": "string",
      "minLength": 1
    },
    "tags": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "dkp_domain": {
      "type": "string",
      "minLength": 1
    },
    "dkp_pack": {
      "type": "string",
      "minLength": 1
    },
    "source_ref": {
      "type": "string"
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "ttl_days": {
      "type": "integer",
      "minimum": 1
    },
    "review_date": {
      "type": "string",
      "format": "date"
    },
    "stability": {
      "type": "string",
      "enum": [
        "stable",
        "volatile",
        "experimental"
      ]
    },
    "audience": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "asset_refs": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "dkp_locale": {
      "type": "string"
    }
  },
  "if": {
    "properties": {
      "type": {
        "const": "KnowledgeChunk"
      }
    }
  },
  "then": {},
  "else": {
    "properties": {
      "confidence": false
    }
  }
}
```

### B.9 `knowledge_graph.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/knowledge_graph.json",
  "title": "DKP Knowledge Graph",
  "type": "object",
  "required": [
    "nodes",
    "edges"
  ],
  "properties": {
    "nodes": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "id",
          "type"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "type": {
            "type": "string",
            "enum": [
              "DomainTerm",
              "DomainRule",
              "Constraint",
              "DecisionProcedure",
              "KnowledgeChunk",
              "EntityType",
              "EvalCase"
            ]
          }
        }
      }
    },
    "edges": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "from",
          "to",
          "relation"
        ],
        "properties": {
          "from": {
            "type": "string",
            "minLength": 1
          },
          "to": {
            "type": "string",
            "minLength": 1
          },
          "relation": {
            "type": "string",
            "enum": [
              "requires",
              "contradicts",
              "elaborates",
              "supersedes",
              "part-of",
              "depends-on",
              "see-also",
              "measured-by",
              "defined-by",
              "specializes"
            ]
          },
          "weight": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0
          }
        }
      }
    }
  }
}
```

### B.10 `taxonomy.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/taxonomy.json",
  "title": "DKP Taxonomy Alignment",
  "type": "object",
  "required": [
    "mappings"
  ],
  "properties": {
    "concept_scheme": {
      "type": "object",
      "properties": {
        "uri": {
          "type": "string"
        },
        "skos_type": {
          "type": "string"
        },
        "dc_title": {
          "type": "string"
        },
        "dc_creator": {
          "type": "string"
        }
      }
    },
    "mappings": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "dkp_id"
        ],
        "properties": {
          "dkp_id": {
            "type": "string",
            "minLength": 1
          },
          "skos_exactMatch": {
            "type": "string"
          },
          "skos_closeMatch": {
            "type": "string"
          },
          "schema_org_type": {
            "type": "string"
          },
          "wikidata": {
            "type": "string"
          }
        }
      }
    }
  }
}
```

### B.11 `assets.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/assets.json",
  "title": "DKP Assets",
  "type": "object",
  "required": [
    "assets"
  ],
  "properties": {
    "assets": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "id",
          "type",
          "path",
          "source_ref"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "type": {
            "type": "string",
            "enum": [
              "image",
              "table",
              "audio",
              "video"
            ]
          },
          "path": {
            "type": "string",
            "minLength": 1
          },
          "source_ref": {
            "type": "string",
            "minLength": 1
          },
          "alt_text": {
            "type": "string",
            "minLength": 1
          },
          "caption": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "columns": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "transcript": {
            "type": "string"
          }
        },
        "allOf": [
          {
            "if": {
              "properties": {
                "type": {
                  "const": "image"
                }
              },
              "required": [
                "type"
              ]
            },
            "then": {
              "required": [
                "alt_text"
              ]
            }
          },
          {
            "if": {
              "properties": {
                "type": {
                  "const": "table"
                }
              },
              "required": [
                "type"
              ]
            },
            "then": {
              "required": [
                "columns"
              ]
            }
          },
          {
            "if": {
              "properties": {
                "type": {
                  "not": {
                    "const": "table"
                  }
                }
              },
              "required": [
                "type"
              ]
            },
            "then": {
              "properties": {
                "columns": false
              }
            }
          },
          {
            "if": {
              "properties": {
                "type": {
                  "not": {
                    "enum": [
                      "audio",
                      "video"
                    ]
                  }
                }
              },
              "required": [
                "type"
              ]
            },
            "then": {
              "properties": {
                "transcript": false
              }
            }
          }
        ]
      }
    }
  }
}
```

### B.12 `cross_refs.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/cross_refs.json",
  "title": "DKP Cross-Pack References",
  "type": "object",
  "required": [
    "cross_refs"
  ],
  "properties": {
    "cross_refs": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "local_id",
          "remote_pack",
          "remote_id",
          "relation"
        ],
        "properties": {
          "local_id": {
            "type": "string",
            "minLength": 1
          },
          "remote_pack": {
            "type": "string",
            "minLength": 1
          },
          "remote_id": {
            "type": "string",
            "minLength": 1
          },
          "relation": {
            "type": "string",
            "enum": [
              "requires",
              "contradicts",
              "elaborates",
              "supersedes",
              "part-of",
              "depends-on",
              "see-also",
              "measured-by",
              "defined-by",
              "specializes"
            ]
          }
        }
      }
    }
  }
}
```

### B.13 `eval_results/eval_summary.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/eval_summary.json",
  "title": "DKP Eval Summary",
  "type": "object",
  "required": [
    "last_run_date",
    "pack_version",
    "model",
    "mean_delta",
    "pass_rate",
    "gate7_pass"
  ],
  "properties": {
    "last_run_date": {
      "type": "string",
      "format": "date-time"
    },
    "pack_version": {
      "type": "string"
    },
    "model": {
      "type": "string"
    },
    "mean_delta": {
      "type": "number",
      "minimum": -1.0,
      "maximum": 1.0
    },
    "pass_rate": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "gate7_pass": {
      "type": "boolean"
    }
  }
}
```

### B.14 `machine/mcp_manifest.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_manifest.json",
  "title": "DKP MCP Manifest",
  "type": "object",
  "required": [
    "schema_version",
    "name",
    "pack_version",
    "resources",
    "tools",
    "generated_at"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "const": "1.0"
    },
    "name": {
      "type": "string",
      "minLength": 1
    },
    "pack_version": {
      "type": "string",
      "pattern": "^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$"
    },
    "resources": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "uri",
          "name",
          "description",
          "mime_type"
        ],
        "properties": {
          "uri": {
            "type": "string",
            "minLength": 1
          },
          "name": {
            "type": "string",
            "minLength": 1
          },
          "description": {
            "type": "string"
          },
          "mime_type": {
            "type": "string"
          },
          "total_count": {
            "type": "integer",
            "minimum": 0
          },
          "supports_pagination": {
            "type": "boolean",
            "description": "Whether this listing resource supports cursor + limit query parameters."
          }
        }
      }
    },
    "tools": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "name",
          "description",
          "inputSchema"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "inputSchema": {
            "type": "object"
          }
        }
      }
    },
    "generated_at": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

### B.15 `inject` Tool Input Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_tool_inject.json",
  "title": "inject Tool Input",
  "type": "object",
  "properties": {
    "scope": {
      "type": "string",
      "enum": [
        "system-prompt",
        "full",
        "minimal",
        "chunks"
      ],
      "default": "system-prompt",
      "description": "Content scope to include in the context block."
    },
    "format": {
      "type": "string",
      "enum": [
        "markdown",
        "xml",
        "json"
      ],
      "default": "markdown",
      "description": "Wrapping format for the returned context block."
    },
    "max_tokens": {
      "type": "integer",
      "minimum": 1,
      "description": "Token budget cap for the returned content."
    }
  }
}
```

### B.16 `search` Tool Input Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_tool_search.json",
  "title": "search Tool Input",
  "type": "object",
  "required": [
    "query"
  ],
  "properties": {
    "query": {
      "type": "string",
      "minLength": 1,
      "description": "Full-text search query (BM25)"
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100,
      "default": 10,
      "description": "Maximum number of results to return"
    },
    "asset_types": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "chunks",
          "terms",
          "rules",
          "constraints",
          "eval-cases",
          "assets",
          "entity-types",
          "decision-trees"
        ]
      },
      "description": "Asset types to include in search. If absent, searches all types."
    }
  }
}
```

### B.17 `chunk` Tool Input Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_tool_chunk.json",
  "title": "chunk Tool Input",
  "type": "object",
  "required": [
    "id"
  ],
  "properties": {
    "id": {
      "type": "string",
      "description": "Chunk ID to retrieve"
    }
  }
}
```

### B.18 `get` Tool Input Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_tool_get.json",
  "title": "get Tool Input",
  "type": "object",
  "required": [
    "asset_type"
  ],
  "properties": {
    "asset_type": {
      "type": "string",
      "enum": [
        "term",
        "rule",
        "chunk",
        "constraint",
        "entity",
        "eval",
        "graph",
        "cross-ref",
        "system-prompt"
      ],
      "description": "Asset type to retrieve"
    },
    "id": {
      "type": "string",
      "description": "Asset ID or title substring to filter by. Omit to get all assets of this type."
    },
    "by_id": {
      "type": "boolean",
      "default": false,
      "description": "When true, match id exactly instead of substring-matching on title."
    }
  }
}
```

### B.19 `list_procedures` Tool Input Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_tool_list_procedures.json",
  "title": "list_procedures Tool Input",
  "type": "object",
  "properties": {}
}
```

### B.20 `run_procedure` Tool Input Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_tool_run_procedure.json",
  "title": "run_procedure Tool Input",
  "type": "object",
  "required": [
    "procedure_id"
  ],
  "properties": {
    "procedure_id": {
      "type": "string",
      "description": "Procedure ID (stem name, e.g. \"calculate-tdee\")"
    },
    "input": {
      "type": "object",
      "description": "JSON input passed to the procedure (default: {})"
    },
    "timeout_ms": {
      "type": "integer",
      "description": "Wall-clock timeout override in milliseconds"
    }
  }
}
```

### B.21 MCP Resource Response Envelope Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_response.json",
  "title": "DKP MCP Resource Response Envelope",
  "type": "object",
  "required": [
    "pack",
    "pack_version",
    "resource_type",
    "content",
    "retrieval_metadata"
  ],
  "properties": {
    "pack": {
      "type": "string",
      "description": "Pack name from manifest.json"
    },
    "pack_version": {
      "type": "string",
      "description": "Pack version from manifest.json"
    },
    "resource_type": {
      "type": "string",
      "description": "DKP resource type (\u00a716.1)"
    },
    "resource_id": {
      "type": "string",
      "description": "Resource ID. OPTIONAL for singleton resources."
    },
    "content": {
      "description": "The DKP asset payload. Schema varies by resource_type."
    },
    "next_cursor": {
      "type": [
        "string",
        "null"
      ],
      "description": "Pagination cursor for the next page of results. Present only on listing responses when pagination is supported. null when all results have been returned."
    },
    "retrieval_metadata": {
      "type": "object",
      "required": [
        "retrieved_at"
      ],
      "properties": {
        "score": {
          "type": [
            "number",
            "null"
          ],
          "description": "BM25 relevance score for search-driven retrievals. null for direct fetches."
        },
        "retrieved_at": {
          "type": "string",
          "format": "date-time",
          "description": "ISO-8601 timestamp of retrieval"
        }
      }
    }
  }
}
```

### B.22 `manifest.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/manifest.json",
  "title": "DKP Manifest",
  "type": "object",
  "required": [
    "spec",
    "name",
    "version",
    "domain",
    "audience",
    "intended_use",
    "known_limitations",
    "update_date",
    "compatibility"
  ],
  "properties": {
    "spec": {
      "type": "string",
      "pattern": "^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$"
    },
    "name": {
      "type": "string",
      "minLength": 1
    },
    "version": {
      "type": "string",
      "pattern": "^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$"
    },
    "domain": {
      "type": "string",
      "minLength": 1
    },
    "audience": {
      "type": "string",
      "minLength": 1
    },
    "intended_use": {
      "type": "string",
      "minLength": 1
    },
    "known_limitations": {
      "type": "string",
      "minLength": 1
    },
    "update_date": {
      "type": "string",
      "format": "date"
    },
    "source_policy": {
      "type": "string",
      "minLength": 1
    },
    "compatibility": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "description": {
      "type": "string"
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "license": {
      "type": "string"
    },
    "audience_profiles": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "id",
          "label"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "label": {
            "type": "string",
            "minLength": 1
          },
          "requires_role": {
            "type": "string"
          }
        }
      }
    },
    "retrieval_hints": {
      "type": "object",
      "properties": {
        "recommended_top_k": {
          "type": "integer",
          "minimum": 1
        },
        "max_context_tokens": {
          "type": "integer",
          "minimum": 1
        },
        "use_reranker": {
          "type": "boolean"
        },
        "embedding_model": {
          "type": "string"
        },
        "index_version": {
          "type": "string"
        }
      }
    },
    "min_eval_delta": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "locales": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "base_locale": {
      "type": "string"
    },
    "publisher": {
      "type": "object",
      "required": [
        "name"
      ],
      "properties": {
        "name": {
          "type": "string",
          "minLength": 1
        },
        "url": {
          "type": "string",
          "format": "uri"
        },
        "pgp_fingerprint": {
          "type": "string"
        },
        "signed": {
          "type": "boolean"
        }
      }
    },
    "access_control": {
      "type": "object",
      "properties": {
        "classification": {
          "type": "string",
          "enum": [
            "public",
            "internal",
            "confidential",
            "restricted"
          ]
        },
        "required_roles": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "export_restrictions": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "encryption_required": {
          "type": "boolean"
        },
        "pii_present": {
          "type": "boolean"
        },
        "gdpr_scope": {
          "type": "boolean"
        },
        "mcp_scopes_required": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "mcp_audience": {
          "type": "string"
        }
      }
    },
    "dependencies": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "name",
          "version"
        ],
        "properties": {
          "name": {
            "type": "string",
            "minLength": 1
          },
          "version": {
            "type": "string",
            "minLength": 1
          },
          "domain": {
            "type": "string"
          },
          "registry": {
            "type": "string",
            "format": "uri"
          },
          "optional": {
            "type": "boolean"
          }
        }
      }
    },
    "procedure_capabilities": {
      "type": "object",
      "properties": {
        "sandbox": {
          "type": "string",
          "enum": [
            "wasm",
            "none"
          ]
        },
        "max_runtime_ms": {
          "type": "integer",
          "minimum": 1
        },
        "network_access": {
          "type": "boolean"
        },
        "filesystem_access": {
          "type": "string",
          "enum": [
            "none",
            "read-only",
            "read-write"
          ]
        }
      }
    },
    "mcp": {
      "type": "object",
      "required": [
        "enabled"
      ],
      "properties": {
        "enabled": {
          "type": "boolean"
        },
        "resource_server": {
          "type": "object",
          "properties": {
            "uri_scheme": {
              "type": "string",
              "default": "dkp"
            },
            "expose_eval_cases": {
              "type": "boolean",
              "default": false
            }
          }
        },
        "tool_provider": {
          "type": "object",
          "properties": {
            "tools": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "auth": {
              "type": "object",
              "required": [
                "scheme"
              ],
              "properties": {
                "scheme": {
                  "type": "string",
                  "enum": [
                    "none",
                    "bearer",
                    "oauth2"
                  ]
                },
                "oauth2": {
                  "type": "object",
                  "required": [
                    "authorization_url",
                    "token_url",
                    "scopes"
                  ],
                  "properties": {
                    "authorization_url": {
                      "type": "string",
                      "format": "uri"
                    },
                    "token_url": {
                      "type": "string",
                      "format": "uri"
                    },
                    "scopes": {
                      "type": "array",
                      "items": {
                        "type": "string"
                      }
                    }
                  }
                }
              },
              "if": {
                "properties": {
                  "scheme": {
                    "const": "oauth2"
                  }
                },
                "required": [
                  "scheme"
                ]
              },
              "then": {
                "required": [
                  "oauth2"
                ]
              }
            }
          }
        },
        "transport": {
          "type": "string",
          "enum": [
            "stdio",
            "http"
          ],
          "default": "stdio"
        }
      }
    }
  }
}
```

### B.23 `{procedure-id}.schema.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/procedure_schema.json",
  "title": "Procedure Schema File",
  "type": "object",
  "required": [
    "input_schema",
    "output_schema"
  ],
  "properties": {
    "input_schema": {
      "type": "object",
      "description": "JSON Schema defining the procedure's input object."
    },
    "output_schema": {
      "type": "object",
      "description": "JSON Schema defining the procedure's output object."
    },
    "entry_point": {
      "type": "object",
      "required": [
        "filename",
        "command"
      ],
      "description": "Required when {procedure-id}.wasm is absent. Declares how to invoke the alternative executable.",
      "properties": {
        "filename": {
          "type": "string",
          "description": "Exact filename of the alternative executable, including extension (e.g., \"macro_calculator.py\")."
        },
        "command": {
          "type": "string",
          "description": "Full execution command string (e.g., \"python3 macro_calculator.py\")."
        }
      }
    }
  }
}
```

### B.24 `evidence/sources.csv` Frictionless Table Schema

```json
{
  "$schema": "https://specs.frictionlessdata.io/schemas/table-schema.json",
  "fields": [
    {
      "name": "id",
      "type": "string",
      "description": "Unique source identifier (e.g., src-001). Referenced by source_ref fields throughout the pack.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "title",
      "type": "string",
      "description": "Title of the source document or resource.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "url",
      "type": "string",
      "description": "URL or DOI. Use N/A for offline-only sources.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "retrieved_date",
      "type": "date",
      "format": "%Y-%m-%d",
      "description": "ISO 8601 date the source was accessed.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "license",
      "type": "string",
      "description": "License of the source (e.g., CC-BY-4.0, Public Domain, All Rights Reserved).",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "notes",
      "type": "string",
      "description": "Any relevant notes about the source. MAY be empty."
    }
  ]
}
```

### B.25 `evidence/rights_log.csv` Frictionless Table Schema

```json
{
  "$schema": "https://specs.frictionlessdata.io/schemas/table-schema.json",
  "fields": [
    {
      "name": "id",
      "type": "string",
      "description": "Unique rights record identifier.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "source_id",
      "type": "string",
      "description": "id from sources.csv this record applies to.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "rights_holder",
      "type": "string",
      "description": "Name of the rights holder.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "license_type",
      "type": "string",
      "description": "License type or grant (e.g., Public Domain, CC-BY-4.0, Commercial License).",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "granted_date",
      "type": "date",
      "format": "%Y-%m-%d",
      "description": "ISO 8601 date rights were confirmed or license granted.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "expiry_date",
      "type": "string",
      "description": "ISO 8601 date rights expire, or the literal string 'perpetual'.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "notes",
      "type": "string",
      "description": "Any relevant notes. MAY be empty."
    }
  ]
}
```
