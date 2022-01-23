import random

def random_searcher(track, params, **kwargs):
    # choose a suitable index: if there is only one defined for this track
    # choose that one, but let the user always override index and type.
    if len(track.indices) == 1:
        default_index = track.indices[0].name
        if len(track.indices[0].types) == 1:
            default_type = track.indices[0].types[0]
        else:
            default_type = None
    else:
        default_index = "_all"
        default_type = None

    index_name = params.get("index", default_index)
    type_name = params.get("type", default_type)

    # you must provide all parameters that the runner expects
    return {
        "body": {
            "query": {
                "script_score": {
                    "query": {
                        "match_all": {}
                    },
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0", 
                        "params": {
                            "query_vector": random.choice(params["vectors"])
                        }
                    }
                }
            }
        },
        "index": index_name,
        "type": type_name,
        "cache": params.get("cache", False)
    }

def register(registry):
    registry.register_param_source("custom-searcher", random_searcher)