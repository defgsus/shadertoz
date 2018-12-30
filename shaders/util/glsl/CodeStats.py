import sys


class CodeStats:

    def __init__(self):
        self._functions = []
        self._calls = dict()
        self._ids = dict()

    def add_call(self, name):
        self._calls[name] = self._calls.get(name, 0) + 1

    def add_id(self, id):
        self._ids[id] = self._ids.get(id, 0) + 1

    def add_function(self, type, name, params, **kwargs):
        obj = {
            "type": type,
            "name": name,
            "params": params
        }
        obj.update(kwargs)
        self._functions.append(obj)

    def dump(self, fp=None):
        self.dump_functions(fp=fp)
        self.dump_calls(fp=fp)
        self.dump_ids(fp=fp)

    def dump_functions(self, fp=None):
        if fp is None:
            fp = sys.stdout
        for f in sorted(self._functions, key=lambda f: f["name"]):
            fp.write("%s %s(%s)\n" % (
                f["type"],
                f["name"],
                ", ".join(
                    " ".join(filter(bool, (p["modifier"], p["type"], p["name"])))
                    for p in f["params"]
                )
            ))

    def dump_calls(self, fp=None):
        if fp is None:
            fp = sys.stdout
        for name in sorted(self._calls, key=lambda name: -self._calls[name]):
            fp.write("%3s %s\n" % (self._calls[name], name))

    def dump_ids(self, fp=None):
        if fp is None:
            fp = sys.stdout
        for id in sorted(self._ids, key=lambda id: -self._ids[id]):
            fp.write("%3s %s\n" % (self._ids[id], id))
