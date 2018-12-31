import sys


class CodeStats:

    def __init__(self, data=None):
        self._functions = []
        self._calls = dict()
        self._ids = dict()
        if data is not None:
            self.from_json(data)

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
        if fp is None:
            fp = sys.stdout
        fp.write("functions:\n")
        self.dump_functions(fp=fp, prefix="  ")
        fp.write("calls:\n")
        self.dump_calls(fp=fp, prefix="  ")
        fp.write("ids:\n")
        self.dump_ids(fp=fp, prefix="  ")

    def dump_functions(self, fp=None, prefix=""):
        if fp is None:
            fp = sys.stdout
        for f in sorted(self._functions, key=lambda f: f["name"]):
            fp.write("%s%s %s(%s)\n" % (
                prefix,
                f["type"],
                f["name"],
                ", ".join(
                    " ".join(filter(bool, (p["modifier"], p["type"], p["name"])))
                    for p in f["params"]
                )
            ))

    def dump_calls(self, fp=None, prefix=""):
        if fp is None:
            fp = sys.stdout
        for name in sorted(self._calls, key=lambda name: -self._calls[name]):
            fp.write("%s%3s %s\n" % (prefix, self._calls[name], name))

    def dump_ids(self, fp=None, prefix=""):
        if fp is None:
            fp = sys.stdout
        for id in sorted(self._ids, key=lambda id: -self._ids[id]):
            fp.write("%s%3s %s\n" % (prefix, self._ids[id], id))

    def to_json(self):
        return {
            "functions": self._functions,
            "calls": self._calls,
            "ids": self._ids,
        }

    def from_json(self, data):
        self._functions = data["functions"]
        self._calls = data["calls"]
        self._ids = data["ids"]