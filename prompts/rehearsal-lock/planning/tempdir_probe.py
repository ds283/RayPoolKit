"""
Does an in-process ray.init(address="local", _temp_dir=D) name D on every Ray process?

The planner's probe for the rehearsal-lock campaign (README §0.3, U2), 2026-10-23. Run from an
empty scratch directory, with no Ray process on the machine and the shared lock free:

    <venv>/bin/python -u -I tempdir_probe.py /tmp/ray-rpkp

at Ray 2.43.0 / Python 3.12.15 (this repository's venv) and Ray 2.55.1 / Python 3.13.16 (an
interpreter with that Ray installed; no client code was imported). The outputs are beside this
file, with the planner's own shell removed (its command line named the temp dir) and the venv
and interpreter paths shortened. It starts Ray; it is not a test.
"""

import os, re, subprocess, sys, time
import ray

D = sys.argv[1]
ray.init(address="local", _temp_dir=D, num_cpus=2, include_dashboard=False)


@ray.remote
class A:
    def pid(self):
        return os.getpid()


@ray.remote
def f():
    return os.getpid()


a = A.remote()
pids = set(ray.get([f.remote() for _ in range(4)])) | {ray.get(a.pid.remote())}
time.sleep(2)
ps = subprocess.run(
    ["ps", "-axww", "-o", "pid=", "-o", "ppid=", "-o", "command="],
    capture_output=True,
    text=True,
).stdout
table = {}
for line in ps.splitlines():
    m = re.match(r"^\s*(\d+)\s+(\d+)\s+(.*)$", line)
    if m:
        table[int(m.group(1))] = (int(m.group(2)), m.group(3))
me = os.getpid()
d = D.removeprefix("/private")
rx = re.compile(r"(/private)?" + re.escape(d) + r"([/ =]|$)")
anc = set()
q = me
while q in table and q > 1:
    anc.add(q)
    q = table[q][0]
seeds = {p for p, (pp, c) in table.items() if rx.search(c) and p not in anc}
marked = set(seeds)
changed = True
while changed:
    changed = False
    for p, (pp, c) in table.items():
        if p not in marked and p != me and pp in marked:
            marked.add(p)
            changed = True
# Ray processes by the venv-path rule, for comparison
venv = os.path.realpath(sys.prefix)
vrx = re.compile(re.escape(venv) + r"/.*site-packages/ray/")
vseeds = {
    p for p, (pp, c) in table.items() if (vrx.search(c) or "ray::" in c) and p != me
}
kids = {p for p, (pp, c) in table.items() if pp == me}
print("ray", ray.__version__, sys.version.split()[0])
print("driver", me, "children of driver:", len(kids))
for p in sorted(kids | seeds | marked):
    pp, c = table[p]
    tag = "SEED" if p in seeds else "desc" if p in marked else "----"
    print(f"  {tag} {p} {pp} {c[:150]}")
print(
    "worker/actor pids reached by temp-dir rule:",
    sorted(pids & marked),
    "missed:",
    sorted(pids - marked),
)
print("child procs of driver missed by temp-dir rule:")
for k in sorted(kids - marked):
    print("   ", table[k][1][:600])
print(
    "client server present:",
    any("ray.util.client.server" in c for _, c in table.values()),
)
ray.shutdown()
time.sleep(3)
ps2 = subprocess.run(
    ["ps", "-axww", "-o", "pid=", "-o", "command="], capture_output=True, text=True
).stdout
left = [l for l in ps2.splitlines() if rx.search(l)]
print("left after shutdown:", left)
